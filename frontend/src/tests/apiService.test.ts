/**
 * Tests for the API service layer
 */
import axios from 'axios';
import { ideasApi, companiesApi, usersApi } from '../api/apiService';
import { Idea, IdeaDetail, Company, User, ListParams } from '../types/api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ideasApi', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    mockedAxios.create.mockReturnValue(mockedAxios);
  });

  test('getIdeas makes correct API call with no parameters', async () => {
    // Setup
    const mockData: Idea[] = [
      {
        id: '1',
        link: 'https://example.com',
        company_id: 'company1',
        user_id: 'user1',
        date: '2023-01-01T00:00:00Z',
        is_short: false,
        is_contest_winner: false
      }
    ];
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });
    
    // Execute
    const result = await ideasApi.getIdeas();
    
    // Verify
    expect(mockedAxios.get).toHaveBeenCalledWith('/ideas/', { params: {} });
    expect(result).toEqual(mockData);
  });

  test('getIdeas makes correct API call with filter parameters', async () => {
    // Setup
    const mockData: Idea[] = [
      {
        id: '1',
        link: 'https://example.com',
        company_id: 'company1',
        user_id: 'user1',
        date: '2023-01-01T00:00:00Z',
        is_short: false,
        is_contest_winner: false
      }
    ];
    
    const params: ListParams = {
      company_id: 'company1',
      user_id: 'user1',
      is_short: false,
      limit: 10,
      skip: 0
    };
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });
    
    // Execute
    const result = await ideasApi.getIdeas(params);
    
    // Verify
    expect(mockedAxios.get).toHaveBeenCalledWith('/ideas/', { params });
    expect(result).toEqual(mockData);
  });

  test('getIdeaById makes correct API call', async () => {
    // Setup
    const mockData: IdeaDetail = {
      id: '1',
      link: 'https://example.com',
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
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });
    
    // Execute
    const result = await ideasApi.getIdeaById('1');
    
    // Verify
    expect(mockedAxios.get).toHaveBeenCalledWith('/ideas/1');
    expect(result).toEqual(mockData);
  });

  test('getIdeaPerformance makes correct API call', async () => {
    // Setup
    const mockData = {
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
    };
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });
    
    // Execute
    const result = await ideasApi.getIdeaPerformance('1');
    
    // Verify
    expect(mockedAxios.get).toHaveBeenCalledWith('/ideas/1/performance');
    expect(result).toEqual(mockData);
  });
});

describe('companiesApi', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    mockedAxios.create.mockReturnValue(mockedAxios);
  });

  test('getCompanies makes correct API call with search parameter', async () => {
    // Setup
    const mockData: Company[] = [
      {
        ticker: 'AAPL',
        company_name: 'Apple Inc.'
      }
    ];
    
    const params: ListParams = {
      search: 'Apple',
      limit: 10,
      skip: 0
    };
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });
    
    // Execute
    const result = await companiesApi.getCompanies(params);
    
    // Verify
    expect(mockedAxios.get).toHaveBeenCalledWith('/companies/', { params });
    expect(result).toEqual(mockData);
  });
});

describe('usersApi', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    mockedAxios.create.mockReturnValue(mockedAxios);
  });

  test('getUsers makes correct API call with search parameter', async () => {
    // Setup
    const mockData: User[] = [
      {
        username: 'testuser',
        user_link: 'https://example.com/users/testuser'
      }
    ];
    
    const params: ListParams = {
      search: 'test',
      limit: 10,
      skip: 0
    };
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });
    
    // Execute
    const result = await usersApi.getUsers(params);
    
    // Verify
    expect(mockedAxios.get).toHaveBeenCalledWith('/users/', { params });
    expect(result).toEqual(mockData);
  });
});

describe('API error handling', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    mockedAxios.create.mockReturnValue(mockedAxios);
  });

  test('handles server errors correctly', async () => {
    // Setup
    const errorResponse = {
      response: {
        status: 500,
        statusText: 'Internal Server Error'
      }
    };
    
    mockedAxios.get.mockRejectedValueOnce(errorResponse);
    
    // Execute and verify
    await expect(ideasApi.getIdeas()).rejects.toMatchObject({
      message: 'Server error: 500 Internal Server Error'
    });
  });

  test('handles network errors correctly', async () => {
    // Setup
    const errorResponse = {
      request: {},
      message: 'Network Error'
    };
    
    mockedAxios.get.mockRejectedValueOnce(errorResponse);
    
    // Execute and verify
    await expect(ideasApi.getIdeas()).rejects.toMatchObject({
      message: 'No response received from server. Please check your connection.'
    });
  });
});