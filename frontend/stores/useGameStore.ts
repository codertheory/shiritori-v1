import { ref } from "vue";
import { defineStore } from "pinia";
import { components } from "~/schema";
import { useSocketStore } from "~/stores/useSocketStore";

export const useGameStore = defineStore("game", () => {
    const game = ref<components["schemas"]["ShiritoriGame"]>();
    const me = ref<components["schemas"]["ShiritoriPlayer"]>();
    const { watchSocket } = useSocketStore();
    const setGame = (g: components["schemas"]["ShiritoriGame"]) => {
        game.value = g;
    };

    const setMe = (m: components["schemas"]["ShiritoriPlayer"]) => {
        me.value = m;
    };

    const onSocketEvent = (e: MessageEvent) => {
        const data = JSON.parse(e.data);
        console.log(data);
    };

    watchSocket((s) => {
        if (s) {
            s.onmessage = onSocketEvent;
        }
    });

    return {
        game,
        setGame,
        me,
        setMe,
    };
});
