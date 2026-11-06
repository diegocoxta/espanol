/** @type {import('next').NextConfig} */
const nextConfig = {
  // Gera um site 100% estático em /out — o progresso vive no localStorage do navegador,
  // então não há servidor nem banco de dados. Funciona em Vercel, Netlify, GitHub Pages etc.
  output: "export",
  trailingSlash: true, // gera /pronominales/index.html (funciona em qualquer hospedagem estática)
  reactStrictMode: true,
  eslint: { ignoreDuringBuilds: true },
};

export default nextConfig;
