import { computed } from "vue";
import { useRuntimeConfig } from "#app";

export const useConfig = () => {
    const config = useRuntimeConfig();

    const isProduction = computed(() => process.env.NODE_ENV === "production");
    const isTest = computed(() => config.public.env === "test");

    const baseURL = computed(() => {
        const schema = isProduction.value ? "https" : "http";
        return `${schema}://${config.public.apiHost}`;
    });

    const wsURL = computed(() => {
        const schema = isProduction.value ? "wss" : "ws";
        return `${schema}://${config.public.apiHost}`;
    });

    return {
        isProduction,
        isTest,
        baseURL,
        wsURL,
    };
};
