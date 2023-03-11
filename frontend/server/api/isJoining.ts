export default defineEventHandler((event) => {
    const sessionid = getCookie(event, "sessionid");
    return {
        result: !(sessionid !== undefined),
    };
});
