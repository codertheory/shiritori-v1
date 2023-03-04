import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { components, createGameSchema } from "~/schema";
import { useSocketStore } from "~/stores/useSocketStore";
import { useApi } from "~/composeables/useApi";

export const useGameStore = defineStore("game", () => {
    const { watchSocket } = useSocketStore();
    const { apiCreateGame, apiJoinGame, apiStartGame } = useApi();
    const game = ref<components["schemas"]["ShiritoriGame"]>();
    const me = ref<components["schemas"]["ShiritoriPlayer"]>();

    const players = computed(() => {
        return game.value?.players ?? [];
    });

    const words = computed(() => {
        return game.value?.words ?? [];
    });

    const isMyTurn = computed(() => {
        // TODO: Implement this
        return undefined;
    });

    const createGame = async (
        settings: components["schemas"]["ShiritoriGameSettings"]
    ) => {
        const { data, error } = await apiCreateGame({ settings });
        if (error.value) {
            throw error.value;
        }
        return data.value;
    };

    const joinGame = async (
        gameId: string,
        player: Pick<components["schemas"]["ShiritoriPlayer"], "name">
    ) => {
        const { data, error } = await apiJoinGame(gameId, player);
        if (error.value) {
            throw error.value;
        }
        return data.value;
    };

    const startGame = async () => {
        const { data, error } = await apiStartGame(game.value!.id);
        if (error.value) {
            throw error.value;
        }
        return data.value;
    };

    const handleCreateGame = async (data: createGameSchema) => {
        const { username, ...rest } = data;
        const game = await createGame(rest);
        if (game) {
            const { connectToGameSocket } = useSocketStore();
            const player = await joinGame(game.id, { name: username });
            if (player) {
                setGame(game);
                setMe(player);
                connectToGameSocket(game.id);
            }
            return game;
        }
    };

    const joinGameWS = () => {
        const { connectToGameSocket } = useSocketStore();
        connectToGameSocket(game.value!.id);
    };

    const setGame = (g: components["schemas"]["ShiritoriGame"]) => {
        game.value = g;
    };

    const setMe = (m: components["schemas"]["ShiritoriPlayer"]) => {
        me.value = m;
    };

    const onSocketEvent = (e: MessageEvent) => {
        const data = JSON.parse(e.data);
        console.error(data);
    };

    watchSocket((s) => {
        if (s) {
            s.onmessage = onSocketEvent;
        }
    });

    return {
        game,
        me,
        players,
        words,
        isMyTurn,
        createGame,
        joinGame,
        startGame,
        handleCreateGame,
        joinGameWS,
        setGame,
        setMe,
    };
});
