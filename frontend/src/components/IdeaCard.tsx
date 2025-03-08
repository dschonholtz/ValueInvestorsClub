import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Heading, Text, Badge, Flex, Link, HStack } from '@chakra-ui/react';
import { Idea } from '../types/api';

interface IdeaCardProps {
  idea: Idea;
}

const IdeaCard: React.FC<IdeaCardProps> = ({ idea }) => {
  const { id, company_id, user_id, date, is_short, is_contest_winner } = idea;
  
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
        <Heading size="md" as={RouterLink} to={`/ideas/${id}`}>
          {company_id}
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
        <Link as={RouterLink} to={`/users/${user_id}`}>
          {user_id}
        </Link>
      </Flex>
    </Box>
  );
};

export default IdeaCard;