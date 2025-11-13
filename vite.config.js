import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import { resolve } from 'path';

export default defineConfig({
    plugins: [tailwindcss()],
    build: {
        outDir: 'static/dist',
        manifest: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'static/src/css/app.css'),
                app: resolve(__dirname, 'static/src/js/app.js'),
            },
        },
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, 'static/src'),
        },
    },
});
