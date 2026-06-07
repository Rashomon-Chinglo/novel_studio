import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite-plus";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8976",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  fmt: {
    ignorePatterns: [".agents/**", ".stitch/**", "dist/**"],
  },
  lint: {
    ignorePatterns: [".agents/**", ".stitch/**", "dist/**"],
    options: { typeAware: true, typeCheck: true },
  },
});
