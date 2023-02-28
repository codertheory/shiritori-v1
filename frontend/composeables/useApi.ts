import { useFetch } from "#imports";
import { components, paths } from "~/schema";

const BASE_URL = "http://localhost:8000";

type ApiPostUrl = keyof paths;
type ApiPostOptions<T> = Parameters<typeof useFetch<T>>[1];

type useApiPost<T = unknown> = (
  url: ApiPostUrl,
  options: ApiPostOptions<T>
) => ReturnType<typeof useFetch<T>>;

export const useApi = () => {
  const post: useApiPost = (url, options) => {
    return useFetch(url, { ...options, baseURL: BASE_URL, method: "POST" });
  };

  const createGame = (body: components["schemas"]["CreateGame"]) =>
    post("/api/game/", {
      body: {
        settings: {
          locale: "en",
          word_length: 5,
          turn_time: 30,
          max_turns: 10,
        },
      } as components["schemas"]["CreateGame"],
    });

  return { createGame };
};
