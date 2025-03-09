/**
 * Tests for the useIdeas hook
 */
import { renderHook } from '@testing-library/react-hooks';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ideasApi } from '../api/apiService';
import { useIdeas, useIdeaDetail } from '../hooks/useIdeas';
import React from 'react';

// Mock the API
jest.mock('../api/apiService', () => ({
  ideasApi: {
    getIdeas: jest.fn(),
    getIdeaById: jest.fn(),
    getIdeaPerformance: jest.fn(),
    getIdeaDescription: jest.fn(),
    getIdeaCatalysts: jest.fn(),
  }
}));

// Sample test data
const mockIdeas = [
  {
    id: '1',
    link: 'https://example.com/1',
    company_id: 'company1',
    user_id: 'user1',
    date: '2023-01-01T00:00:00Z',
    is_short: false,
    is_contest_winner: false
  },
  {
    id: '2',
    link: 'https://example.com/2',
    company_id: 'company2',
    user_id: 'user2',
    date: '2023-01-02T00:00:00Z',
    is_short: true,
    is_contest_winner: true
  }
];

const mockIdeaDetail = {
  id: '1',
  link: 'https://example.com/1',
  company_id: 'company1',
  user_id: 'user1',
  date: '2023-01-01T00:00:00Z',
  is_short: false,
  is_contest_winner: false,
  company: {
    ticker: 'AAPL',
    company_name: 'Apple Inc.'
  },
  user: {
    username: 'testuser',
    user_link: 'https://example.com/users/testuser'
  },
  description: {
    description: 'Test description'
  },
  catalysts: {
    catalysts: 'Test catalysts'
  },
  performance: {
    nextDayOpen: 1.0,
    nextDayClose: 1.1,
    oneWeekClosePerf: 1.2,
    twoWeekClosePerf: 1.3,
    oneMonthPerf: 1.4,
    threeMonthPerf: 1.5,
    sixMonthPerf: 1.6,
    oneYearPerf: 1.7,
    twoYearPerf: 1.8,
    threeYearPerf: 1.9,
    fiveYearPerf: 2.0
  }
};

// Setup wrapper for react-query
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useIdeas hook', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('fetches and returns ideas with no parameters', async () => {
    // Setup
    (ideasApi.getIdeas as jest.Mock).mockResolvedValueOnce(mockIdeas);
    
    // Execute
    const { result, waitFor } = renderHook(() => useIdeas(), {
      wrapper: createWrapper(),
    });
    
    // Verify initial loading state
    expect(result.current.isLoading).toBe(true);
    
    // Wait for query to resolve
    await waitFor(() => result.current.isSuccess);
    
    // Verify data
    expect(ideasApi.getIdeas).toHaveBeenCalledWith({});
    expect(result.current.data).toEqual(mockIdeas);
  });

  test('fetches and returns ideas with filter parameters', async () => {
    // Setup
    const params = {
      company_id: 'company1',
      is_short: false,
      limit: 10
    };
    
    (ideasApi.getIdeas as jest.Mock).mockResolvedValueOnce([mockIdeas[0]]);
    
    // Execute
    const { result, waitFor } = renderHook(() => useIdeas(params), {
      wrapper: createWrapper(),
    });
    
    // Wait for query to resolve
    await waitFor(() => result.current.isSuccess);
    
    // Verify
    expect(ideasApi.getIdeas).toHaveBeenCalledWith(params);
    expect(result.current.data).toEqual([mockIdeas[0]]);
  });

  test('handles error states correctly', async () => {
    // Setup
    const error = new Error('Failed to fetch ideas');
    (ideasApi.getIdeas as jest.Mock).mockRejectedValueOnce(error);
    
    // Execute
    const { result, waitFor } = renderHook(() => useIdeas(), {
      wrapper: createWrapper(),
    });
    
    // Wait for query to fail
    await waitFor(() => result.current.isError);
    
    // Verify
    expect(result.current.error).toBe(error);
  });
});

describe('useIdeaDetail hook', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('fetches and returns idea detail', async () => {
    // Setup
    (ideasApi.getIdeaById as jest.Mock).mockResolvedValueOnce(mockIdeaDetail);
    
    // Execute
    const { result, waitFor } = renderHook(() => useIdeaDetail('1'), {
      wrapper: createWrapper(),
    });
    
    // Wait for query to resolve
    await waitFor(() => result.current.isSuccess);
    
    // Verify
    expect(ideasApi.getIdeaById).toHaveBeenCalledWith('1');
    expect(result.current.data).toEqual(mockIdeaDetail);
  });

  test('does not fetch when id is not provided', async () => {
    // Execute
    const { result } = renderHook(() => useIdeaDetail(''), {
      wrapper: createWrapper(),
    });
    
    // Verify
    expect(ideasApi.getIdeaById).not.toHaveBeenCalled();
    expect(result.current.isIdle).toBe(true);
  });

  test('handles error states correctly', async () => {
    // Setup
    const error = new Error('Failed to fetch idea detail');
    (ideasApi.getIdeaById as jest.Mock).mockRejectedValueOnce(error);
    
    // Execute
    const { result, waitFor } = renderHook(() => useIdeaDetail('1'), {
      wrapper: createWrapper(),
    });
    
    // Wait for query to fail
    await waitFor(() => result.current.isError);
    
    // Verify
    expect(result.current.error).toBe(error);
  });
});