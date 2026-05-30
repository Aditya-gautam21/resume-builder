import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/tailored-resume': 'http://localhost:8000',
      '/parse-resume': 'http://localhost:8000',
      '/job-description': 'http://localhost:8000',
    },
  },
})
