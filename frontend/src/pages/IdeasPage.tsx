import React, { useState, useEffect } from 'react';
import {
  Box,
  SimpleGrid,
  Heading,
  Text,
  Button,
  Flex,
  Select,
  Input,
  Stack,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';
import { useIdeas } from '../hooks/useIdeas';
import IdeaCard from '../components/IdeaCard';
import { ListParams, Idea } from '../types/api';
import { useLocation, useNavigate } from 'react-router-dom';

const IdeasPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get query parameters from URL
  const getInitialFilters = (): ListParams => {
    const searchParams = new URLSearchParams(location.search);
    const initialFilters: ListParams = {
      skip: 0,
      limit: 20,
    };
    
    // Add filters from URL parameters
    if (searchParams.has('company_id')) {
      initialFilters.company_id = searchParams.get('company_id') || undefined;
    }
    
    if (searchParams.has('user_id')) {
      initialFilters.user_id = searchParams.get('user_id') || undefined;
    }
    
    if (searchParams.has('is_short')) {
      initialFilters.is_short = searchParams.get('is_short') === 'true';
    }
    
    if (searchParams.has('is_contest_winner')) {
      initialFilters.is_contest_winner = searchParams.get('is_contest_winner') === 'true';
    }
    
    // Add performance filters from URL parameters
    if (searchParams.has('has_performance')) {
      initialFilters.has_performance = searchParams.get('has_performance') === 'true';
    }
    
    if (searchParams.has('min_performance')) {
      const minPerf = parseFloat(searchParams.get('min_performance') || '');
      if (!isNaN(minPerf)) {
        initialFilters.min_performance = minPerf;
      }
    }
    
    if (searchParams.has('max_performance')) {
      const maxPerf = parseFloat(searchParams.get('max_performance') || '');
      if (!isNaN(maxPerf)) {
        initialFilters.max_performance = maxPerf;
      }
    }
    
    if (searchParams.has('performance_period')) {
      initialFilters.performance_period = searchParams.get('performance_period') || undefined;
    }
    
    if (searchParams.has('sort_by')) {
      initialFilters.sort_by = searchParams.get('sort_by') || undefined;
    }
    
    if (searchParams.has('sort_order')) {
      initialFilters.sort_order = searchParams.get('sort_order') || undefined;
    }
    
    return initialFilters;
  };

  const [filters, setFilters] = useState<ListParams>(getInitialFilters());
  const [searchQuery, setSearchQuery] = useState('');
  
  // Update URL when filters change
  useEffect(() => {
    const searchParams = new URLSearchParams();
    
    // Add all non-empty filters to URL
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && key !== 'skip' && key !== 'limit') {
        searchParams.set(key, String(value));
      }
    });
    
    // Update URL without reloading the page
    const newSearch = searchParams.toString();
    if (newSearch) {
      navigate(`?${newSearch}`, { replace: true });
    } else if (location.search) {
      navigate('', { replace: true });
    }
  }, [filters, navigate, location.search]);
  
  // Keep track of all loaded ideas and seen IDs to prevent duplicates
  const [allIdeas, setAllIdeas] = React.useState<Idea[]>([]);
  const seenIdeaIds = React.useRef(new Set<string>());
  
  // Use a ref to track if we need to append or replace ideas
  const isNewFilter = React.useRef(true);
  
  // Get ideas from the API
  const { data: ideas, isLoading, isError, error } = useIdeas(filters);
  
  // When new ideas load, either append them or replace the current list
  React.useEffect(() => {
    if (ideas) {
      if (filters.skip === 0 || isNewFilter.current) {
        // Clear tracking and reset for new filters
        seenIdeaIds.current = new Set<string>();
        
        // Add new ideas to seen set
        ideas.forEach(idea => seenIdeaIds.current.add(idea.id));
        
        // Replace ideas when starting from the beginning or changing filters
        setAllIdeas(ideas);
        isNewFilter.current = false;
      } else {
        // Filter out duplicates and only add new ideas
        const newIdeas = ideas.filter(idea => !seenIdeaIds.current.has(idea.id));
        
        // Update seen set with new ideas
        newIdeas.forEach(idea => seenIdeaIds.current.add(idea.id));
        
        // Append only new ideas
        if (newIdeas.length > 0) {
          setAllIdeas(prev => [...prev, ...newIdeas]);
        }
      }
    }
  }, [ideas, filters.skip]);
  
  const handleFilterChange = (field: keyof ListParams, value: unknown) => {
    // Mark that we're changing filters
    isNewFilter.current = true;
    
    setFilters(prev => ({
      ...prev,
      skip: 0, // Reset pagination when changing filters
      [field]: value,
    }));
  };
  
  const handleSearch = () => {
    // Mark that we're changing filters
    isNewFilter.current = true;
    
    setFilters(prev => ({
      ...prev,
      skip: 0, // Reset pagination when searching
      search: searchQuery.trim() || undefined
    }));
  };
  
  const loadMore = () => {
    setFilters(prev => ({
      ...prev,
      skip: (prev.skip || 0) + (prev.limit || 20),
    }));
  };

  return (
    <Box>
      <Heading mb={6}>Investment Ideas</Heading>
      
      {/* Filters */}
      <Box mb={6} p={4} borderWidth="1px" borderRadius="lg">
        {/* Basic Filters */}
        <Stack spacing={6} direction={{ base: 'column', md: 'row' }} mb={4}>
          <Box flex="1">
            <Text fontWeight="medium" mb={1}>Search</Text>
            <Input 
              placeholder="Search by company..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              data-testid="company-search"
            />
          </Box>
          
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Position Type</Text>
            <Select 
              width="100%"
              value={filters.is_short !== undefined ? (filters.is_short ? 'short' : 'long') : 'all'}
              onChange={(e) => {
                const value = e.target.value;
                if (value === 'all') {
                  // Destructure to remove is_short but not use it directly
                  // eslint-disable-next-line @typescript-eslint/no-unused-vars
                  const { is_short, ...rest } = filters;
                  setFilters(rest);
                } else {
                  handleFilterChange('is_short', value === 'short');
                }
              }}
              data-testid="short-ideas-toggle"
            >
              <option value="all">All</option>
              <option value="long">Long</option>
              <option value="short">Short</option>
            </Select>
          </Box>
          
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Contest Winner</Text>
            <Select 
              width="100%"
              value={filters.is_contest_winner !== undefined ? (filters.is_contest_winner ? 'yes' : 'no') : 'all'}
              onChange={(e) => {
                const value = e.target.value;
                if (value === 'all') {
                  // Destructure to remove is_contest_winner but not use it directly
                  // eslint-disable-next-line @typescript-eslint/no-unused-vars
                  const { is_contest_winner, ...rest } = filters;
                  setFilters(rest);
                } else {
                  handleFilterChange('is_contest_winner', value === 'yes');
                }
              }}
              data-testid="user-search"
            >
              <option value="all">All</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </Select>
          </Box>
        </Stack>
        
        {/* Performance Filters */}
        <Heading size="sm" mt={4} mb={2}>Performance Filters</Heading>
        <Stack spacing={6} direction={{ base: 'column', md: 'row' }} mb={4}>
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Has Performance</Text>
            <Select
              width="100%"
              value={filters.has_performance !== undefined ? (filters.has_performance ? 'true' : 'false') : 'all'}
              onChange={(e) => {
                const value = e.target.value;
                if (value === 'all') {
                  // Destructure to remove has_performance
                  // eslint-disable-next-line @typescript-eslint/no-unused-vars
                  const { has_performance, ...rest } = filters;
                  setFilters(rest);
                } else {
                  handleFilterChange('has_performance', value === 'true');
                }
              }}
            >
              <option value="all">All</option>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </Select>
          </Box>
          
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Performance Period</Text>
            <Select
              width="100%"
              value={filters.performance_period || 'one_year_perf'}
              onChange={(e) => {
                const value = e.target.value;
                if (value === 'none') {
                  // Destructure to remove performance_period
                  // eslint-disable-next-line @typescript-eslint/no-unused-vars
                  const { performance_period, ...rest } = filters;
                  setFilters(rest);
                } else {
                  handleFilterChange('performance_period', value);
                }
              }}
            >
              <option value="one_week_perf">1 Week</option>
              <option value="two_week_perf">2 Weeks</option>
              <option value="one_month_perf">1 Month</option>
              <option value="three_month_perf">3 Months</option>
              <option value="six_month_perf">6 Months</option>
              <option value="one_year_perf">1 Year</option>
              <option value="two_year_perf">2 Years</option>
              <option value="three_year_perf">3 Years</option>
              <option value="five_year_perf">5 Years</option>
            </Select>
          </Box>
          
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Min Performance (%)</Text>
            <Input 
              width="100%"
              type="number"
              value={filters.min_performance !== undefined ? filters.min_performance : ''}
              onChange={(e) => {
                const value = e.target.value;
                handleFilterChange('min_performance', value === '' ? undefined : parseFloat(value));
              }}
            />
          </Box>
          
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Max Performance (%)</Text>
            <Input 
              width="100%"
              type="number"
              value={filters.max_performance !== undefined ? filters.max_performance : ''}
              onChange={(e) => {
                const value = e.target.value;
                handleFilterChange('max_performance', value === '' ? undefined : parseFloat(value));
              }}
            />
          </Box>
        </Stack>
        
        {/* Sorting Options */}
        <Heading size="sm" mb={2}>Sorting</Heading>
        <Stack spacing={6} direction={{ base: 'column', md: 'row' }}>
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Sort By</Text>
            <Select
              width="100%" 
              value={filters.sort_by || 'date'}
              onChange={(e) => {
                const value = e.target.value;
                // If sorting by performance, ensure we have a performance_period set
                if (value === 'performance' && !filters.performance_period) {
                  handleFilterChange('performance_period', 'one_year_perf');
                }
                handleFilterChange('sort_by', value);
              }}
            >
              <option value="date">Date</option>
              <option value="performance">Performance</option>
            </Select>
          </Box>
          
          {/* Only show performance period selector when sorting by performance */}
          {filters.sort_by === 'performance' && (
            <Box width={{ base: '100%', md: '200px' }}>
              <Text fontWeight="medium" mb={1}>Performance Period</Text>
              <Select
                width="100%"
                value={filters.performance_period || 'one_year_perf'}
                onChange={(e) => {
                  const value = e.target.value;
                  handleFilterChange('performance_period', value);
                }}
              >
                <option value="one_week_perf">1 Week</option>
                <option value="two_week_perf">2 Weeks</option>
                <option value="one_month_perf">1 Month</option>
                <option value="three_month_perf">3 Months</option>
                <option value="six_month_perf">6 Months</option>
                <option value="one_year_perf">1 Year</option>
                <option value="two_year_perf">2 Years</option>
                <option value="three_year_perf">3 Years</option>
                <option value="five_year_perf">5 Years</option>
              </Select>
            </Box>
          )}
          
          <Box width={{ base: '100%', md: '200px' }}>
            <Text fontWeight="medium" mb={1}>Sort Order</Text>
            <Select
              width="100%"
              value={filters.sort_order || 'desc'}
              onChange={(e) => {
                const value = e.target.value;
                handleFilterChange('sort_order', value);
              }}
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </Select>
          </Box>
        </Stack>
      </Box>
      
      {/* Ideas Grid */}
      {isLoading ? (
        <Flex justify="center" align="center" minH="300px">
          <Spinner size="xl" />
        </Flex>
      ) : isError ? (
        <Alert status="error">
          <AlertIcon />
          <AlertTitle>Error loading ideas!</AlertTitle>
          <AlertDescription>
            {error ? (error as Error).message || 'An error occurred' : 'Unknown error occurred'}
          </AlertDescription>
        </Alert>
      ) : allIdeas && allIdeas.length > 0 ? (
        <>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
            {allIdeas.map((idea) => (
              <IdeaCard 
                key={idea.id} 
                idea={idea}
                // Don't pass performance prop - we'll let the card fetch its own performance data
                // This keeps the list view light and doesn't require changes to the API
              />
            ))}
          </SimpleGrid>
          
          <Flex justify="center" mt={8}>
            <Button 
              onClick={loadMore} 
              size="lg" 
              colorScheme="blue"
              isLoading={isLoading}
              loadingText="Loading..."
              isDisabled={ideas && ideas.length === 0} // Disable if no more ideas
              data-testid="load-more-button"
            >
              {ideas && ideas.length === 0 ? "No More Ideas" : "Load More"}
            </Button>
          </Flex>
        </>
      ) : (
        <Box textAlign="center" p={8}>
          <Text fontSize="xl">No investment ideas found matching your criteria.</Text>
        </Box>
      )}
    </Box>
  );
};

export default IdeasPage;