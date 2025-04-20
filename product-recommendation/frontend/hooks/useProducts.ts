import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getProduct, getRecommendations } from '../lib/api'

export const useRecommendations = () => {
  return useQuery({
    queryKey: ['recommendations'],
    queryFn: getRecommendations,
  })
}

export function useProduct(id: string) {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => getProduct(id),
    enabled: !!id,
  })
} 