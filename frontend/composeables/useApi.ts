import { useFetch, useRequestHeaders } from "#imports";
import { operations, paths } from "~/schema";
import { useConfig } from "~/composeables/useConfig";
import { HTTPMethod } from "h3";
import { FetchOptions } from "ofetch";

export type apiPath = keyof paths;
export type apiUseFetchResponse<T> = Promise<ReturnType<typeof useFetch<T>>>;

export type operationPathParameters<key extends keyof operations> =
    // @ts-ignore
    operations[key]["parameters"]["path"];
export type operationResponse<key extends keyof operations> =
    // @ts-ignore
    operations[key]["responses"][200]["content"]["application/json"];
export type operationRequestBody<key extends keyof operations> =
    // @ts-ignore
    operations[key]["requestBody"]["content"]["application/json"];
export type apiUseFetchOptions<key extends keyof operations> =
    FetchOptions<"json"> & {
        body?: operationRequestBody<key>;
    };

export type client = {
    [key in keyof operations]: (
        // eslint-disable-next-line no-unused-vars
        pathParameters?: operationPathParameters<key>,
        // eslint-disable-next-line no-unused-vars
        options?: apiUseFetchOptions<key>
    ) => apiUseFetchResponse<operationResponse<key>>;
};

export const useApi = () => {
    const { baseURL, isProduction } = useConfig();

    const useApiFetch = async <key extends keyof operations>(
        path: apiPath,
        method: HTTPMethod,
        options?: apiUseFetchOptions<key>
    ): apiUseFetchResponse<operationResponse<key>> => {
        return useFetch(path, {
            ...(options || {}),
            method,
            body: options?.body,
            baseURL: options?.baseURL || baseURL.value,
            credentials: "include",
            // eslint-disable-next-line no-undef
            headers: useRequestHeaders(["cookie"]) as HeadersInit,
            onRequestError({ error }) {
                // Handle the request errors
                console.error("onRequestError", error);
            },
        });
    };
    const api = <client>{
        apiGameList: async (pathParameters, options) => {
            return useApiFetch("/api/game/", "GET", options);
        },
        apiGameCreate: async (pathParameters, options = {}) => {
            return useApiFetch("/api/game/", "POST", options);
        },
        apiGameTurnCreate: async (pathParameters, options) => {
            return useApiFetch(
                `/api/game/${pathParameters?.id}/turn/`,
                "POST",
                options
            );
        },
        apiGameRetrieve: async (pathParameters, options) => {
            return useApiFetch(`/api/game/${pathParameters?.id}/`, "GET", {
                ...options,
                // This only exists because of a bug that
                // locally this singular get function breaks
                baseURL: isProduction.value
                    ? baseURL.value
                    : "http://127.0.0.1:8000",
            });
        },
        apiGameJoinCreate: async (pathParameters, options) => {
            return useApiFetch(
                `/api/game/${pathParameters?.id}/join/`,
                "POST",
                options
            );
        },
        apiGameLeaveCreate: async (pathParameters, options) => {
            return useApiFetch(
                `/api/game/${pathParameters?.id}/leave/`,
                "POST",
                options
            );
        },
        apiGameStartCreate: async (pathParameters, options) => {
            return useApiFetch(
                `/api/game/${pathParameters?.id}/start/`,
                "POST",
                options
            );
        },
        apiCsrfCookieCreate: async (pathParameters?, options?) => {
            return useApiFetch("/api/set-csrf-cookie/", "GET", options);
        },
    };

    return {
        ...api,
    };
};
