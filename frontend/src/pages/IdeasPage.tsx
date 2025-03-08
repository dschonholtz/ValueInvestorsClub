import React, { useState } from 'react';
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
import { ListParams } from '../types/api';

const IdeasPage: React.FC = () => {
  const [filters, setFilters] = useState<ListParams>({
    skip: 0,
    limit: 20,
  });
  const [searchQuery, setSearchQuery] = useState('');
  
  const { data: ideas, isLoading, isError, error } = useIdeas(filters);
  
  const handleFilterChange = (field: keyof ListParams, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
    }));
  };
  
  const handleSearch = () => {
    // TODO: Implement company search once the API supports it
    console.log('Search query:', searchQuery);
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
        <Stack spacing={4} direction={{ base: 'column', md: 'row' }}>
          <Box flex="1">
            <Input 
              placeholder="Search by company..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
          </Box>
          
          <Select 
            placeholder="Position Type" 
            width={{ base: '100%', md: '200px' }}
            onChange={(e) => {
              const value = e.target.value;
              if (value === '') {
                const { is_short, ...rest } = filters;
                setFilters(rest);
              } else {
                handleFilterChange('is_short', value === 'short');
              }
            }}
          >
            <option value="long">Long</option>
            <option value="short">Short</option>
          </Select>
          
          <Select 
            placeholder="Contest Winner" 
            width={{ base: '100%', md: '200px' }}
            onChange={(e) => {
              const value = e.target.value;
              if (value === '') {
                const { is_contest_winner, ...rest } = filters;
                setFilters(rest);
              } else {
                handleFilterChange('is_contest_winner', value === 'yes');
              }
            }}
          >
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </Select>
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
            {error instanceof Error ? error.message : 'Unknown error occurred'}
          </AlertDescription>
        </Alert>
      ) : ideas && ideas.length > 0 ? (
        <>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
            {ideas.map((idea) => (
              <IdeaCard key={idea.id} idea={idea} />
            ))}
          </SimpleGrid>
          
          <Flex justify="center" mt={8}>
            <Button onClick={loadMore} size="lg" colorScheme="blue">
              Load More
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