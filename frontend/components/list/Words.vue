<template>
    <Sidebar v-model="globalStore.showSidebar" position="right" :modal="false">
        <h2>Words Used</h2>
        <ListItemGameWord />
    </Sidebar>
</template>

<script setup lang="ts">
    import { useGlobalStore } from "~/stores/useGlobalStore";

    const globalStore = useGlobalStore();
</script>

<style scoped></style>
