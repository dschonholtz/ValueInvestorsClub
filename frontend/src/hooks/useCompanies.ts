import { useQuery, UseQueryOptions } from 'react-query';
import { companiesApi } from '../api/apiService';
import { Company, ListParams } from '../types/api';

export function useCompanies(params: ListParams = {}, options?: UseQueryOptions<Company[]>) {
  return useQuery<Company[]>(
    ['companies', params],
    () => companiesApi.getCompanies(params),
    options
  );
}