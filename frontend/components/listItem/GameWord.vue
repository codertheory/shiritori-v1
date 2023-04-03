<template>
    <Timeline :value="gameStore.words">
        <template #opposite="slotProps">
            <div
                class="flex flex-row justify-content-start align-items-end pt-sm"
            >
                <span class="font-bold text-primary">{{
                    getPlayerName(slotProps.item)
                }}</span>
            </div>
        </template>
        <template #marker="slotProps">
            <div
                class="flex flex-row justify-content-center align-items-center"
            >
                <Badge :value="slotProps.item.score" />
            </div>
        </template>
        <template #content="slotProps">
            <div
                class="flex flex-row justify-content-center align-items-end pt-sm"
            >
                <span class="font-bold">{{ slotProps.item.word }}</span>
            </div>
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

<style scoped>
    .pt-sm {
        padding-top: 0.1rem;
    }
</style>
