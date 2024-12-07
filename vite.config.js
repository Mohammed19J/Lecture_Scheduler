import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Replace <repository-name> with the name of your GitHub repository
export default defineConfig({
  plugins: [react()],
  base: '/Lecture_Scheduler/', // Important for GitHub Pages
});
