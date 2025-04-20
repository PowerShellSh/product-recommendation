import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  CardActionArea,
} from '@mui/material'
import { useRouter } from 'next/navigation'
import { Product } from '../types'

interface ProductCardProps {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  const router = useRouter()

  return (
    <Card>
      <CardActionArea onClick={() => router.push(`/products/${product.id}`)}>
        <CardMedia
          component="img"
          height="200"
          image={product.image_url}
          alt={product.name}
        />
        <CardContent>
          <Typography gutterBottom variant="h6" component="div">
            {product.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {product.category}
          </Typography>
          <Typography variant="h6" color="primary" sx={{ mt: 1 }}>
            ¥{product.price.toLocaleString()}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  )
} 