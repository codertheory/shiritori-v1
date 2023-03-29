import { z } from "zod";

export const getSubmitFn = <Schema extends z.ZodTypeAny>(
    _: Schema,
    // eslint-disable-next-line no-unused-vars
    callback: (data: z.infer<Schema>) => Promise<void>
) => {
    return (values: Record<string, any>) => {
        return callback(values);
    };
};
