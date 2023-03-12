import { useGameStore } from "~/stores/useGameStore";
import { useFetch } from "#app";
import { components } from "~/schema";

export default defineNuxtRouteMiddleware(async (to) => {
    const { id } = to.params;
    const { setGame, game } = useGameStore();

    if (game?.id === id) return true;

    const { data, error } = await useFetch(
        `http://127.0.0.1:8000/api/game/${id}`,
        {
            method: "GET",
        }
    );
    if (!data.value || error.value) {
        return abortNavigation();
    }
    setGame(data.value as components["schemas"]["ShiritoriGame"]);
    return true;
});
