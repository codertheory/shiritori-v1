<template>
    <div>
        <h1>Game {{ $route.params.id }}</h1>
        <div class="grid">
            <div class="col">
                <h1>Settings</h1>
            </div>
            <div class="col">
                <ListLobbyPlayers />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts"></script>

<style scoped></style>
