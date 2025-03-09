/**
 * Jest setup file
 */
import '@testing-library/jest-dom';

// Mock API URL environment variable
process.env.VITE_API_URL = '/api';

// Mock window.matchMedia
window.matchMedia = (query) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: jest.fn(),
  removeListener: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  dispatchEvent: jest.fn(),
});

// Silence React Query errors in tests
const originalConsoleError = console.error;
console.error = (...args) => {
  if (
    args[0] && 
    typeof args[0] === 'string' && 
    args[0].includes('Warning: useLayoutEffect does nothing on the server')
  ) {
    return;
  }
  if (
    args[0] && 
    typeof args[0] === 'string' && 
    args[0].includes('was triggered by an UNKNOWN event')
  ) {
    return;
  }
  originalConsoleError(...args);
};