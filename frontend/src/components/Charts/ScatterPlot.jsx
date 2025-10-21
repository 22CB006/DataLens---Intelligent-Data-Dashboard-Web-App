/**
 * Scatter Plot Component
 * 
 * Reusable scatter plot using Chart.js
 */

import { Scatter } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const ScatterPlot = ({ 
  data, 
  title = 'Scatter Plot',
  xLabel = '',
  yLabel = '',
  height = 400,
  showTrendline = false 
}) => {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: !!title,
        text: title,
        font: {
          size: 16,
          weight: 'bold',
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 13,
        },
        callbacks: {
          label: function(context) {
            return `(${context.parsed.x}, ${context.parsed.y})`;
          },
        },
      },
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: !!xLabel,
          text: xLabel,
        },
      },
      y: {
        title: {
          display: !!yLabel,
          text: yLabel,
        },
      },
    },
  };

  return (
    <div style={{ height: `${height}px` }}>
      <Scatter data={data} options={options} />
    </div>
  );
};

export default ScatterPlot;
