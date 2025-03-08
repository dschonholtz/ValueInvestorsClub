import { useQuery, UseQueryOptions } from 'react-query';
import { ideasApi } from '../api/apiService';
import { Idea, IdeaDetail, ListParams, Performance } from '../types/api';

export function useIdeas(params: ListParams = {}, options?: UseQueryOptions<Idea[]>) {
  return useQuery<Idea[]>(
    ['ideas', params],
    () => ideasApi.getIdeas(params),
    options
  );
}

export function useIdeaDetail(id: string, options?: UseQueryOptions<IdeaDetail>) {
  return useQuery<IdeaDetail>(
    ['idea', id],
    () => ideasApi.getIdeaById(id),
    {
      enabled: !!id,
      ...options,
    }
  );
}

export function useIdeaPerformance(id: string, options?: UseQueryOptions<Performance>) {
  return useQuery<Performance>(
    ['ideaPerformance', id],
    () => ideasApi.getIdeaPerformance(id),
    {
      enabled: !!id,
      ...options,
    }
  );
}

export function useIdeaDescription(id: string, options?: UseQueryOptions<string>) {
  return useQuery<string>(
    ['ideaDescription', id],
    () => ideasApi.getIdeaDescription(id),
    {
      enabled: !!id,
      ...options,
    }
  );
}

export function useIdeaCatalysts(id: string, options?: UseQueryOptions<string>) {
  return useQuery<string>(
    ['ideaCatalysts', id],
    () => ideasApi.getIdeaCatalysts(id),
    {
      enabled: !!id,
      ...options,
    }
  );
}