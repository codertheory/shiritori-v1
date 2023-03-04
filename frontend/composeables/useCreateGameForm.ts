import { ref } from "vue";
import { z } from "zod";
import { toFormValidator } from "@vee-validate/zod";
import { useApi } from "~/composeables/useApi";
import { useGameStore } from "~/stores/useGameStore";
import { navigateTo } from "@typed-router";
import { useSocketStore } from "~/stores/useSocketStore";

const gameSettingsSchema = z.object({
    locale: z.literal("en").default("en"),
    word_length: z.number().min(3).max(5).default(3),
    turn_time: z.number().min(30).max(120).default(60),
    max_turns: z.number().min(5).max(20).default(10),
});

const createGameSchema = gameSettingsSchema.extend({
    username: z.string().min(3, "Username must be at least 3 characters long"),
});

type createGameSchema = z.infer<typeof createGameSchema>;
export const useCreateGameForm = () => {
    const loading = ref(false);
    const { createGame, joinGame } = useApi();
    const { setGame, setMe } = useGameStore();
    const { connectToGameSocket } = useSocketStore();
    const validationSchema = toFormValidator(createGameSchema);
    const initialValues = gameSettingsSchema.parse({});
    const onSubmit = async (values: createGameSchema) => {
        loading.value = true;
        try {
            const { username, ...rest } = values;
            const { data: gameData } = await createGame({ settings: rest });
            if (gameData) {
                const { data: playerData } = await joinGame(gameData.value.id, {
                    name: username,
                });
                if (playerData) {
                    setGame(gameData.value);
                    setMe(playerData.value);
                    await navigateTo({
                        name: "game-id",
                        params: { id: gameData.value.id },
                        replace: true,
                    });
                    connectToGameSocket(gameData.value.id);
                }
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    return { validationSchema, initialValues, onSubmit, loading };
};
