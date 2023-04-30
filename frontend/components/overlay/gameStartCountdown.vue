<template>
    <Dialog
        :closable="false"
        :visible="gameStore.isGameStarting"
        modal
        :draggable="false"
        header="Game is starting..."
    >
        <TimerTurnGame class="ml-2" :time-left="timeLeft" :max-time="3" />
    </Dialog>
</template>

<script setup lang="ts">
    import { computed } from "vue";
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();

    const timeLeft = computed(() => {
        return gameStore.gameStartCountdown;
    });
</script>

<style scoped></style>
