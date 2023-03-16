import { useFetch, useRequestHeaders } from "#imports";
import { components, paths } from "~/schema";
import { useConfig } from "~/composeables/useConfig";

type ApiPostOptions<T> = Parameters<typeof useFetch<T>>[1];

type useApiPost<T = unknown> = (
    // eslint-disable-next-line no-unused-vars
    url: keyof paths,
    // eslint-disable-next-line no-unused-vars
    options?: Omit<ApiPostOptions<T>, "method">
) => ReturnType<typeof useFetch>;

export const useApi = () => {
    const { baseURL, isProduction } = useConfig();

    const api: useApiPost = <R extends keyof paths, O>(
        url: R,
        options: ApiPostOptions<O> = {}
    ) => {
        return useFetch(url as unknown as string, {
            ...options,
            method: options.method || "POST",
            baseURL: options.baseURL || baseURL.value,
            credentials: "include",
            // eslint-disable-next-line no-undef
            headers: useRequestHeaders(["cookie"]) as HeadersInit,
            onRequestError({ error }) {
                // Handle the request errors
                console.error("onRequestError", error);
            },
        });
    };

    const apiSetCsrfToken = async () =>
        api("/api/set-csrf-cookie/", { method: "GET" });

    const apiGetGame = (gameId: string) =>
        api(`/api/game/${gameId}/`, {
            method: "GET",
            query: {
                format: "json",
            },
            // This only exists because of a bug that
            // locally this singular get function breaks
            baseURL: isProduction.value
                ? baseURL.value
                : "http://127.0.0.1:8000",
        });

    const apiCreateGame = (body: components["schemas"]["CreateGame"]) =>
        api("/api/game/", {
            body,
        });

    const apiTakeTurn = (
        gameId: string,
        body: components["schemas"]["ShiritoriTurn"]
    ) =>
        api(`/api/game/${gameId}/turn/`, {
            body,
        });

    const apiJoinGame = (
        gameId: string,
        body: Pick<components["schemas"]["ShiritoriPlayer"], "name">
    ) =>
        api(`/api/game/${gameId}/join/`, {
            body,
        });

    const apiLeaveGame = (gameId: string) =>
        api(`/api/game/${gameId}/leave/`, {});

    const apiStartGame = (gameId: string) =>
        api(`/api/game/${gameId}/start/`, {});

    return {
        apiSetCsrfToken,
        apiGetGame,
        apiCreateGame,
        apiTakeTurn,
        apiJoinGame,
        apiLeaveGame,
        apiStartGame,
    };
};
