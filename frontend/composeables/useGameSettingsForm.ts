import { gameSettingsSchema } from "~/schema";
import { toFormValidator } from "@vee-validate/zod";
import { useGameStore } from "~/stores/useGameStore";

export const useGameSettingsForm = () => {
    const validationSchema = toFormValidator(gameSettingsSchema);
    const gameStore = useGameStore();
    const initialValues = gameSettingsSchema.parse(gameStore?.settings ?? {});

    const onSubmit = getSubmitFn(gameSettingsSchema, async (values) => {
        // TODO: Implement this
    });

    return {
        validationSchema,
        initialValues,
        onSubmit,
    };
};
