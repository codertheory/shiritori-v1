import { z } from "zod";
import { toFormValidator } from "@vee-validate/zod";

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
  const validationSchema = toFormValidator(createGameSchema);
  const initialValues = gameSettingsSchema.parse({});
  const onSubmit = async (values: createGameSchema) => {
    console.log("onSubmit", values);
  };

  return { validationSchema, initialValues, onSubmit };
};
