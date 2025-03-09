import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Heading, Text, Badge, Flex, Link, HStack, Skeleton } from '@chakra-ui/react';
import { Idea, Company, User } from '../types/api';
import { useQuery } from 'react-query';
import { companiesApi, usersApi } from '../api/apiService';

interface IdeaCardProps {
  idea: Idea;
}

const IdeaCard: React.FC<IdeaCardProps> = ({ idea }) => {
  const { id, company_id, user_id, date, is_short, is_contest_winner } = idea;
  
  // Search by ticker/name instead of company_id
  const { data: companies } = useQuery<Company[]>(
    ['company-search', company_id],
    () => companiesApi.getCompanies({ search: company_id }),
    { enabled: !!company_id }
  );
  
  // Get the first company if multiple are returned
  const company = companies && companies.length > 0 ? companies[0] : null;

  // Search by username instead of user_id
  const { data: users } = useQuery<User[]>(
    ['user-search', user_id],
    () => usersApi.getUsers({ search: user_id }),
    { enabled: !!user_id }
  );
  
  // Get the first user if multiple are returned
  const user = users && users.length > 0 ? users[0] : null;
  
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

  return (
    <Box 
      p={4} 
      borderWidth="1px" 
      borderRadius="lg" 
      overflow="hidden"
      _hover={{ boxShadow: 'md', transform: 'translateY(-2px)' }}
      transition="all 0.2s"
    >
      <Flex justifyContent="space-between" alignItems="center">
        <Heading size="md">
          <Link as={RouterLink} to={`/ideas/${id}`} _hover={{ textDecoration: 'none' }}>
            {company ? (
              <>
                {company.company_name || company_id} 
                {company.ticker && <span>({company.ticker})</span>}
              </>
            ) : (
              <Skeleton isLoaded={!!companies}>
                {company_id}
              </Skeleton>
            )}
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
          {user ? (
            user.username || user_id
          ) : (
            <Skeleton isLoaded={!!user}>
              {user_id}
            </Skeleton>
          )}
        </Link>
      </Flex>
    </Box>
  );
};

export default IdeaCard;