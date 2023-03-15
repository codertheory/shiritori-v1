<template>
    <Sidebar
        v-model="globalStore.showSidebar"
        :modal="false"
        :visible="globalStore.showSidebar"
        position="right"
    >
        <h2>Words Used</h2>
        <ListItemGameWord />
    </Sidebar>
</template>

<script setup lang="ts">
    import { useGlobalStore } from "~/stores/useGlobalStore";

    const globalStore = useGlobalStore();
</script>

<style scoped></style>
