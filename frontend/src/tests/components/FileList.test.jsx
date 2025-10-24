/**
 * FileList Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import FileList from '../../components/FileList';

// Mock data
const mockDatasets = [
  {
    id: '1',
    filename: 'test_dataset.csv',
    original_filename: 'test_data.csv',
    row_count: 100,
    column_count: 5,
    file_size: 1024,
    created_at: '2024-01-01T00:00:00Z',
    status: 'completed',
  },
  {
    id: '2',
    filename: 'another_dataset.csv',
    original_filename: 'another_data.csv',
    row_count: 200,
    column_count: 10,
    file_size: 2048,
    created_at: '2024-01-02T00:00:00Z',
    status: 'completed',
  },
];

// Wrapper component for Router
const Wrapper = ({ children }) => <BrowserRouter>{children}</BrowserRouter>;

describe('FileList Component', () => {
  const mockOnDelete = vi.fn();
  const mockOnRename = vi.fn();
  const mockOnRefresh = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders dataset list correctly', () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
          onRefresh={mockOnRefresh}
        />
      </Wrapper>
    );

    // Check if datasets are rendered
    expect(screen.getByText('test_data.csv')).toBeInTheDocument();
    expect(screen.getByText('another_data.csv')).toBeInTheDocument();
  });

  it('displays dataset statistics', () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    // Check if row and column counts are displayed
    expect(screen.getByText(/100 rows/i)).toBeInTheDocument();
    expect(screen.getByText(/5 columns/i)).toBeInTheDocument();
  });

  it('shows empty state when no datasets', () => {
    render(
      <Wrapper>
        <FileList
          datasets={[]}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    expect(screen.getByText(/no datasets found/i)).toBeInTheDocument();
  });

  it('opens delete confirmation modal on delete click', async () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    // Find and click delete button
    const deleteButtons = screen.getAllByTitle('Delete');
    fireEvent.click(deleteButtons[0]);

    // Check if modal appears
    await waitFor(() => {
      expect(screen.getByText(/delete dataset/i)).toBeInTheDocument();
    });
  });

  it('calls onDelete when delete is confirmed', async () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    // Click delete button
    const deleteButtons = screen.getAllByTitle('Delete');
    fireEvent.click(deleteButtons[0]);

    // Wait for modal and click confirm
    await waitFor(() => {
      const confirmButton = screen.getByText('Delete');
      fireEvent.click(confirmButton);
    });

    // Check if onDelete was called
    await waitFor(() => {
      expect(mockOnDelete).toHaveBeenCalledWith('1');
    });
  });

  it('enables rename mode when edit button is clicked', async () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    // Find and click edit button
    const editButtons = screen.getAllByTitle('Rename');
    fireEvent.click(editButtons[0]);

    // Check if input field appears
    await waitFor(() => {
      expect(screen.getByDisplayValue('test_dataset.csv')).toBeInTheDocument();
    });
  });

  it('navigates to dataset details on view click', () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    // Find view button
    const viewButtons = screen.getAllByTitle('View Details');
    expect(viewButtons[0]).toBeInTheDocument();
  });

  it('navigates to analysis page on analyze click', () => {
    render(
      <Wrapper>
        <FileList
          datasets={mockDatasets}
          onDelete={mockOnDelete}
          onRename={mockOnRename}
        />
      </Wrapper>
    );

    // Find analyze button
    const analyzeButtons = screen.getAllByTitle('Analyze');
    expect(analyzeButtons[0]).toBeInTheDocument();
  });
});
