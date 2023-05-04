import { toTypedSchema } from "@vee-validate/zod";
import { useGameStore } from "~/stores/useGameStore";
import { navigateTo } from "@typed-router";
import { createGameSchema, gameSettingsSchema } from "~/schema";
import { getSubmitFn } from "~/utils/getSubmitFn";

export const useCreateGameForm = () => {
    const { handleCreateGame } = useGameStore();
    const validationSchema = toTypedSchema(createGameSchema);
    const initialValues = gameSettingsSchema.parse({});
    const onSubmit = getSubmitFn(createGameSchema, async (values) => {
        try {
            const game = await handleCreateGame(values);
            await navigateTo(
                {
                    name: "game-id",
                    params: { id: game!.id },
                },
                { replace: true }
            );
        } catch (e) {
            console.error(e);
        }
    });

    return { validationSchema, initialValues, onSubmit };
};
