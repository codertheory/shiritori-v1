import { useRoute } from "#imports";
import { toFormValidator } from "@vee-validate/zod";
import { joinGameSchema } from "~/schema";
import { useGameStore } from "~/stores/useGameStore";
import { getSubmitFn } from "~/utils/getSubmitFn";

export const useJoinGameForm = () => {
    const validationSchema = toFormValidator(joinGameSchema);
    const gameStore = useGameStore();

    const onSubmit = getSubmitFn(joinGameSchema, async (values) => {
        console.log("onSubmit", values);
        const route = useRoute();
        const id = route.params.id;
        if (!id) throw new Error("No game id found");
        await gameStore.joinGame(id as string, {
            name: values.username,
        });
    });

    return {
        validationSchema,
        onSubmit,
    };
};
