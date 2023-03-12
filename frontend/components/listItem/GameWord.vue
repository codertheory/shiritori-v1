<template>
    <Timeline :value="gameStore.words">
        <template #opposite="slotProps">
            <InlineMessage severity="info"
                >{{ slotProps.item.player.name }}
            </InlineMessage>
        </template>
        <template #marker="slotProps">
            <Badge :value="slotProps.item.score" size="large" />
        </template>
        <template #content="slotProps">
            {{ slotProps.item.word ?? "No word" }}
        </template>
    </Timeline>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
