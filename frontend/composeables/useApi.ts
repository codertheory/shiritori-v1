import { useFetch } from "#imports";
import { components, paths } from "~/schema";
import { NitroFetchOptions } from "nitropack";

const BASE_URL = "http://0.0.0.0:8000";

type ApiPostOptions<T> = Parameters<typeof useFetch<T>>[1];

type useApiPost<T = unknown> = (
    url: keyof paths,
    options?: Omit<ApiPostOptions<T>, "method">,
    method?: NitroFetchOptions<string>["method"]
) => ReturnType<typeof useFetch>;

export const useApi = () => {
    const api: useApiPost = <R extends keyof paths, O>(
        url: R,
        options: ApiPostOptions<O> = {},
        method: NitroFetchOptions<string>["method"] = "POST"
    ) => {
        return useFetch(url as unknown as string, {
            ...options,
            baseURL: BASE_URL,
            method,
            onRequestError({ request, options, error }) {
                // Handle the request errors
                console.log("onRequestError", request, options, error);
            },
        });
    };

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
        apiGetGame,
        apiCreateGame,
        apiTakeTurn,
        apiJoinGame,
        apiLeaveGame,
        apiStartGame,
    };
};
