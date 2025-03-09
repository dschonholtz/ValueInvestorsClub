import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Box, Heading } from '@chakra-ui/react';
import { Performance } from '../types/api';

interface PerformanceChartProps {
  performance: Performance;
  isShort: boolean;
}

const PerformanceChart: React.FC<PerformanceChartProps> = ({ performance, isShort }) => {
  /**
   * Format performance data for chart display
   * 
   * For short positions:
   * - We invert the values to show returns from the perspective of the investor
   * - A positive percentage in the database means the stock price went up, which is bad for shorts
   * - A negative percentage in the database means the stock price went down, which is good for shorts
   * - By inverting the values, positive bars indicate a successful investment
   */
  const formatPerformanceData = () => {
    // Convert performance object to array for chart
    const data = [
      { name: '1 Week', value: performance.oneWeekClosePerf },
      { name: '2 Weeks', value: performance.twoWeekClosePerf },
      { name: '1 Month', value: performance.oneMonthPerf },
      { name: '3 Months', value: performance.threeMonthPerf },
      { name: '6 Months', value: performance.sixMonthPerf },
      { name: '1 Year', value: performance.oneYearPerf },
      { name: '2 Years', value: performance.twoYearPerf },
      { name: '3 Years', value: performance.threeYearPerf },
      { name: '5 Years', value: performance.fiveYearPerf },
    ].filter((item) => item.value !== null);

    // For short positions, invert the values for visualization
    // When a stock goes down (negative return), that's a positive result for shorts
    if (isShort) {
      return data.map(item => ({
        ...item,
        value: item.value !== null ? -item.value : null
      }));
    }
    
    return data;
  };

  const data = formatPerformanceData();
  
  // If no performance data is available
  if (data.length === 0) {
    return (
      <Box>
        <Heading size="md" mb={4}>Performance Data</Heading>
        <Box p={4} borderWidth="1px" borderRadius="md">
          No performance data available
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Heading size="md" mb={4}>Performance</Heading>
      <Box height="400px" p={4} borderWidth="1px" borderRadius="md">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis 
              tickFormatter={(value) => `${value.toFixed(2)}%`} 
              domain={['auto', 'auto']}
            />
            <Tooltip 
              formatter={(value: number) => [`${value.toFixed(2)}%`, 'Return']}
              labelFormatter={(name) => `Time Period: ${name}`}
            />
            <Legend />
            <Bar 
              dataKey="value" 
              name="Return %" 
              fill={isShort ? '#F56565' : '#48BB78'} 
            />
          </BarChart>
        </ResponsiveContainer>
      </Box>
    </Box>
  );
};

export default PerformanceChart;