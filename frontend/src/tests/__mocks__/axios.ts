// Mock for axios
import { jest } from '@jest/globals';

interface AxiosMock {
  create: jest.Mock;
  get: jest.Mock;
  post: jest.Mock;
  put: jest.Mock;
  delete: jest.Mock;
  interceptors: {
    request: {
      use: jest.Mock;
      eject: jest.Mock;
    };
    response: {
      use: jest.Mock;
      eject: jest.Mock;
    };
  };
  defaults: {
    baseURL: string;
    headers: {
      'Content-Type': string;
    };
  };
}

const axiosMock: AxiosMock = {
  create: jest.fn().mockReturnThis(),
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  interceptors: {
    request: {
      use: jest.fn(),
      eject: jest.fn(),
    },
    response: {
      use: jest.fn(),
      eject: jest.fn(),
    },
  },
  defaults: {
    baseURL: 'http://localhost:8000',
    headers: {
      'Content-Type': 'application/json',
    },
  },
};

export default axiosMock;