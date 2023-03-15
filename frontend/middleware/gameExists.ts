import { useGameStore } from "~/stores/useGameStore";
import { useFetch } from "#app";
import { components } from "~/schema";
import { useConfig } from "~/composeables/useConfig";

export default defineNuxtRouteMiddleware(async (to) => {
    const { id } = to.params;
    const { setGame, game } = useGameStore();
    const { baseURL } = useConfig();

    if (game?.id === id) return true;

    const { data, error } = await useFetch(`/api/game/${id}`, {
        method: "GET",
        baseURL,
    });
    if (!data.value || error.value) {
        return abortNavigation();
    }
    setGame(data.value as components["schemas"]["ShiritoriGame"]);
    return true;
});
