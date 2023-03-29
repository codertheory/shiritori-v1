import { defineEventHandler, getCookie } from "h3";

export default defineEventHandler((event) => {
    const sessionid = getCookie(event, "sessionid");
    return {
        result: !(sessionid !== undefined),
    };
});
