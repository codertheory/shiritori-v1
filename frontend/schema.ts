import { z } from "zod";

export interface paths {
    "/api/game/": {
        get: operations["api_game_list"];
        post: operations["api_game_create"];
    };
    [key: `/api/game/${string}/`]: {
        get: operations["api_game_retrieve"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/join/`]: {
        post: operations["api_game_join_create"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/leave/`]: {
        post: operations["api_game_leave_create"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/start/`]: {
        post: operations["api_game_start_create"];
    };

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    [key: `/api/game/${string}/turn/`]: {
        post: operations["api_game_turn_create"];
    };
}

export interface components {
    schemas: {
        CreateGame: {
            settings: components["schemas"]["ShiritoriGameSettings"];
        };
        /** @enum {string} */
        LocaleEnum: "en";
        ShiritoriGame: {
            id: string;
            settings: components["schemas"]["ShiritoriGameSettings"];
            player_count: number;
            word_count: number;
            is_finished: boolean;
            winner: components["schemas"]["ShiritoriPlayer"];
            current_player: components["schemas"]["ShiritoriPlayer"];
            turn_time_left: number;
            words: readonly components["schemas"]["ShiritoriGameWord"][];
            players: readonly components["schemas"]["ShiritoriPlayer"][];
            /** Format: date-time */
            created_at: string;
            /** Format: date-time */
            updated_at: string;
            status?: components["schemas"]["StatusEnum"];
            current_turn?: number;
            last_word?: string;
        };
        ShiritoriGameSettings: {
            locale?: components["schemas"]["LocaleEnum"];
            word_length?: number;
            turn_time?: number;
            max_turns?: number;
        };
        ShiritoriGameWord: {
            word?: string;
            /** Format: double */
            score?: number;
            /** Format: double */
            duration?: number;
        };
        ShiritoriPlayer: {
            id: string;
            name: string;
            score: number;
        };
        ShiritoriTurn: {
            word: string;
            duration: number;
        };
        /** @enum {string} */
        StatusEnum: "WAITING" | "PLAYING" | "FINISHED";
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}

// export type external = Record<string, never>;

export interface operations {
    api_game_list: {
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriGame"][];
                };
            };
        };
    };
    api_game_create: {
        requestBody: {
            content: {
                "application/json": components["schemas"]["CreateGame"];
                "application/x-www-form-urlencoded": components["schemas"]["CreateGame"];
                "multipart/form-data": components["schemas"]["CreateGame"];
            };
        };
        responses: {
            201: {
                content: {
                    "application/json": components["schemas"]["ShiritoriGame"];
                };
            };
        };
    };
    api_game_retrieve: {
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
    api_game_join_create: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ShiritoriPlayer"];
                "application/x-www-form-urlencoded": components["schemas"]["ShiritoriPlayer"];
                "multipart/form-data": components["schemas"]["ShiritoriPlayer"];
            };
        };
        responses: {
            200: {
                content: {
                    "application/json": components["schemas"]["ShiritoriPlayer"];
                };
            };
        };
    };
    api_game_leave_create: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["ShiritoriGame"];
                "application/x-www-form-urlencoded": components["schemas"]["ShiritoriGame"];
                "multipart/form-data": components["schemas"]["ShiritoriGame"];
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
    api_game_start_create: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ShiritoriTurn"];
                "application/x-www-form-urlencoded": components["schemas"]["ShiritoriTurn"];
                "multipart/form-data": components["schemas"]["ShiritoriTurn"];
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
    api_game_turn_create: {
        parameters: {
            /** @description A unique value identifying this game. */
            path: {
                id: string;
            };
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ShiritoriTurn"];
                "application/x-www-form-urlencoded": components["schemas"]["ShiritoriTurn"];
                "multipart/form-data": components["schemas"]["ShiritoriTurn"];
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
}

export const gameSettingsSchema = z.object({
    locale: z.literal("en").default("en"),
    word_length: z.number().min(3).max(5).default(3),
    turn_time: z.number().min(30).max(120).default(60),
    max_turns: z.number().min(5).max(20).default(10),
});

export const createGameSchema = gameSettingsSchema.extend({
    username: z.string().min(3, "Username must be at least 3 characters long"),
});

export type createGameSchema = z.infer<typeof createGameSchema>;
