<template>
    <Card>
        <template #title>Words Used</template>
        <template #content>
            <ListItemGameWord :words="gameStore.wordsTimeLine" />
        </template>
    </Card>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
