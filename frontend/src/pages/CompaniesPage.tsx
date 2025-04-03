import React, { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Input,
  Flex,
  Spinner,
  Alert,
  AlertIcon,
  Text,
  InputGroup,
  InputRightElement,
} from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';
import { useCompanies } from '../hooks/useCompanies';
import { ListParams } from '../types/api';

const CompaniesPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<ListParams>({
    skip: 0,
    limit: 50,
    search: '',
  });

  const { data: companies, isLoading, isError, error } = useCompanies(filters);

  const handleSearch = () => {
    setFilters(prev => ({
      ...prev,
      search: searchQuery,
      skip: 0, // Reset pagination on new search
    }));
  };

  const loadMore = () => {
    setFilters(prev => ({
      ...prev,
      skip: (prev.skip || 0) + (prev.limit || 50),
    }));
  };

  return (
    <Box>
      <Heading mb={6}>Companies</Heading>

      {/* Search */}
      <Box mb={6}>
        <InputGroup size="lg">
          <Input
            placeholder="Search companies by name or ticker..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <InputRightElement width="4.5rem">
            <Button h="1.75rem" size="sm" onClick={handleSearch}>
              <SearchIcon />
            </Button>
          </InputRightElement>
        </InputGroup>
      </Box>

      {/* Companies Table */}
      {isLoading && !companies ? (
        <Flex justify="center" align="center" minH="300px">
          <Spinner size="xl" />
        </Flex>
      ) : isError ? (
        <Alert status="error">
          <AlertIcon />
          <Box>
            <Heading size="md" mb={2}>Error loading companies</Heading>
            <Text>{error instanceof Error ? error.message : 'Unknown error occurred'}</Text>
          </Box>
        </Alert>
      ) : companies && companies.length > 0 ? (
        <>
          <Box overflowX="auto">
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Ticker</Th>
                  <Th>Company Name</Th>
                  <Th>View Ideas</Th>
                </Tr>
              </Thead>
              <Tbody>
                {companies.map((company) => (
                  <Tr key={company.ticker}>
                    <Td fontWeight="bold">{company.ticker}</Td>
                    <Td>{company.company_name}</Td>
                    <Td>
                      <Button
                        as={RouterLink}
                        to={`/ideas?company_id=${company.ticker}`}
                        size="sm"
                        colorScheme="blue"
                      >
                        View Ideas
                      </Button>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>

          <Flex justify="center" mt={8}>
            <Button onClick={loadMore} size="lg" colorScheme="blue">
              Load More
            </Button>
          </Flex>
        </>
      ) : (
        <Box textAlign="center" p={8}>
          <Text fontSize="xl">No companies found matching your search criteria.</Text>
        </Box>
      )}
    </Box>
  );
};

export default CompaniesPage;