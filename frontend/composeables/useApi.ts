import { useFetch } from "#imports";
import { components, paths } from "~/schema";

const BASE_URL = "http://localhost:8000";

type ApiPostOptions<T> = Parameters<typeof useFetch<T>>[1];

type useApiPost<T = unknown> = (
  url: keyof paths,
  options: ApiPostOptions<T>
) => ReturnType<typeof useFetch>;

export const useApi = () => {
  const post: useApiPost = <R extends keyof paths, O>(
    url: R,
    options: ApiPostOptions<O>
  ) => {
    return useFetch(url as unknown as string, {
      ...options,
      baseURL: BASE_URL,
      method: "POST",
    });
  };

  const createGame = (body: components["schemas"]["CreateGame"]) =>
    post("/api/game/", {
      body,
    });

  const takeTurn = (
    gameId: string,
    body: components["schemas"]["ShiritoriTurn"]
  ) =>
    post(`/api/game/${gameId}/turn/`, {
      body,
    });

  const joinGame = (
    gameId: string,
    body: Pick<components["schemas"]["ShiritoriPlayer"], "name">
  ) =>
    post(`/api/game/${gameId}/join/`, {
      body,
    });

  const leaveGame = (gameId: string) => post(`/api/game/${gameId}/leave/`, {});

  const startGame = (gameId: string) => post(`/api/game/${gameId}/start/`, {});

  return { createGame, takeTurn, joinGame, leaveGame, startGame };
};
