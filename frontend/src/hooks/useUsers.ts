import { useQuery, UseQueryOptions } from 'react-query';
import { usersApi } from '../api/apiService';
import { User, ListParams } from '../types/api';

export function useUsers(params: ListParams = {}, options?: UseQueryOptions<User[]>) {
  return useQuery<User[]>(
    ['users', params],
    () => usersApi.getUsers(params),
    options
  );
}