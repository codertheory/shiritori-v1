import { z } from "zod";

export interface paths {
    "/api/game/": {
        get: operations["apiGameList"];
        post: operations["apiGameCreate"];
    };

    [key: `/api/game/${string}/`]: {
        get: operations["apiGameRetrieve"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/join/`]: {
        post: operations["apiGameJoinCreate"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/leave/`]: {
        post: operations["apiGameLeaveCreate"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/start/`]: {
        post: operations["apiGameStartCreate"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/turn/`]: {
        post: operations["apiGameTurnCreate"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    "/api/set-csrf-cookie/": {
        get: operations["apiCsrfCookieCreate"];
    };
}

export interface components {
    schemas: {
        CreateGame: {
            settings: components["schemas"]["ShiritoriGameSettings"];
        };
        JoinGame: {
            name: string;
        };
        Player: {
            id: string;
        };
        ShiritoriGame: {
            id: string;
            settings: components["schemas"]["ShiritoriGameSettings"];
            playerCount: number;
            wordCount: number;
            isFinished: boolean;
            winner: string;
            currentPlayer: string;
            turnTimeLeft: number;
            words: readonly components["schemas"]["ShiritoriGameWord"][];
            players: readonly components["schemas"]["ShiritoriPlayer"][];
            /** Format: date-time */
            createdAt: string;
            /** Format: date-time */
            updatedAt: string;
            /**
             * @description * `WAITING` - Waiting
             * * `PLAYING` - Playing
             * * `FINISHED` - Finished
             * @enum {string}
             */
            status?: "WAITING" | "PLAYING" | "FINISHED";
            currentTurn?: number;
            lastWord?: string | null;
        };
        ShiritoriGameSettings: {
            /**
             * @description * `en` - English
             * @enum {string}
             */
            locale?: "en";
            wordLength?: number;
            turnTime?: number;
            maxTurns?: number;
        };
        ShiritoriGameWord: {
            word?: string | null;
            /** Format: double */
            score: number;
            /** Format: double */
            duration: number;
            playerId: string;
        };
        ShiritoriPlayer: {
            id: string;
            name: string;
            score: number;
            /**
             * @description * `HUMAN` - human
             * * `BOT` - bot
             * * `SPECTATOR` - spectator
             * * `WINNER` - winner
             * @enum {string}
             */
            type?: "HUMAN" | "BOT" | "SPECTATOR" | "WINNER";
            isCurrent?: boolean;
            isHost?: boolean;
        };
        ShiritoriTurn: {
            word: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}

// export type external = Record<string, never>;

export interface operations {
    apiGameList: {
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriGame"][];
                };
            };
        };
    };
    apiGameCreate: {
        requestBody: {
            content: {
                "application/json": components["schemas"]["CreateGame"];
            };
        };
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriGame"];
                };
            };
        };
    };
    apiGameRetrieve: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriGame"];
                };
            };
        };
    };
    apiGameJoinCreate: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["JoinGame"];
            };
        };
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["Player"];
                };
            };
        };
    };
    apiGameLeaveCreate: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        responses: {
            /** @description No response body */
            200: never;
        };
    };
    apiGameStartCreate: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ShiritoriTurn"];
            };
        };
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriTurn"];
                };
            };
        };
    };
    apiGameTurnCreate: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ShiritoriTurn"];
            };
        };
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriTurn"];
                };
            };
        };
    };
    apiCsrfCookieCreate: {
        responses: {
            200: {
                content: {
                    "application/json": { details: string };
                };
            };
        };
    };
}

export const gameSettingsSchema = z.object({
    locale: z.literal("en").default("en"),
    word_length: z.number().min(3).max(5).default(3),
    turn_time: z.number().min(5).max(60).default(60),
    max_turns: z.number().min(5).max(20).default(10),
});

export const usernameSchema = z
    .string()
    .min(3, "Username must be at least 3 characters long");

export const createGameSchema = gameSettingsSchema.extend({
    username: usernameSchema,
});

export const joinGameSchema = z.object({
    username: usernameSchema,
});

export type createGameSchema = z.infer<typeof createGameSchema>;
export type gameSettingsSchema = z.infer<typeof gameSettingsSchema>;
export type usernameSchema = z.infer<typeof usernameSchema>;
