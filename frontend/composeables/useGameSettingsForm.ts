import { ref } from "vue";
import { gameSettingsSchema } from "~/schema";
import { toFormValidator } from "@vee-validate/zod";
import { useGameStore } from "~/stores/useGameStore";
import { getSubmitFn } from "~/utils/getSubmitFn";

export const useGameSettingsForm = () => {
    const validationSchema = toFormValidator(gameSettingsSchema);
    const gameStore = useGameStore();
    const initialValues = ref(
        gameSettingsSchema.parse(gameStore.initialSettings ?? {})
    );

    const onSubmit = getSubmitFn(gameSettingsSchema, async (settings) => {
        await gameStore.handleStartGame(settings);
    });

    return {
        validationSchema,
        initialValues,
        onSubmit,
    };
};
