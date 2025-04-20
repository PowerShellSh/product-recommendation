import { Providers } from "./providers";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { AppBar, Toolbar, Typography } from "@mui/material";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Product Recommendation System",
  description: "E-commerce product recommendation system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <AppBar position="static">
            <Toolbar>
              <img
                src="https://img.icons8.com/?size=100&id=huAylk8k2FB0&format=png&color=000000"
                alt="ロゴ"
                style={{ height: "40px", marginRight: "16px" }}
              />
              <Typography variant="h6">商品推薦システム</Typography>
            </Toolbar>
          </AppBar>
          <main className="min-h-screen">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
