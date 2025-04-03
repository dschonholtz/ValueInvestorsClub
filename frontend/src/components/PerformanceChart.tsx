import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { 
  Box, 
  Heading, 
  Tabs, 
  TabList, 
  Tab, 
  TabPanels, 
  TabPanel,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge
} from '@chakra-ui/react';
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
    // If we have the new timeline data, use it
    if (performance.timeline_labels && performance.timeline_values) {
      const data = performance.timeline_labels.map((label, index) => {
        // Check if timeline_values exists and has the value at this index
        const rawValue = performance.timeline_values && index < performance.timeline_values.length 
          ? performance.timeline_values[index] 
          : null;
          
        return {
          name: formatTimeLabel(label),
          value: isShort && rawValue !== null && rawValue !== undefined
            ? -rawValue 
            : rawValue
        };
      });
      return data;
    }
    
    // Fallback to the original approach if timeline data is not available
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
    if (isShort) {
      return data.map(item => ({
        ...item,
        value: item.value !== null ? -item.value : null
      }));
    }
    
    return data;
  };
  
  /**
   * Format time period labels for better display
   */
  const formatTimeLabel = (label: string): string => {
    const labelMap: Record<string, string> = {
      '1W': '1 Week',
      '2W': '2 Weeks',
      '1M': '1 Month',
      '3M': '3 Months',
      '6M': '6 Months',
      '1Y': '1 Year',
      '2Y': '2 Years',
      '3Y': '3 Years',
      '5Y': '5 Years'
    };
    
    return labelMap[label] || label;
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
      <Box p={4} borderWidth="1px" borderRadius="md">
        <Tabs>
          <TabList>
            <Tab>Bar Chart</Tab>
            <Tab>Line Chart</Tab>
            <Tab>Table</Tab>
          </TabList>
          
          <TabPanels>
            {/* Bar Chart View */}
            <TabPanel p={0} pt={4}>
              <Box height="400px">
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
            </TabPanel>
            
            {/* Line Chart View */}
            <TabPanel p={0} pt={4}>
              <Box height="400px">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
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
                    <Line 
                      type="monotone"
                      dataKey="value" 
                      name="Return %" 
                      stroke={isShort ? '#F56565' : '#48BB78'}
                      strokeWidth={2}
                      dot={{ stroke: isShort ? '#F56565' : '#48BB78', strokeWidth: 2, r: 4 }}
                      activeDot={{ r: 8 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </TabPanel>
            
            {/* Table View */}
            <TabPanel p={0} pt={4}>
              <Box overflowX="auto">
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Time Period</Th>
                      <Th isNumeric>Return (%)</Th>
                      <Th>Performance</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {data.map((item) => {
                      const value = item.value;
                      const isPositive = value !== null && value !== undefined && (
                        isShort 
                          ? value < 0  // For shorts, negative value means positive return
                          : value > 0  // For longs, positive value means positive return
                      );
                        
                      return (
                        <Tr key={item.name}>
                          <Td>{item.name}</Td>
                          <Td isNumeric>{value !== null && value !== undefined ? value.toFixed(2) + "%" : "N/A"}</Td>
                          <Td>
                            {value !== null && value !== undefined && (
                              <Badge 
                                colorScheme={isPositive ? "green" : "red"}
                                px={2}
                                py={1}
                                borderRadius="md"
                              >
                                {isPositive ? "Positive" : "Negative"}
                              </Badge>
                            )}
                          </Td>
                        </Tr>
                      );
                    })}
                  </Tbody>
                </Table>
              </Box>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Box>
  );
};

export default PerformanceChart;