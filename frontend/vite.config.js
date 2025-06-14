import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, //"127.0.0.1",
    port: 5050,
    watch: {
      usePolling: true,
    },
    proxy: {
      "/api/core": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/core/, ""),
      },
      "/api/images": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/images/, ""),
      },
    },
  },
});
