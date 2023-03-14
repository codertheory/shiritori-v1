import { useGameStore } from "~/stores/useGameStore";
import { z } from "zod";
import { FetchError } from "ofetch";
import { SubmissionHandler } from "vee-validate";
import { ref } from "vue";

export const useGameTurnForm = () => {
    const isLoading = ref(false);
    const gameStore = useGameStore();
    const minWordLength = gameStore?.game?.settings?.wordLength || 3;
    const schema = z.object({
        word: z.string().min(minWordLength),
    });
    type schema = z.infer<typeof schema>;

    const wordValidation = (word: string) => {
        if (!word) return "Word is required";
        const lastWord = gameStore.lastWord;
        const lastWordLastChar = lastWord[lastWord.length - 1];
        const firstChar = word[0];
        const isLastWordLastChar = lastWordLastChar === firstChar;
        if (!isLastWordLastChar) {
            return "Word must start with the last letter of the last word";
        }
        const isWordLengthValid = word.length >= minWordLength;
        if (!isWordLengthValid) {
            return `Word must be at least ${minWordLength} characters long`;
        }
        return isLastWordLastChar && isWordLengthValid;
    };

    const validateWord = (value: string) => {
        const result = wordValidation(value);
        return {
            valid: result,
            result,
        };
    };

    const onSubmit: SubmissionHandler<schema> = async (
        values: schema,
        { setFieldError, setFieldValue }
    ) => {
        if (!values.word) return;
        isLoading.value = true;
        try {
            const { valid, result } = validateWord(values.word);
            if (!valid) return;
            if (typeof result === "string") {
                setFieldError("word", result);
                return;
            }
            await gameStore.handleTakeTurn(values.word);
            setFieldValue("word", "");
        } catch (e: FetchError | unknown) {
            if (e instanceof FetchError) {
                if (e?.data?.detail) {
                    setFieldError("word", e.data.detail);
                }
            }
        } finally {
            isLoading.value = false;
        }
    };

    return {
        isLoading,
        onSubmit,
        schema,
        validateWord,
    };
};
