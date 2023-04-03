<template>
    <DataTable :value="gameStore.leaderboard" table-style="min-width: 50rem">
        <Column field="trophy" header=""></Column>
        <Column field="score" header="Points"></Column>
        <Column field="name" header="Player"></Column>
        <Column :field="getBestWord" header="Best Word"></Column>
    </DataTable>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";
    import { components } from "~/schema";

    const gameStore = useGameStore();

    const getBestWord = (player: components["schemas"]["ShiritoriPlayer"]) => {
        const words = gameStore.getPlayerWords(player.id);
        if (words.length === 0) {
            return "";
        }
        const bestWord = words.reduce((a, b) => (a.score > b.score ? a : b));
        return bestWord.word;
    };
</script>

<style scoped>
    :deep(th) {
        background: transparent !important;
        border: unset !important;
        font-size: 1.5rem !important;
        font-weight: normal !important;
    }
    :deep(tr) {
        background: transparent !important;
        font-size: 3rem !important;
        font-weight: bold;
    }
    :deep(td) {
        background: transparent !important;
        font-size: 3rem !important;
        border: unset !important;
    }
</style>
