import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { components, createGameSchema } from "~/schema";
import { useSocketStore } from "~/stores/useSocketStore";
import { useApi } from "~/composeables/useApi";

export const useGameStore = defineStore("game", () => {
    const { watchSocket } = useSocketStore();
    const { apiCreateGame, apiJoinGame, apiStartGame, apiSetCsrfToken } =
        useApi();
    const game = ref<components["schemas"]["ShiritoriGame"]>();
    const myId = ref<string>();
    const isJoining = ref<boolean>(false);

    const me = computed(() => {
        return game.value?.players.find((p) => p.id === myId.value);
    });

    const players = computed(() => {
        return game.value?.players ?? [];
    });

    const words = computed(() => {
        return game.value?.words ?? [];
    });

    const isMyTurn = computed(() => {
        return game.value?.current_player === myId.value;
    });

    const settings = computed(() => {
        return game.value?.settings ?? {};
    });

    const turnTimeLeft = computed(() => {
        return game.value?.turn_time_left ?? 0;
    });

    const lastWord = computed(() => {
        return game.value?.last_word ?? "";
    });

    const gameTurnDuration = computed(() => {
        return game.value?.settings.turn_time ?? 0;
    });

    const isHost = computed(() => {
        return me.value?.type === "HOST";
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
        await apiSetCsrfToken();
        setIsJoining(false);
        joinGameWS(gameId);
        setMe(data.value.id);
        return data;
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
            await joinGame(game.id, { name: username });
            return game;
        }
    };

    const joinGameWS = (gameId: string | undefined) => {
        const { connectToGameSocket } = useSocketStore();
        connectToGameSocket(gameId ?? game.value!.id);
    };

    const setGame = (g: components["schemas"]["ShiritoriGame"]) => {
        game.value = g;
    };

    const setMe = (m: string) => {
        myId.value = m;
    };

    const setIsJoining = (i: boolean) => {
        isJoining.value = i;
    };

    const onSocketEvent = (e: MessageEvent) => {
        const eventData = JSON.parse(e.data);
        switch (eventData.type) {
            case "game_updated":
                setGame(eventData.data);
                break;
            case "connected":
                setGame(eventData.data.game);
                setMe(eventData.data.self_player);
                break;
            default:
                break;
        }
    };

    watchSocket((s) => {
        if (s) {
            s.onmessage = onSocketEvent;
        }
    });

    return {
        game,
        myId,
        me,
        isJoining,
        players,
        words,
        isMyTurn,
        settings,
        turnTimeLeft,
        lastWord,
        gameTurnDuration,
        isHost,
        createGame,
        joinGame,
        startGame,
        handleCreateGame,
        joinGameWS,
        setGame,
        setMe,
        setIsJoining,
    };
});
