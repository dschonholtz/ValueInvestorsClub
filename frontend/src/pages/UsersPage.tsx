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
  Link,
} from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';
import { useUsers } from '../hooks/useUsers';
import { ListParams } from '../types/api';

const UsersPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<ListParams>({
    skip: 0,
    limit: 50,
    search: '',
  });

  const { data: users, isLoading, isError, error } = useUsers(filters);

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
      <Heading mb={6}>VIC Members</Heading>

      {/* Search */}
      <Box mb={6}>
        <InputGroup size="lg">
          <Input
            placeholder="Search users by username..."
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

      {/* Users Table */}
      {isLoading && !users ? (
        <Flex justify="center" align="center" minH="300px">
          <Spinner size="xl" />
        </Flex>
      ) : isError ? (
        <Alert status="error">
          <AlertIcon />
          <Box>
            <Heading size="md" mb={2}>Error loading users</Heading>
            <Text>{error instanceof Error ? error.message : 'Unknown error occurred'}</Text>
          </Box>
        </Alert>
      ) : users && users.length > 0 ? (
        <>
          <Box overflowX="auto">
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Username</Th>
                  <Th>View Ideas</Th>
                  <Th>Original Profile</Th>
                </Tr>
              </Thead>
              <Tbody>
                {users.map((user) => (
                  <Tr key={user.user_link}>
                    <Td fontWeight="bold">{user.username}</Td>
                    <Td>
                      <Button
                        as={RouterLink}
                        to={`/ideas?user_id=${user.user_link}`}
                        size="sm"
                        colorScheme="blue"
                      >
                        View Ideas
                      </Button>
                    </Td>
                    <Td>
                      <Link href={user.user_link} isExternal color="blue.500">
                        VIC Profile
                      </Link>
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
          <Text fontSize="xl">No users found matching your search criteria.</Text>
        </Box>
      )}
    </Box>
  );
};

export default UsersPage;