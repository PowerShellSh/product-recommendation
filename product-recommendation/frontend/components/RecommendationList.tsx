'use client'

import { Grid, Container, Typography, CircularProgress, Alert } from '@mui/material'
import ProductCard from './ProductCard'
import { useRecommendations } from '../hooks/useProducts'

export default function RecommendationList() {
  const { data: recommendations, isLoading, error } = useRecommendations()

  if (isLoading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Container>
    )
  }

  if (error) {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="error">商品の取得に失敗しました</Alert>
      </Container>
    )
  }

  return (
    <Container sx={{ py: 4 }}>
      <Grid container spacing={3}>
        {recommendations?.map((product) => (
          <Grid item key={product.id} xs={12} sm={6} md={4} lg={3}>
            <ProductCard product={product} />
          </Grid>
        ))}
      </Grid>
    </Container>
  )
} 