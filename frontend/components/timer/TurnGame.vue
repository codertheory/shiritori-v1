<template>
    <Knob
        v-model="gameStore.turnTimeLeft"
        :min="0"
        :max="gameStore.gameTurnDuration"
        readonly
    />
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
