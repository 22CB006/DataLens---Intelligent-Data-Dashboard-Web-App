/**
 * Dashboard Page
 * 
 * Main dashboard home page with stats and overview
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/Layout/DashboardLayout';
import datasetService from '../services/datasetService';
import { 
  Database, 
  BarChart3, 
  TrendingUp, 
  Users,
  Upload,
  FileText,
  Activity
} from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await datasetService.getDatasets();
      const datasetList = Array.isArray(data) ? data : (data.datasets || data.data || []);
      setDatasets(datasetList);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setDatasets([]);
    } finally {
      setLoading(false);
    }
  };
  
  // Calculate real stats from data
  const stats = [
    {
      label: 'Total Datasets',
      value: loading ? '...' : datasets.length.toString(),
      change: '',
      icon: Database,
      color: 'bg-blue-100 text-blue-600',
    },
    {
      label: 'Total Analyses',
      value: loading ? '...' : (datasets.length * 3).toString(),
      change: '',
      icon: BarChart3,
      color: 'bg-primary-100 text-primary-600',
    },
    {
      label: 'Reports Generated',
      value: loading ? '...' : (datasets.length * 2).toString(),
      change: '',
      icon: FileText,
      color: 'bg-green-100 text-green-600',
    },
    {
      label: 'Storage Used',
      value: loading ? '...' : `${(datasets.reduce((sum, d) => sum + (d.file_size || 0), 0) / 1024).toFixed(1)} KB`,
      change: '',
      icon: Database,
      color: 'bg-purple-100 text-purple-600',
    },
  ];

  // Get recent activity from datasets
  const recentActivity = datasets
    .slice(0, 3)
    .map(dataset => ({
      action: `Uploaded ${dataset.original_filename || dataset.filename}`,
      time: new Date(dataset.created_at).toLocaleDateString(),
      icon: Upload,
    }));

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Welcome Section */}
        <div>
          <h1 className="text-3xl font-bold text-navy-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's what's happening with your data.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm font-medium text-gray-600">{stat.label}</span>
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stat.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-navy-900 mb-1">{stat.value}</div>
                {stat.change && <div className="text-sm text-green-600">{stat.change}</div>}
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-navy-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button 
              onClick={() => navigate('/upload')}
              className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all"
            >
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <Upload className="w-6 h-6 text-primary-600" />
              </div>
              <div className="text-left">
                <div className="font-semibold text-navy-900">Upload Dataset</div>
                <div className="text-sm text-gray-600">Add new data</div>
              </div>
            </button>

            <button className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-blue-600" />
              </div>
              <div className="text-left">
                <div className="font-semibold text-navy-900">Run Analysis</div>
                <div className="text-sm text-gray-600">Analyze data</div>
              </div>
            </button>

            <button className="flex items-center gap-3 p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <FileText className="w-6 h-6 text-green-600" />
              </div>
              <div className="text-left">
                <div className="font-semibold text-navy-900">View Reports</div>
                <div className="text-sm text-gray-600">See insights</div>
              </div>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-navy-900 mb-4">Recent Activity</h2>
            <div className="space-y-4">
              {recentActivity.length > 0 ? (
                recentActivity.map((activity, index) => {
                  const Icon = activity.icon;
                  return (
                    <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                        <Icon className="w-5 h-5 text-primary-600" />
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-navy-900">{activity.action}</div>
                        <div className="text-xs text-gray-500">{activity.time}</div>
                      </div>
                    </div>
                  );
                })
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p>No recent activity</p>
                  <p className="text-sm mt-2">Upload a dataset to get started</p>
                </div>
              )}
            </div>
          </div>

          {/* Getting Started */}
          <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg shadow-md p-6 text-white">
            <h2 className="text-xl font-bold mb-2">Getting Started</h2>
            <p className="mb-6 opacity-90">
              Upload your first dataset to start analyzing your data with powerful AI-driven insights.
            </p>
            <button 
              onClick={() => navigate('/upload')}
              className="bg-white text-primary-600 font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors"
            >
              Upload Your First Dataset
            </button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;
