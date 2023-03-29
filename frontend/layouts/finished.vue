<template>
    <Card>
        <template #title>
            <h1>Finished</h1>
        </template>
        <template #content>
            <h1>Winner: {{ winnerName }} with {{ winnerScore }} Points</h1>
        </template>
    </Card>
</template>

<script lang="ts" setup>
    import { useGameStore } from "~/stores/useGameStore";
    import { computed } from "vue";

    const gameStore = useGameStore();

    const winnerName = computed(() => gameStore?.winner?.name ?? "");
    const winnerScore = computed(() => gameStore?.winner?.score ?? 0);
</script>

<style scoped></style>
