import { ref } from "vue";
import { toFormValidator } from "@vee-validate/zod";
import { useGameStore } from "~/stores/useGameStore";
import { navigateTo } from "@typed-router";
import { createGameSchema, gameSettingsSchema } from "~/schema";

export const useCreateGameForm = () => {
    const loading = ref(false);
    const { handleCreateGame } = useGameStore();
    const validationSchema = toFormValidator(createGameSchema);
    const initialValues = gameSettingsSchema.parse({});
    const onSubmit = async (values: createGameSchema) => {
        loading.value = true;
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
        } finally {
            loading.value = false;
        }
    };

    return { validationSchema, initialValues, onSubmit, loading };
};
