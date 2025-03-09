import React from 'react';
import {
  Box,
  Heading,
  Text,
  VStack,
  Link,
  UnorderedList,
  ListItem,
  Divider,
} from '@chakra-ui/react';

const AboutPage: React.FC = () => {
  return (
    <Box maxW="800px" mx="auto">
      <VStack spacing={8} align="start">
        <Box>
          <Heading as="h1" size="xl" mb={4}>About VIC Analytics Dashboard</Heading>
          <Text mb={3}>
            VIC Analytics Dashboard is an independent platform designed to provide insights and analysis
            of investment ideas shared on ValueInvestorsClub.com. This tool allows you to explore
            investment theses, track performance metrics, and discover patterns in value investing strategies.
          </Text>
          <Text fontWeight="bold" color="blue.600">
            IMPORTANT: This site is NOT affiliated with, endorsed by, or connected to ValueInvestorsClub.com in any official capacity.
            It is an independent analytical tool for publicly available investment ideas.
          </Text>
        </Box>

        <Divider />

        <Box>
          <Heading as="h2" size="lg" mb={4}>What is ValueInvestorsClub?</Heading>
          <Text mb={4}>
            <Link href="https://www.valueinvestorsclub.com" isExternal color="blue.500">
              ValueInvestorsClub.com
            </Link>{' '}
            is an exclusive online investment club where value-oriented investors share and discuss
            their best investment ideas. Founded by Joel Greenblatt and John Petry in 2000, the club
            maintains a high standard for membership and investment analysis.
          </Text>
          <Text>
            The club features both long and short investment ideas across various market capitalizations,
            sectors, and geographies. Many of these ideas come with detailed fundamental analysis and
            investment theses that reflect deep research and value investing principles.
          </Text>
        </Box>

        <Divider />

        <Box>
          <Heading as="h2" size="lg" mb={4}>Features of This Platform</Heading>
          <UnorderedList spacing={2} pl={4}>
            <ListItem>
              <Text fontWeight="bold">Investment Idea Database</Text>
              <Text>Browse through a collection of investment ideas shared on ValueInvestorsClub</Text>
            </ListItem>
            <ListItem>
              <Text fontWeight="bold">Performance Metrics</Text>
              <Text>Track the performance of investment ideas over various time periods</Text>
            </ListItem>
            <ListItem>
              <Text fontWeight="bold">Company Analysis</Text>
              <Text>View all investment ideas related to specific companies</Text>
            </ListItem>
            <ListItem>
              <Text fontWeight="bold">Member Insights</Text>
              <Text>Explore investment ideas from specific VIC members</Text>
            </ListItem>
          </UnorderedList>
        </Box>

        <Divider />

        <Box>
          <Heading as="h2" size="lg" mb={4}>Disclaimer</Heading>
          <Text mb={3}>
            This platform is provided for informational and educational purposes only. It is not
            intended as investment advice, and should not be used as the basis for any investment decision.
            The performance metrics shown are based on historical data and do not guarantee future results.
          </Text>
          <Text fontWeight="medium" color="red.600">
            This site is an independent analysis tool and is NOT affiliated with, endorsed by, sponsored by, or 
            officially connected to ValueInvestorsClub.com. All ValueInvestorsClub content is used according to 
            fair use principles for analysis and educational purposes.
          </Text>
        </Box>

        <Divider />

        <Box>
          <Heading as="h2" size="lg" mb={4}>Data Sources</Heading>
          <Text>
            The investment ideas and related information displayed on this platform are sourced from
            ValueInvestorsClub.com. Performance metrics are calculated based on publicly available
            market data. We strive to ensure the accuracy of the information presented, but cannot
            guarantee its completeness or correctness.
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default AboutPage;