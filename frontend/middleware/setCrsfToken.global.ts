import { useApi } from "~/composeables/useApi";

export default defineNuxtRouteMiddleware((to, from) => {
    // skip middleware on server
    if (process.server) return;

    const { apiSetCsrfToken } = useApi();
    const cookie = useCookie("csrftoken");
    if (!cookie.value) {
        apiSetCsrfToken().then();
    }
});
