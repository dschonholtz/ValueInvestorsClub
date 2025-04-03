import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Heading, Text, Badge, Flex, Link, HStack, Skeleton, SimpleGrid } from '@chakra-ui/react';
import { Idea, Company, User, Performance } from '../types/api';
import { useQuery } from 'react-query';
import { companiesApi, usersApi, ideasApi } from '../api/apiService';

interface IdeaCardProps {
  idea: Idea;
  performance?: Performance; // Making it optional since not all ideas have performance data
}

const IdeaCard: React.FC<IdeaCardProps> = ({ idea, performance: initialPerformance }) => {
  const { id, company_id, user_id, date, is_short, is_contest_winner } = idea;
  
  // Fetch performance data if not provided
  const { data: fetchedPerformance, isLoading: isPerformanceLoading } = useQuery(
    ['idea-performance', id],
    () => ideasApi.getIdeaPerformance(id),
    {
      enabled: !initialPerformance, // Only fetch if not provided
      staleTime: 60000, // Cache results for 1 minute
      cacheTime: 300000 // Keep in cache for 5 minutes
    }
  );
  
  // Use provided performance or fetched data
  const performance = initialPerformance || fetchedPerformance;
  
  // Search by ticker/name instead of company_id
  const { data: companies, isLoading: isCompanyLoading } = useQuery<Company[]>(
    ['company-search', company_id],
    () => companiesApi.getCompanies({ search: company_id }),
    { 
      enabled: !!company_id,
      staleTime: 60000, // Cache results for 1 minute to reduce flickering
      cacheTime: 300000 // Keep in cache for 5 minutes
    }
  );
  
  // Get the first company if multiple are returned
  const company = companies && companies.length > 0 ? companies[0] : null;

  // Search by username instead of user_id
  const { data: users, isLoading: isUserLoading } = useQuery<User[]>(
    ['user-search', user_id],
    () => usersApi.getUsers({ search: user_id }),
    { 
      enabled: !!user_id,
      staleTime: 60000, // Cache results for 1 minute to reduce flickering
      cacheTime: 300000 // Keep in cache for 5 minutes
    }
  );
  
  // Get the first user if multiple are returned
  const user = users && users.length > 0 ? users[0] : null;
  
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
  
  // Format performance values with appropriate color and +/- sign
  const formatPerformance = (value: number | null | undefined, isShort: boolean) => {
    if (value === null || value === undefined) return null;
    
    // For shorts, positive stock movement is negative result for investor
    // For longs, positive stock movement is positive result for investor
    const valueAdjusted = isShort ? -value : value;
    const isPositive = valueAdjusted > 0;
    const color = isPositive ? "green.500" : "red.500";
    
    // Performance values are already stored as decimal percentages in the database
    // No need to multiply by 100
    const formattedValue = valueAdjusted.toFixed(1);
    const sign = isPositive ? "+" : "";
    
    return (
      <Text color={color} fontWeight="medium">
        {sign}{formattedValue}%
      </Text>
    );
  };

  return (
    <Box 
      p={4} 
      borderWidth="1px" 
      borderRadius="lg" 
      overflow="hidden"
      _hover={{ boxShadow: 'md', transform: 'translateY(-2px)' }}
      transition="all 0.2s"
      data-testid="idea-card"
    >
      <Flex justifyContent="space-between" alignItems="center">
        <Heading size="md">
          <Link as={RouterLink} to={`/ideas/${id}`} _hover={{ textDecoration: 'none' }}>
            <Skeleton isLoaded={!isCompanyLoading} startColor="gray.100" endColor="gray.300" display="inline">
              {company ? (
                <>
                  {company.company_name || company_id} 
                  {company.ticker && <span>({company.ticker})</span>}
                </>
              ) : (
                company_id
              )}
            </Skeleton>
          </Link>
        </Heading>
        <HStack spacing={2}>
          <Badge colorScheme={is_short ? 'red' : 'green'}>
            {is_short ? 'Short' : 'Long'}
          </Badge>
          {is_contest_winner && (
            <Badge colorScheme="purple">Contest Winner</Badge>
          )}
        </HStack>
      </Flex>
      
      <Flex mt={2} fontSize="sm" color="gray.500">
        <Text>Posted: {formattedDate}</Text>
        <Text mx={2}>|</Text>
        <Link as={RouterLink} to={`/ideas?user_id=${user_id}`}>
          <Skeleton isLoaded={!isUserLoading} startColor="gray.100" endColor="gray.300" display="inline">
            {user ? user.username || user_id : user_id}
          </Skeleton>
        </Link>
      </Flex>
      
      {/* Performance Metrics */}
      {(performance || isPerformanceLoading) && (
        <Box mt={3} pt={3} borderTopWidth="1px" borderTopColor="gray.200">
          <Skeleton 
            isLoaded={!isPerformanceLoading} 
            startColor="gray.100" 
            endColor="gray.300"
          >
            {performance && (
              <>
                <Text fontSize="xs" fontWeight="medium" mb={1} color="gray.600">
                  Performance
                </Text>
                <SimpleGrid columns={4} spacing={2} fontSize="xs">
                  {/* 1 Week */}
                  <Box>
                    <Text color="gray.500">1W</Text>
                    {formatPerformance(performance.oneWeekClosePerf, is_short)}
                  </Box>
                  
                  {/* 1 Month */}
                  <Box>
                    <Text color="gray.500">1M</Text>
                    {formatPerformance(performance.oneMonthPerf, is_short)}
                  </Box>
                  
                  {/* 6 Months */}
                  <Box>
                    <Text color="gray.500">6M</Text>
                    {formatPerformance(performance.sixMonthPerf, is_short)}
                  </Box>
                  
                  {/* 1 Year */}
                  <Box>
                    <Text color="gray.500">1Y</Text>
                    {formatPerformance(performance.oneYearPerf, is_short)}
                  </Box>
                </SimpleGrid>
              </>
            )}
          </Skeleton>
        </Box>
      )}
    </Box>
  );
};

export default IdeaCard;