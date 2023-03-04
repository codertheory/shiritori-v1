<template>
    <div>
        <NuxtLayout />
    </div>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    definePageMeta({
        middleware: ["game-exists"],
        layout: "lobby",
    });

    const { joinGameWS } = useGameStore();

    onMounted(() => {
        joinGameWS();
    });
</script>

<style scoped></style>
