<template>
    <div>
        <h1>Players</h1>
        <ul>
            <li v-for="player in players" :key="player.id">
                <ListItemLobbyPlayer :player="player" />
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
    import { useGameStore } from "~/stores/useGameStore";

    const { players } = useGameStore();



</script>

<style scoped></style>
