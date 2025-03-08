import axios from 'axios';
import { Idea, IdeaDetail, Company, User, ListParams, Performance } from '../types/api';

// Base API URL
const API_URL = '/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Ideas API
export const ideasApi = {
  getIdeas: async (params: ListParams = {}): Promise<Idea[]> => {
    const response = await apiClient.get('/ideas/', { params });
    return response.data;
  },

  getIdeaById: async (id: string): Promise<IdeaDetail> => {
    const response = await apiClient.get(`/ideas/${id}`);
    return response.data;
  },

  getIdeaPerformance: async (id: string): Promise<Performance> => {
    const response = await apiClient.get(`/ideas/${id}/performance`);
    return response.data;
  },

  getIdeaDescription: async (id: string): Promise<string> => {
    const response = await apiClient.get(`/ideas/${id}/description`);
    return response.data.description;
  },

  getIdeaCatalysts: async (id: string): Promise<string> => {
    const response = await apiClient.get(`/ideas/${id}/catalysts`);
    return response.data.catalysts;
  },
};

// Companies API
export const companiesApi = {
  getCompanies: async (params: ListParams = {}): Promise<Company[]> => {
    const response = await apiClient.get('/companies/', { params });
    return response.data;
  },
};

// Users API
export const usersApi = {
  getUsers: async (params: ListParams = {}): Promise<User[]> => {
    const response = await apiClient.get('/users/', { params });
    return response.data;
  },
};

// Health check API
export const healthApi = {
  check: async (): Promise<{ status: string }> => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};