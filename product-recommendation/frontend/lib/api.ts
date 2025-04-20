import { Product } from "../types";

// ブラウザから見えるバックエンドのURL
const API_BASE_URL_CLIENT = 'http://localhost:8000';
// Next.jsサーバーサイドから見えるバックエンドのURL (docker-compose.ymlの値)
const API_BASE_URL_SERVER = process.env.NEXT_PUBLIC_API_URL; // http://backend:8000

// 実行環境(ブラウザかサーバーか)に応じてベースURLを返す関数
const getApiBaseUrl = () => {
  // 'typeof window !== "undefined"' はブラウザ環境で true になる
  return typeof window !== 'undefined' ? API_BASE_URL_CLIENT : API_BASE_URL_SERVER;
};

export async function getRecommendations(): Promise<Product[]> {
  // ★★★ 適切なベースURLを取得 ★★★
  const baseUrl = getApiBaseUrl();
  // 正しいパスで呼び出す
  const response = await fetch(`${baseUrl}/api/v1/recommendations/?user_id=1`); // /v1 を確認
  if (!response.ok) {
    console.error("Failed to fetch recommendations:", response.status, await response.text());
    throw new Error('Failed to fetch recommendations');
  }
  return response.json();
}

export async function getProduct(id: string): Promise<Product | null> {
  // ★★★ 適切なベースURLを取得 ★★★
  const baseUrl = getApiBaseUrl();
  // 正しいパスで呼び出す
  const response = await fetch(`${baseUrl}/api/v1/products/${id}`); // /v1 を確認
  if (!response.ok) {
    if (response.status === 404) return null;
    console.error("Failed to fetch product:", response.status, await response.text());
    throw new Error('Failed to fetch product');
  }
  return response.json();
}