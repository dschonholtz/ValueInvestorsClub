import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Heading,
  Text,
  Button,
  SimpleGrid,
  Stack,
  useColorModeValue,
} from '@chakra-ui/react';

const HomePage: React.FC = () => {
  return (
    <Box>
      {/* Hero Section */}
      <Box 
        bg={useColorModeValue('blue.50', 'blue.900')} 
        borderRadius="xl" 
        p={12} 
        mb={12}
        textAlign="center"
      >
        <Heading as="h1" size="2xl" mb={4}>
          VIC Analytics Dashboard
        </Heading>
        <Text fontSize="xl" maxW="3xl" mx="auto" mb={4}>
          Explore and analyze investment ideas from ValueInvestorsClub.com, tracking performance metrics
          and uncovering insights from top value investors.
        </Text>
        <Text fontSize="md" fontWeight="bold" color="blue.600" maxW="2xl" mx="auto" mb={8}>
          This is an independent analysis tool not affiliated with ValueInvestorsClub.com
        </Text>
        <Stack direction={{ base: 'column', md: 'row' }} spacing={4} justify="center">
          <Button as={RouterLink} to="/ideas" size="lg" colorScheme="blue">
            Browse Ideas
          </Button>
          <Button as={RouterLink} to="/companies" size="lg" variant="outline">
            View Companies
          </Button>
        </Stack>
      </Box>

      {/* Features Section */}
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} mb={12}>
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="md">
          <Heading fontSize="xl" mb={4}>Investment Ideas Database</Heading>
          <Text>
            Access a comprehensive collection of publicly available investment ideas from
            ValueInvestorsClub.com, including both long and short positions.
          </Text>
          <Button as={RouterLink} to="/ideas" mt={4} colorScheme="blue" variant="outline">
            Browse Ideas
          </Button>
        </Box>
        
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="md">
          <Heading fontSize="xl" mb={4}>Performance Tracking</Heading>
          <Text>
            View detailed performance metrics for each investment idea, including short-term
            and long-term returns.
          </Text>
          <Button as={RouterLink} to="/ideas" mt={4} colorScheme="blue" variant="outline">
            Analyze Performance
          </Button>
        </Box>
        
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="md">
          <Heading fontSize="xl" mb={4}>Member Insights</Heading>
          <Text>
            Discover investment ideas from top contributors and track their performance
            over time to identify successful strategies.
          </Text>
          <Button as={RouterLink} to="/users" mt={4} colorScheme="blue" variant="outline">
            View Members
          </Button>
        </Box>
      </SimpleGrid>

      {/* CTA Section */}
      <Box
        bg={useColorModeValue('gray.50', 'gray.700')}
        p={8}
        borderRadius="lg"
        textAlign="center"
      >
        <Heading size="lg" mb={4}>
          Start Exploring Investment Ideas
        </Heading>
        <Text fontSize="lg" mb={6}>
          Dive into a wealth of value investing knowledge and performance data
        </Text>
        <Button
          as={RouterLink}
          to="/ideas"
          size="lg"
          colorScheme="blue"
          px={8}
        >
          Browse Ideas
        </Button>
      </Box>
    </Box>
  );
};

export default HomePage;