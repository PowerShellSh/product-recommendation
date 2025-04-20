import RecommendationList from "../components/RecommendationList";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">おすすめ商品</h1>
      <RecommendationList />
    </div>
  )
} 