import { useApi } from "~/composeables/useApi";
import { useGameStore } from "~/stores/useGameStore";

export default defineNuxtRouteMiddleware(async (to) => {
    const { id } = to.params;
    const { apiGetGame } = useApi();
    const { setGame, game } = useGameStore();

    if (game?.id === id) return true;

    const { data, error } = await apiGetGame(id as string);
    if (!data.value || error.value) {
        return abortNavigation();
    }
    setGame(data.value);
    return true;
});
