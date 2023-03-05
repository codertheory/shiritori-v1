<template>
    <div>
        <NuxtLayout :name="currentLayout" />
    </div>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();

    const currentLayout = computed<string>(() => {
        switch (gameStore.game?.status) {
            case "WAITING":
                return "lobby";
            case "PLAYING":
                return "playing";
            default:
                return "lobby";
        }
    });

    definePageMeta({
        middleware: ["game-exists"],
        layout: false,
    });

    onMounted(() => {
        gameStore.joinGameWS();
    });
</script>

<style scoped></style>
