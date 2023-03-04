<template>
    <Button
        icon="pi pi-check"
        type="button"
        label="Start Game"
        @click="startGame"
    />
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const { startGame } = useGameStore();
</script>

<style scoped></style>
