import { useApi } from "~/composeables/useApi";
import { useGameStore } from "~/stores/useGameStore";

export default defineNuxtRouteMiddleware(async (to, from) => {
    const { id } = to.params;
    const { getGame } = useApi();
    const { setGame } = useGameStore();
    const { data, error } = await getGame(id as string);
    if (!data.value || error.value) {
        return abortNavigation();
    }
    setGame(data.value);
    return true;
});
