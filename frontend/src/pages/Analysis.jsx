/**
 * Analysis Page
 * 
 * Comprehensive data analysis dashboard
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/Layout/DashboardLayout';
import BarChart from '../components/Charts/BarChart';
import LineChart from '../components/Charts/LineChart';
import PieChart from '../components/Charts/PieChart';
import ScatterPlot from '../components/Charts/ScatterPlot';
import Heatmap from '../components/Charts/Heatmap';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';
import analysisService from '../services/analysisService';
import datasetService from '../services/datasetService';
import { 
  TrendingUp, 
  AlertTriangle, 
  Download, 
  RefreshCw,
  BarChart3,
  Activity,
  Database
} from 'lucide-react';

const Analysis = () => {
  const { datasetId } = useParams();
  const navigate = useNavigate();
  const { toasts, removeToast, showSuccess, showError } = useToast();
  
  const [dataset, setDataset] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [distributions, setDistributions] = useState(null);
  const [correlation, setCorrelation] = useState(null);
  const [outliers, setOutliers] = useState(null);
  const [trends, setTrends] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadData();
  }, [datasetId]);

  const loadData = async () => {
    try {
      setLoading(true);
      console.log('🔍 Loading data for dataset:', datasetId);
      
      // Load all analysis data
      const [statsData, corrData, outliersData, trendsData, datasetData, previewData] = await Promise.all([
        analysisService.getAnalysis(datasetId),
        analysisService.getCorrelation(datasetId),
        analysisService.getOutliers(datasetId),
        analysisService.getTrends(datasetId).catch(() => null), // Trends might not be available for all datasets
        datasetService.getDataset(datasetId),
        datasetService.getDatasetPreview(datasetId, 10)
      ]);
      
      console.log('📊 Stats Data:', statsData);
      console.log('🔗 Correlation Data:', corrData);
      console.log('⚠️ Outliers Data:', outliersData);
      console.log('📈 Trends Data:', trendsData);
      console.log('📁 Dataset Data:', datasetData);
      console.log('👁️ Preview Data:', previewData);
      
      // Handle new nested structure: {statistics: {...}, distributions: {...}}
      if (statsData.statistics) {
        setAnalysis(statsData.statistics);
        setDistributions(statsData.distributions || null);
        console.log('✅ Set analysis (nested):', statsData.statistics);
      } else {
        // Backward compatibility: if data is not nested
        setAnalysis(statsData);
        setDistributions(null);
        console.log('✅ Set analysis (flat):', statsData);
      }
      
      setCorrelation(corrData);
      setOutliers(outliersData);
      setTrends(trendsData);
      setDataset(datasetData);
      setPreview(previewData);
      
      console.log('✅ All data loaded successfully');
      console.log('Dataset state will be:', datasetData);
    } catch (error) {
      console.error('❌ Error loading data:', error);
      console.error('Error details:', error.response?.data);
      showError(error.userMessage || 'Failed to load analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleRunAnalysis = async () => {
    try {
      setAnalyzing(true);
      const result = await analysisService.runAnalysis(datasetId);
      setAnalysis(result);
      showSuccess('Analysis completed successfully!');
      loadData(); // Reload all data
    } catch (error) {
      showError(error.userMessage || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleExport = async (format) => {
    try {
      const blob = await analysisService.exportAnalysis(datasetId, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analysis_${datasetId}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      showSuccess(`Analysis exported as ${format.toUpperCase()}`);
    } catch (error) {
      showError('Export failed');
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mb-4"></div>
            <p className="text-gray-600">Loading analysis...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  console.log('🔎 Current dataset state:', dataset);
  console.log('🔎 Loading state:', loading);
  
  if (!dataset) {
    console.log('⚠️ Dataset is null/undefined, showing "not found" message');
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-gray-600">Dataset not found</p>
          <button onClick={() => navigate('/upload')} className="btn-primary mt-4">
            Go to Upload
          </button>
        </div>
      </DashboardLayout>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'correlation', label: 'Correlation', icon: Activity },
    { id: 'outliers', label: 'Outliers', icon: AlertTriangle },
    { id: 'trends', label: 'Trends', icon: TrendingUp },
    { id: 'data', label: 'Data Preview', icon: Database },
  ];

  return (
    <DashboardLayout>
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-navy-900">{dataset.original_filename || dataset.filename}</h1>
            <p className="text-gray-600 mt-1">
              {dataset.row_count?.toLocaleString() || 0} rows × {dataset.column_count?.toLocaleString() || 0} columns
            </p>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={loadData}
              className="btn-secondary flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
            
            {!analysis ? (
              <button
                onClick={handleRunAnalysis}
                disabled={analyzing}
                className="btn-primary flex items-center gap-2"
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <BarChart3 className="w-4 h-4" />
                    Run Analysis
                  </>
                )}
              </button>
            ) : (
              <button
                onClick={() => handleExport('pdf')}
                className="btn-primary flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Export PDF
              </button>
            )}
          </div>
        </div>

        {!analysis ? (
          <div className="card text-center py-12">
            <BarChart3 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No Analysis Available
            </h3>
            <p className="text-gray-600 mb-6">
              Run analysis to generate insights and visualizations
            </p>
            <button
              onClick={handleRunAnalysis}
              disabled={analyzing}
              className="btn-primary"
            >
              {analyzing ? 'Analyzing...' : 'Run Analysis Now'}
            </button>
          </div>
        ) : (
          <>
            {/* Tabs */}
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`
                        flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm
                        ${activeTab === tab.id
                          ? 'border-primary-500 text-primary-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }
                      `}
                    >
                      <Icon className="w-4 h-4" />
                      {tab.label}
                    </button>
                  );
                })}
              </nav>
            </div>

            {/* Tab Content */}
            <div className="space-y-6">
              {activeTab === 'overview' && (
                <>
                  {/* Statistical Summary */}
                  <div className="card">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      Statistical Summary
                    </h2>
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                              Column
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                              Mean
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                              Median
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                              Std Dev
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                              Min
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                              Max
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {analysis && Object.entries(analysis).map(([col, stats]) => (
                            <tr key={col}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                {col}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {stats.mean?.toFixed(2) || 'N/A'}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {stats.median?.toFixed(2) || 'N/A'}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {stats.std?.toFixed(2) || 'N/A'}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {stats.min?.toFixed(2) || 'N/A'}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {stats.max?.toFixed(2) || 'N/A'}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* Statistical Visualizations */}
                  {analysis && Object.keys(analysis).length > 0 && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {/* Mean vs Median Comparison */}
                      <div className="card">
                        <BarChart
                          data={{
                            labels: Object.keys(analysis),
                            datasets: [
                              {
                                label: 'Mean',
                                data: Object.values(analysis).map(s => s.mean || 0),
                                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                                borderColor: 'rgba(59, 130, 246, 1)',
                                borderWidth: 2,
                              },
                              {
                                label: 'Median',
                                data: Object.values(analysis).map(s => s.median || 0),
                                backgroundColor: 'rgba(16, 185, 129, 0.6)',
                                borderColor: 'rgba(16, 185, 129, 1)',
                                borderWidth: 2,
                              },
                            ],
                          }}
                          title="Mean vs Median Comparison"
                          height={300}
                        />
                      </div>

                      {/* Standard Deviation */}
                      <div className="card">
                        <BarChart
                          data={{
                            labels: Object.keys(analysis),
                            datasets: [{
                              label: 'Standard Deviation',
                              data: Object.values(analysis).map(s => s.std || 0),
                              backgroundColor: 'rgba(251, 146, 60, 0.6)',
                              borderColor: 'rgba(251, 146, 60, 1)',
                              borderWidth: 2,
                            }],
                          }}
                          title="Standard Deviation by Column"
                          height={300}
                        />
                      </div>

                      {/* Min-Max Range */}
                      <div className="card">
                        <BarChart
                          data={{
                            labels: Object.keys(analysis),
                            datasets: [
                              {
                                label: 'Min',
                                data: Object.values(analysis).map(s => s.min || 0),
                                backgroundColor: 'rgba(239, 68, 68, 0.6)',
                                borderColor: 'rgba(239, 68, 68, 1)',
                                borderWidth: 2,
                              },
                              {
                                label: 'Max',
                                data: Object.values(analysis).map(s => s.max || 0),
                                backgroundColor: 'rgba(139, 92, 246, 0.6)',
                                borderColor: 'rgba(139, 92, 246, 1)',
                                borderWidth: 2,
                              },
                            ],
                          }}
                          title="Min-Max Range by Column"
                          height={300}
                        />
                      </div>

                      {/* Data Overview Pie Chart */}
                      <div className="card">
                        <PieChart
                          data={{
                            labels: Object.keys(analysis),
                            datasets: [{
                              label: 'Count',
                              data: Object.values(analysis).map(s => s.count || 0),
                              backgroundColor: [
                                'rgba(59, 130, 246, 0.8)',
                                'rgba(16, 185, 129, 0.8)',
                                'rgba(251, 146, 60, 0.8)',
                                'rgba(239, 68, 68, 0.8)',
                                'rgba(139, 92, 246, 0.8)',
                                'rgba(236, 72, 153, 0.8)',
                              ],
                              borderColor: [
                                'rgba(59, 130, 246, 1)',
                                'rgba(16, 185, 129, 1)',
                                'rgba(251, 146, 60, 1)',
                                'rgba(239, 68, 68, 1)',
                                'rgba(139, 92, 246, 1)',
                                'rgba(236, 72, 153, 1)',
                              ],
                              borderWidth: 2,
                            }],
                          }}
                          title="Data Count Distribution"
                          height={300}
                        />
                      </div>
                    </div>
                  )}

                  {/* Distribution Histograms */}
                  {distributions && Object.keys(distributions).length > 0 && (
                    <div className="space-y-4">
                      <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                        Distribution Histograms
                      </h2>
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {Object.entries(distributions).map(([col, dist]) => (
                          <div key={col} className="card">
                            <BarChart
                              data={{
                                labels: dist.labels,
                                datasets: [{
                                  label: `${col} Frequency`,
                                  data: dist.values,
                                  backgroundColor: 'rgba(59, 130, 246, 0.6)',
                                  borderColor: 'rgba(59, 130, 246, 1)',
                                  borderWidth: 2,
                                }],
                              }}
                              title={`${col} Distribution`}
                              xLabel="Value Range"
                              yLabel="Frequency"
                              height={300}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}

              {activeTab === 'correlation' && (
                <div className="space-y-6">
                  {/* Correlation Heatmap */}
                  {correlation && correlation.matrix && correlation.columns && (
                    <div className="card">
                      <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        Correlation Heatmap
                      </h2>
                      <Heatmap
                        data={{
                          labels: correlation.columns,
                          values: correlation.matrix,
                        }}
                        title=""
                        height={500}
                      />
                    </div>
                  )}

                  {/* Strong Correlations Table */}
                  <div className="card">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      Strong Correlations
                    </h2>
                    {correlation && correlation.strong_correlations && correlation.strong_correlations.length > 0 ? (
                      <div className="space-y-6">
                        {/* Bar Chart of Correlations */}
                        <BarChart
                          data={{
                            labels: correlation.strong_correlations.map(c => `${c.column1} × ${c.column2}`),
                            datasets: [{
                              label: 'Correlation Coefficient',
                              data: correlation.strong_correlations.map(c => c.correlation),
                              backgroundColor: correlation.strong_correlations.map(c => 
                                c.correlation >= 0 ? 'rgba(16, 185, 129, 0.6)' : 'rgba(239, 68, 68, 0.6)'
                              ),
                              borderColor: correlation.strong_correlations.map(c => 
                                c.correlation >= 0 ? 'rgba(16, 185, 129, 1)' : 'rgba(239, 68, 68, 1)'
                              ),
                              borderWidth: 2,
                            }],
                          }}
                          title="Correlation Strength"
                          height={300}
                        />

                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                  Column 1
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                  Column 2
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                  Correlation
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                  Strength
                                </th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {correlation.strong_correlations.map((corr, idx) => (
                                <tr key={idx}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    {corr.column1}
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    {corr.column2}
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {corr.correlation.toFixed(3)}
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                      corr.strength.includes('positive') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                    }`}>
                                      {corr.strength}
                                    </span>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    ) : (
                      <p className="text-gray-500 text-center py-8">
                        No strong correlations found
                      </p>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'outliers' && (
                <div className="space-y-6">
                  {/* Outlier Summary Chart */}
                  {outliers && Object.keys(outliers).length > 0 && (
                    <div className="card">
                      <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        Outlier Summary
                      </h2>
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Outlier Count Bar Chart */}
                        <BarChart
                          data={{
                            labels: Object.keys(outliers),
                            datasets: [{
                              label: 'Outlier Count',
                              data: Object.values(outliers).map(d => d.count || 0),
                              backgroundColor: 'rgba(239, 68, 68, 0.6)',
                              borderColor: 'rgba(239, 68, 68, 1)',
                              borderWidth: 2,
                            }],
                          }}
                          title="Outliers by Column"
                          height={300}
                        />

                        {/* Outlier Percentage Pie Chart */}
                        <PieChart
                          data={{
                            labels: Object.keys(outliers),
                            datasets: [{
                              label: 'Outlier Percentage',
                              data: Object.values(outliers).map(d => d.percentage || 0),
                              backgroundColor: [
                                'rgba(239, 68, 68, 0.8)',
                                'rgba(251, 146, 60, 0.8)',
                                'rgba(234, 179, 8, 0.8)',
                                'rgba(139, 92, 246, 0.8)',
                                'rgba(236, 72, 153, 0.8)',
                                'rgba(59, 130, 246, 0.8)',
                              ],
                              borderColor: [
                                'rgba(239, 68, 68, 1)',
                                'rgba(251, 146, 60, 1)',
                                'rgba(234, 179, 8, 1)',
                                'rgba(139, 92, 246, 1)',
                                'rgba(236, 72, 153, 1)',
                                'rgba(59, 130, 246, 1)',
                              ],
                              borderWidth: 2,
                            }],
                          }}
                          title="Outlier Distribution (%)"
                          height={300}
                        />
                      </div>
                    </div>
                  )}

                  {/* Outlier Details */}
                  <div className="card">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      Outlier Detection Details
                    </h2>
                    {outliers && Object.keys(outliers).length > 0 ? (
                      <div className="space-y-6">
                        {Object.entries(outliers).map(([column, data]) => (
                          <div key={column} className="border-b border-gray-200 pb-4 last:border-b-0">
                            <h3 className="text-lg font-medium text-gray-900 mb-3">{column}</h3>
                            {data.count > 0 ? (
                              <div className="space-y-2">
                                <div className="flex items-center justify-between text-sm">
                                  <span className="text-gray-600">Outliers Found:</span>
                                  <span className="font-semibold text-red-600">{data.count} ({data.percentage.toFixed(1)}%)</span>
                                </div>
                                <div className="flex items-center justify-between text-sm">
                                  <span className="text-gray-600">Method:</span>
                                  <span className="font-medium">{data.method.toUpperCase()}</span>
                                </div>
                                <div className="flex items-center justify-between text-sm">
                                  <span className="text-gray-600">Lower Bound:</span>
                                  <span className="font-medium">{data.lower_bound?.toFixed(2)}</span>
                                </div>
                                <div className="flex items-center justify-between text-sm">
                                  <span className="text-gray-600">Upper Bound:</span>
                                  <span className="font-medium">{data.upper_bound?.toFixed(2)}</span>
                                </div>
                                {data.values && data.values.length > 0 && (
                                  <div className="mt-2">
                                    <span className="text-sm text-gray-600">Outlier Values:</span>
                                    <div className="flex flex-wrap gap-2 mt-1">
                                      {data.values.slice(0, 10).map((val, idx) => (
                                        <span key={idx} className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">
                                          {typeof val === 'number' ? val.toFixed(2) : val}
                                        </span>
                                      ))}
                                      {data.values.length > 10 && (
                                        <span className="text-xs text-gray-500">+{data.values.length - 10} more</span>
                                      )}
                                    </div>
                                  </div>
                                )}
                              </div>
                            ) : (
                              <p className="text-sm text-green-600">✓ No outliers detected</p>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-500 text-center py-8">
                        No outlier data available
                      </p>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'trends' && (
                <div className="space-y-6">
                  {trends && Object.keys(trends).length > 0 ? (
                    <>
                      {/* Trend Summary */}
                      <div className="card">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4">
                          Trend Analysis Summary
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {Object.entries(trends).map(([column, trendData]) => (
                            <div key={column} className="p-4 bg-gray-50 rounded-lg">
                              <h3 className="font-medium text-gray-900 mb-2">{column}</h3>
                              {trendData.trend && (
                                <div className="space-y-1 text-sm">
                                  <div className="flex justify-between">
                                    <span className="text-gray-600">Direction:</span>
                                    <span className={`font-semibold ${
                                      trendData.trend.direction === 'increasing' ? 'text-green-600' :
                                      trendData.trend.direction === 'decreasing' ? 'text-red-600' :
                                      'text-gray-600'
                                    }`}>
                                      {trendData.trend.direction || 'stable'}
                                    </span>
                                  </div>
                                  {trendData.trend.slope !== undefined && (
                                    <div className="flex justify-between">
                                      <span className="text-gray-600">Slope:</span>
                                      <span className="font-medium">{trendData.trend.slope.toFixed(4)}</span>
                                    </div>
                                  )}
                                  {trendData.trend.r_squared !== undefined && (
                                    <div className="flex justify-between">
                                      <span className="text-gray-600">R²:</span>
                                      <span className="font-medium">{trendData.trend.r_squared.toFixed(4)}</span>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Trend Line Charts */}
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {Object.entries(trends).map(([column, trendData]) => (
                          trendData.values && trendData.values.length > 0 && (
                            <div key={column} className="card">
                              <LineChart
                                data={{
                                  labels: trendData.values.map((_, idx) => `Point ${idx + 1}`),
                                  datasets: [{
                                    label: column,
                                    data: trendData.values,
                                    borderColor: 'rgba(59, 130, 246, 1)',
                                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                    borderWidth: 2,
                                    fill: true,
                                    tension: 0.4,
                                  }],
                                }}
                                title={`${column} Trend`}
                                height={300}
                              />
                            </div>
                          )
                        ))}
                      </div>
                    </>
                  ) : (
                    <div className="card">
                      <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        Trend Analysis
                      </h2>
                      <div className="text-center py-12">
                        <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 mb-2">
                          No Trend Data Available
                        </h3>
                        <p className="text-gray-600 mb-4">
                          Trend analysis requires time-series or sequential data.
                        </p>
                        <p className="text-sm text-gray-500">
                          Your dataset shows statistical patterns but doesn't have a clear time-based or sequential structure for trend analysis.
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'data' && (
                <div className="card">
                  <h2 className="text-xl font-semibold text-gray-900 mb-4">
                    Data Preview
                  </h2>
                  {preview && preview.data && preview.data.length > 0 ? (
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            {preview.columns.map((col) => (
                              <th
                                key={col}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                              >
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {preview.data.map((row, idx) => (
                            <tr key={idx} className="hover:bg-gray-50">
                              {preview.columns.map((col) => (
                                <td
                                  key={col}
                                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                  {row[col] !== null && row[col] !== undefined
                                    ? String(row[col])
                                    : 'N/A'}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                      <p className="text-sm text-gray-500 mt-4 text-center">
                        Showing first 10 rows of {dataset.row_count?.toLocaleString() || 'N/A'} total rows
                      </p>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-8">
                      No preview data available
                    </p>
                  )}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
};

export default Analysis;
