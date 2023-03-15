<template>
    <div v-tooltip.top="tooltipMessage" style="display: inline-block">
        <Button
            :disabled="!gameStore.canStart"
            icon="pi pi-check"
            label="Start Game"
            type="button"
            @click="gameStore.startGame"
        />
    </div>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();

    const tooltipMessage = computed(() => {
        if (!gameStore.isHost) {
            return "Only the host can start the game";
        }
        if (!gameStore.canStart) {
            return "You need least 2 players to start the game";
        }
    });
</script>

<style scoped></style>
