<template>
    <Button
        icon="pi pi-check"
        type="button"
        label="Start Game"
        @click="gameStore.startGame"
        :disabled="!gameStore.isHost"
    />
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
