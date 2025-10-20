/**
 * Loading Skeleton Component
 * 
 * Reusable skeleton loaders for different content types
 */

export const CardSkeleton = () => (
  <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
    <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
    <div className="h-3 bg-gray-200 rounded w-2/3"></div>
  </div>
);

export const TableSkeleton = () => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden animate-pulse">
    <div className="p-4 border-b border-gray-200">
      <div className="h-4 bg-gray-200 rounded w-1/4"></div>
    </div>
    {[...Array(5)].map((_, i) => (
      <div key={i} className="p-4 border-b border-gray-200 flex gap-4">
        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
        <div className="h-3 bg-gray-200 rounded w-1/3"></div>
        <div className="h-3 bg-gray-200 rounded w-1/5"></div>
        <div className="h-3 bg-gray-200 rounded w-1/6"></div>
      </div>
    ))}
  </div>
);

export const ChartSkeleton = () => (
  <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-1/3 mb-6"></div>
    <div className="h-64 bg-gray-200 rounded"></div>
  </div>
);

export const StatCardSkeleton = () => (
  <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
    <div className="flex items-center justify-between mb-4">
      <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      <div className="w-10 h-10 bg-gray-200 rounded-lg"></div>
    </div>
    <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div className="h-3 bg-gray-200 rounded w-1/2"></div>
  </div>
);

export const DashboardSkeleton = () => (
  <div className="p-6 space-y-6">
    {/* Stats Grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <StatCardSkeleton key={i} />
      ))}
    </div>

    {/* Charts */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <ChartSkeleton />
      <ChartSkeleton />
    </div>

    {/* Table */}
    <TableSkeleton />
  </div>
);

export default {
  Card: CardSkeleton,
  Table: TableSkeleton,
  Chart: ChartSkeleton,
  StatCard: StatCardSkeleton,
  Dashboard: DashboardSkeleton,
};
