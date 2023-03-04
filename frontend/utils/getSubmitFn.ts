import { z } from "zod";

export const getSubmitFn = <Schema extends z.ZodTypeAny>(
    _: Schema,
    callback: (data: z.infer<Schema>) => Promise<void>
) => {
    return (values: Record<string, any>) => {
        return callback(values);
    };
};
