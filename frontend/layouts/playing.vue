<template>
    <div>
        <h1>Game {{ $route.params.id }}</h1>
        <div class="grid">
            <div class="grid-item">
                <h2>Players</h2>
                <div class="grid">
                    <div
                        class="grid-item"
                        v-for="player in gameStore.players"
                        :key="player.id"
                    >
                        <ListItemGamePlayer :player="player" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();
</script>

<style scoped></style>
