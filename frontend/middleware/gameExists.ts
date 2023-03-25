import { useGameStore } from "~/stores/useGameStore";
import { components } from "~/schema";
import { useApi } from "~/composeables/useApi";

export default defineNuxtRouteMiddleware(async (to) => {
    const { id } = to.params;
    const { setGame, game } = useGameStore();
    const { apiGameRetrieve } = useApi();

    if (game?.id === id) return true;

    const { data, error } = await apiGameRetrieve({ id: id as string });
    if (!data.value || error.value) {
        return abortNavigation();
    }
    setGame(data.value as components["schemas"]["ShiritoriGame"]);
    return true;
});
