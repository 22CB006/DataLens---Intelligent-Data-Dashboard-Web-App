/**
 * Heatmap Component
 * 
 * Correlation heatmap visualization
 */

import { useEffect, useRef } from 'react';

const Heatmap = ({ 
  data, 
  title = 'Correlation Heatmap',
  height = 400 
}) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data || !data.labels) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { labels, values } = data;

    // Convert values object to 2D array if needed
    let matrixValues = values;
    if (values && typeof values === 'object' && !Array.isArray(values)) {
      // Convert object matrix to 2D array
      matrixValues = labels.map(row => 
        labels.map(col => values[row]?.[col] ?? 0)
      );
    }

    if (!matrixValues || !Array.isArray(matrixValues) || matrixValues.length === 0) {
      return;
    }

    const size = labels.length;
    const cellSize = Math.min(400 / size, 60);
    const padding = 80;
    
    canvas.width = size * cellSize + padding * 2;
    canvas.height = size * cellSize + padding * 2;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw title
    ctx.font = 'bold 16px sans-serif';
    ctx.fillStyle = '#1f2937';
    ctx.textAlign = 'center';
    ctx.fillText(title, canvas.width / 2, 30);

    // Draw heatmap cells
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        const value = matrixValues[i][j];
        const x = j * cellSize + padding;
        const y = i * cellSize + padding + 20;

        // Color based on correlation value (-1 to 1)
        const intensity = Math.abs(value);
        const color = value >= 0 
          ? `rgba(59, 130, 246, ${intensity})` // Blue for positive
          : `rgba(239, 68, 68, ${intensity})`; // Red for negative

        ctx.fillStyle = color;
        ctx.fillRect(x, y, cellSize, cellSize);

        // Draw cell border
        ctx.strokeStyle = '#e5e7eb';
        ctx.strokeRect(x, y, cellSize, cellSize);

        // Draw value text
        ctx.font = '12px sans-serif';
        ctx.fillStyle = intensity > 0.5 ? '#ffffff' : '#1f2937';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(
          value.toFixed(2),
          x + cellSize / 2,
          y + cellSize / 2
        );
      }
    }

    // Draw row labels
    ctx.font = '12px sans-serif';
    ctx.fillStyle = '#4b5563';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    for (let i = 0; i < size; i++) {
      const y = i * cellSize + padding + 20 + cellSize / 2;
      ctx.fillText(labels[i], padding - 10, y);
    }

    // Draw column labels
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    for (let j = 0; j < size; j++) {
      const x = j * cellSize + padding + cellSize / 2;
      ctx.save();
      ctx.translate(x, padding + 10);
      ctx.rotate(-Math.PI / 4);
      ctx.fillText(labels[j], 0, 0);
      ctx.restore();
    }

    // Draw color scale legend
    const legendY = canvas.height - 40;
    const legendWidth = 200;
    const legendX = (canvas.width - legendWidth) / 2;

    // Gradient
    const gradient = ctx.createLinearGradient(legendX, 0, legendX + legendWidth, 0);
    gradient.addColorStop(0, 'rgba(239, 68, 68, 1)');
    gradient.addColorStop(0.5, 'rgba(255, 255, 255, 1)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 1)');

    ctx.fillStyle = gradient;
    ctx.fillRect(legendX, legendY, legendWidth, 20);
    ctx.strokeStyle = '#d1d5db';
    ctx.strokeRect(legendX, legendY, legendWidth, 20);

    // Legend labels
    ctx.font = '11px sans-serif';
    ctx.fillStyle = '#6b7280';
    ctx.textAlign = 'left';
    ctx.fillText('-1', legendX - 20, legendY + 10);
    ctx.textAlign = 'center';
    ctx.fillText('0', legendX + legendWidth / 2, legendY + 10);
    ctx.textAlign = 'right';
    ctx.fillText('1', legendX + legendWidth + 20, legendY + 10);

  }, [data, title]);

  if (!data || !data.labels || !data.values) {
    return (
      <div className="flex items-center justify-center" style={{ height: `${height}px` }}>
        <p className="text-gray-500">No correlation data available</p>
      </div>
    );
  }

  return (
    <div className="flex justify-center overflow-auto" style={{ height: `${height}px` }}>
      <canvas ref={canvasRef} />
    </div>
  );
};

export default Heatmap;
