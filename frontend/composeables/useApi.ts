import { useFetch, useRequestHeaders } from "#imports";
import { components, paths } from "~/schema";
import { NitroFetchOptions } from "nitropack";
import { useConfig } from "~/composeables/useConfig";

type ApiPostOptions<T> = Parameters<typeof useFetch<T>>[1];

type useApiPost<T = unknown> = (
    // eslint-disable-next-line no-unused-vars
    url: keyof paths,
    // eslint-disable-next-line no-unused-vars
    options?: Omit<ApiPostOptions<T>, "method">,
    // eslint-disable-next-line no-unused-vars
    method?: NitroFetchOptions<string>["method"]
) => ReturnType<typeof useFetch>;

export const useApi = () => {
    const { baseURL } = useConfig();

    const api: useApiPost = <R extends keyof paths, O>(
        url: R,
        options: ApiPostOptions<O> = {},
        method: NitroFetchOptions<string>["method"] = "POST"
    ) => {
        return useFetch(url as unknown as string, {
            ...options,
            method,
            baseURL,
            credentials: "include",
            // eslint-disable-next-line no-undef
            headers: useRequestHeaders(["cookie"]) as HeadersInit,
            onRequestError({ error }) {
                // Handle the request errors
                console.error("onRequestError", error);
            },
        });
    };

    const apiSetCsrfToken = async () => api("/api/set-csrf-cookie/", {}, "GET");

    const apiGetGame = (gameId: string) =>
        api(
            `/api/game/${gameId}/`,
            {
                query: {
                    format: "json",
                },
            },
            "GET"
        );

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
