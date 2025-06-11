import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': '/src'
        }
    },
    server: {
        port: 5173,
        host: '0.0.0.0',
        proxy: {
            '/api': 'http://localhost:5000'
        }
    }
})
