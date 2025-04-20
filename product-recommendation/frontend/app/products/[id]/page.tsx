'use client'

import {
  Container,
  Grid,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Box,
} from '@mui/material'
import Image from 'next/image'
import { useProduct } from '../../../hooks/useProducts'

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const { data: product, isLoading, error } = useProduct(id)

  if (isLoading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Container>
    )
  }

  if (error || !product) {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="error">商品の取得に失敗しました</Alert>
      </Container>
    )
  }

  return (
    <Container sx={{ py: 4 }}>
      <Paper elevation={2} sx={{ p: 3 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Box sx={{ position: 'relative', height: 400 }}>
              <Image
                src={product.image_url}
                alt={product.name}
                fill
                style={{ objectFit: 'cover' }}
              />
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="h4" gutterBottom>
              {product.name}
            </Typography>
            <Typography variant="h5" color="primary" gutterBottom>
              ¥{product.price.toLocaleString()}
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              {product.category}
            </Typography>
            <Typography variant="body1" paragraph>
              {product.description}
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  )
} 