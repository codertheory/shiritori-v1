<template>
    <InputText
        :placeholder="gameStore.lastWord"
        :disabled="!gameStore.isMyTurn"
    />
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
