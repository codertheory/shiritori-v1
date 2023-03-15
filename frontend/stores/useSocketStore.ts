import { defineStore } from "pinia";
import { ref, watch, WatchCallback } from "vue";
import { useConfig } from "~/composeables/useConfig";

export const useSocketStore = defineStore("socket", () => {
    const socket = ref<WebSocket | undefined>();
    const { wsURL } = useConfig();

    const isConnected = computed(() => {
        return socket.value?.readyState === WebSocket.OPEN;
    });

    const setSocket = (s: WebSocket | undefined) => {
        socket.value = s;
    };

    const connectToGameSocket = (
        gameId: string,
        reconnect: boolean = false
    ) => {
        if (!socket.value && !isConnected.value && gameId && !reconnect)
            setSocket(new WebSocket(`${wsURL.value}/ws/game/${gameId}/`));
        if (reconnect && socket.value && !isConnected.value) {
            socket.value?.close(1000);
            setSocket(new WebSocket(`${wsURL.value}/ws/game/${gameId}/`));
        }
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
        isConnected,
        setSocket,
        connectToGameSocket,
        disconnectFromGameSocket,
        watchSocket,
    };
});
