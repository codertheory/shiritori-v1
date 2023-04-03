<template>
    <div class="grid gap-6">
        <template v-for="player in gameStore.players" :key="player.id">
            <ListItemGamePlayer :player="player" />
        </template>
    </div>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
