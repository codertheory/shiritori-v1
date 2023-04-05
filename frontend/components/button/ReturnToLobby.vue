<template>
    <Button
        class="w-full h-4rem"
        label="Return to Lobby"
        type="submit"
        :disabled="!gameStore.isHost"
        @click="gameStore.handleRestartGame"
    />
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
