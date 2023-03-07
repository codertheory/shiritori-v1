import { useApi } from "~/composeables/useApi";

export default defineNuxtRouteMiddleware(async (to, from) => {
    // skip middleware on server
    if (process.server) return;

    const { apiSetCsrfToken } = useApi();
    const cookie = useCookie("csrftoken");

    const fromSameRoute = from.fullPath === to.fullPath;
    const isGameroute = to.name === "game-id";

    if (fromSameRoute && isGameroute) return;

    if (!cookie.value) {
        await apiSetCsrfToken();
    }
});
