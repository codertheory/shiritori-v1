import { defineNuxtConfig } from "nuxt/config";
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: [
        "@sfxcode/nuxt-primevue",
        "@nuxt/devtools",
        "@pinia/nuxt",
        "nuxt-typed-router",
        "nuxt-icon",
        "@nuxtjs/device",
        "@nuxtjs/eslint-module",
    ],
    css: [
        "assets/css/theme.css",
        "primevue/resources/primevue.min.css",
        "primeicons/primeicons.css",
        "primeflex/primeflex.css",
    ],
    build: {
        transpile: ["primevue"],
    },
    primevue: {
        config: {
            ripple: true,
        },
    },
    typescript: {
        strict: true,
        typeCheck: true,
    },
    test: true,
    runtimeConfig: {
        public: {
            env: "dev",
            apiHost: "dev.shiritoriwithfriends.com",
        },
    },
    eslint: {
        lintOnStart: false,
    },
});
