<template>
    <div>
        <NuxtLayout :name="currentLayout" />
    </div>
</template>

<script setup lang="ts">
    import { useRoute } from "vue-router";
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
    const result = await useFetch("/api/isJoining");
    gameStore.setIsJoining(result.data?.value?.result);
    const route = useRoute();

    const currentLayout = computed<string>(() => {
        if (gameStore.isJoining) {
            return "joining";
        }
        switch (gameStore.game?.status) {
            case "WAITING":
                return "lobby";
            case "PLAYING":
                return "playing";
            case "FINISHED":
                return "finished";
            default:
                return "lobby";
        }
    });

    definePageMeta({
        middleware: ["game-exists"],
        layout: false,
    });

    onMounted(() => {
        if (!gameStore.isJoining) {
            gameStore.joinGameWS(route.params.id as string);
        }
    });
</script>

<style scoped></style>
