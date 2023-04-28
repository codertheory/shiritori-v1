import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { components, createGameSchema, gameSettingsSchema } from "~/schema";
import { useSocketStore } from "~/stores/useSocketStore";
import { useApi } from "~/composeables/useApi";
import { Writeable } from "zod";

export const useGameStore = defineStore("game", () => {
    const { watchSocket } = useSocketStore();
    const {
        apiGameCreate,
        apiGameJoinCreate,
        apiGameStartCreate,
        apiGameRestartCreate,
        apiCsrfCookieCreate,
        apiGameTurnCreate,
    } = useApi();
    const game = ref<components["schemas"]["ShiritoriGame"]>();
    const myId = ref<string>();
    const isJoining = ref<boolean | undefined>();
    const gameTurnTimeLeft = ref<number>(0);
    const initialSettings =
        ref<components["schemas"]["ShiritoriGameSettings"]>();

    const roomCode = computed(() => {
        return game.value?.id ?? "";
    });

    const me = computed(() => {
        return game.value?.players?.find((p) => p.id === myId.value);
    });

    const players = computed(() => {
        return game.value?.players ?? [];
    });

    const connectedPlayers = computed(() => {
        return players.value.filter((p) => p.isConnected);
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

    const isCurrentPlayerMe = computed(() => {
        return currentPlayer.value?.id == me.value?.id;
    });

    const settings = computed(() => {
        return game.value?.settings ?? gameSettingsSchema.parse({});
    });

    const currentRound = computed(() => {
        return game.value?.currentRound ?? 0;
    });

    const maxTurns = computed(() => {
        return game.value?.settings.maxTurns ?? 0;
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
        return isHost.value && connectedPlayers.value.length >= 2;
    });

    const winner = computed(() => {
        return players.value.find((p) => p.type === "WINNER");
    });

    const leaderboard = computed(() => {
        return [...players.value].sort((a, b) => b.score - a.score);
    });

    const isPlayerCurrent = (playerId: string) => {
        return playerId === currentPlayer.value?.id;
    };

    const getPlayer = (playerId: string) => {
        return players.value.find((p) => p.id === playerId);
    };

    const getPlayerIndex = (playerId: string) => {
        return players.value.findIndex((p) => p.id === playerId);
    };

    const setPlayerConnected = (playerId: string, connected: boolean) => {
        const playerIndex = getPlayerIndex(playerId);
        if (playerIndex !== -1) {
            const player = game.value?.players[playerIndex];
            if (player) {
                player.isConnected = connected;
            }
        }
    };

    const getPlayerWords = (playerId: string) => {
        return words.value.filter((w) => w.playerId === playerId);
    };

    const addPlayer = (player: components["schemas"]["ShiritoriPlayer"]) => {
        if (!game.value) {
            return;
        }
        if (!game.value.players) {
            game.value.players = [];
        }
        game.value.players.push(player);
    };

    const removePlayer = (playerId: string) => {
        const playerIndex = getPlayerIndex(playerId);
        if (playerIndex !== -1) {
            game.value!.players.splice(playerIndex, 1);
        }
    };

    const updatePlayer = (player: components["schemas"]["ShiritoriPlayer"]) => {
        const playerIndex = getPlayerIndex(player.id);
        if (playerIndex !== -1) {
            game.value!.players[playerIndex] = player;
        }
    };

    const addWord = (word: components["schemas"]["ShiritoriGameWord"]) => {
        game.value!.words.push(word);
        const player = getPlayer(word.playerId);
        if (player) {
            player.score += word.score;
        }
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

    const handleStartGame = async (
        settings: components["schemas"]["ShiritoriGameSettings"]
    ) => {
        gameTurnTimeLeft.value = settings.turnTime;
        const { data, error } = await apiGameStartCreate(
            {
                id: game.value!.id,
            },
            { body: { settings } }
        );
        if (error.value) {
            throw error.value;
        }
        return data.value;
    };

    const handleRestartGame = async () => {
        await apiGameRestartCreate({ id: game.value!.id });
    };

    const handleCreateGame = async (data: createGameSchema) => {
        const { username, ...rest } = data;
        const game = await createGame(rest);
        if (game) {
            await joinGame(game.id, { name: username });
            initialSettings.value = game.settings;
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
        setTurnTimeLeft(g.turnTimeLeft);
    };

    const setMe = (m: string) => {
        myId.value = m;
    };

    const setIsJoining = (i: boolean | undefined) => {
        isJoining.value = i;
    };

    const setTurnTimeLeft = (t: number) => {
        if (t) {
            gameTurnTimeLeft.value = t;
        }
    };

    const onSocketEvent = (e: MessageEvent) => {
        const eventData = JSON.parse(e.data);
        switch (eventData.type) {
            case "game_updated":
                setGame(eventData.data);
                break;
            case "game_timer_updated":
                setTurnTimeLeft(eventData.data);
                break;
            case "connected":
                setGame(eventData.data.game);
                setMe(eventData.data.selfPlayer);
                break;
            case "player_connected":
                setPlayerConnected(eventData.data.playerId, true);
                break;
            case "player_disconnected":
                setPlayerConnected(eventData.data.playerId, false);
                break;
            case "player_joined":
                addPlayer(eventData.data);
                break;
            case "player_left":
                removePlayer(eventData.data);
                break;
            case "player_updated":
                updatePlayer(eventData.data);
                break;
            case "turn_taken":
                addWord(eventData.data);
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
        roomCode,
        me,
        isJoining,
        players,
        words,
        isMyTurn,
        currentPlayer,
        isCurrentPlayerMe,
        settings,
        currentRound,
        maxTurns,
        gameTurnTimeLeft,
        initialSettings,
        lastWord,
        lastLetter,
        gameTurnDuration,
        isHost,
        canStart,
        winner,
        leaderboard,
        isPlayerCurrent,
        getPlayer,
        getPlayerWords,
        createGame,
        joinGame,
        handleStartGame,
        handleRestartGame,
        handleCreateGame,
        handleTakeTurn,
        joinGameWS,
        setGame,
        setMe,
        setIsJoining,
    };
});
