import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { components, createGameSchema } from "~/schema";
import { useSocketStore } from "~/stores/useSocketStore";
import { useApi } from "~/composeables/useApi";
import { Writeable } from "zod";

export const useGameStore = defineStore("game", () => {
    const { watchSocket } = useSocketStore();
    const {
        apiGameCreate,
        apiGameJoinCreate,
        apiGameStartCreate,
        apiCsrfCookieCreate,
        apiGameTurnCreate,
    } = useApi();
    const game = ref<components["schemas"]["ShiritoriGame"]>();
    const myId = ref<string>();
    const isJoining = ref<boolean | undefined>();

    const me = computed(() => {
        return game.value?.players?.find((p) => p.id === myId.value);
    });

    const players = computed(() => {
        return game.value?.players ?? [];
    });

    const words = computed(
        (): Writeable<components["schemas"]["ShiritoriGameWord"][]> => {
            return Object.assign([], game.value?.words ?? []);
        }
    );

    const isMyTurn = computed(() => {
        return me.value?.isCurrent ?? false;
    });

    const currentPlayer = computed(() => {
        return game.value?.players.find((p) => p.isCurrent);
    });

    const settings = computed(() => {
        return game.value?.settings ?? {};
    });

    const turnTimeLeft = computed(() => {
        return game.value?.turnTimeLeft ?? 0;
    });

    const lastWord = computed(() => {
        return game.value?.lastWord ?? "";
    });

    const lastLetter = computed(() => {
        if (!lastWord.value) {
            return "";
        }
        return lastWord.value[lastWord.value.length - 1];
    });

    const gameTurnDuration = computed(() => {
        return game.value?.settings.turnTime ?? 0;
    });

    const isHost = computed(() => {
        return me.value?.isHost ?? false;
    });

    const canStart = computed(() => {
        return isHost.value && players.value.length >= 2;
    });

    const winner = computed(() => {
        return players.value.find((p) => p.type === "WINNER");
    });

    const isPlayerCurrent = (playerId: string) => {
        return playerId === currentPlayer.value?.id;
    };

    const getPlayer = (playerId: string) => {
        return players.value.find((p) => p.id === playerId);
    };

    const createGame = async (
        settings: components["schemas"]["ShiritoriGameSettings"]
    ) => {
        const { data, error } = await apiGameCreate({}, { body: { settings } });
        if (error.value) {
            throw error.value;
        }
        return data.value;
    };

    const joinGame = async (
        gameId: string,
        player: Pick<components["schemas"]["ShiritoriPlayer"], "name">
    ) => {
        const { data, error } = await apiGameJoinCreate(
            { id: gameId },
            { body: player }
        );
        if (error.value) {
            throw error.value;
        }
        await apiCsrfCookieCreate();
        setIsJoining(false);
        joinGameWS(gameId);
        setMe(data.value!.id);
        return data;
    };

    const handleStartGame = async () => {
        const { data, error } = await apiGameStartCreate({
            id: game.value!.id,
        });
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

    const handleTakeTurn = async (word: string) => {
        const { data, error } = await apiGameTurnCreate(
            { id: game.value!.id },
            { body: { word } }
        );
        if (error.value) {
            throw error.value;
        }
        return data.value;
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

    const setIsJoining = (i: boolean | undefined) => {
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
                setMe(eventData.data.selfPlayer);
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
        currentPlayer,
        settings,
        turnTimeLeft,
        lastWord,
        lastLetter,
        gameTurnDuration,
        isHost,
        canStart,
        winner,
        isPlayerCurrent,
        getPlayer,
        createGame,
        joinGame,
        handleStartGame,
        handleCreateGame,
        handleTakeTurn,
        joinGameWS,
        setGame,
        setMe,
        setIsJoining,
    };
});
