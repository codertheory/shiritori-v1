import { gameSettingsSchema } from "~/schema";
import { toFormValidator } from "@vee-validate/zod";
import { useGameStore } from "~/stores/useGameStore";
import { getSubmitFn } from "~/utils/getSubmitFn";
export const useGameSettingsForm = () => {
    const validationSchema = toFormValidator(gameSettingsSchema);
    const gameStore = useGameStore();
    const initialValues = gameSettingsSchema.parse(gameStore?.settings ?? {});

    const onSubmit = getSubmitFn(gameSettingsSchema, async () => {
        await gameStore.handleStartGame();
    });

    return {
        validationSchema,
        initialValues,
        onSubmit,
    };
};
