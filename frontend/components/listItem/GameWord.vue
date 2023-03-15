<template>
    <Timeline :value="gameStore.words">
        <template #opposite="slotProps">
            <span class="font-bold text-primary">{{
                getPlayerName(slotProps.item)
            }}</span>
        </template>
        <template #marker="slotProps">
            <Badge :value="slotProps.item.score" />
        </template>
        <template #content="slotProps">
            {{ slotProps.item.word ?? "No word" }}
        </template>
    </Timeline>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";
    import { components } from "~/schema";

    const gameStore = useGameStore();

    const getPlayerName = (word: components["schemas"]["ShiritoriGameWord"]) =>
        gameStore.getPlayer(word.playerId)?.name;
</script>

<style scoped></style>
