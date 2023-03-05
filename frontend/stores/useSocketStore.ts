import { defineStore } from "pinia";
import { ref, watch, WatchCallback } from "vue";

export const useSocketStore = defineStore("socket", () => {
    const socket = ref<WebSocket | undefined>();

    const setSocket = (s: WebSocket | undefined) => {
        socket.value = s;
    };

    const connectToGameSocket = (gameId: string) => {
        if (!socket.value)
            setSocket(new WebSocket(`ws://127.0.0.1:8000/ws/game/${gameId}/`));
    };

    const disconnectFromGameSocket = () => {
        socket.value?.close();
        setSocket(undefined);
    };

    const watchSocket = (cb: WatchCallback<WebSocket | undefined>) => {
        watch(socket, cb);
    };

    return {
        socket,
        setSocket,
        connectToGameSocket,
        disconnectFromGameSocket,
        watchSocket,
    };
});
