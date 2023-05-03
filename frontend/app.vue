<template>
    <Message class="p-card mt-0 pt-0" severity="info" sticky :closable="false">
        <div
            class="flex flex-grow-1 justify-center justify-content-center align-center align-items-center text-center"
        >
            Please note that this is a beta version of the website which is
            still undergoing final testing before its official release.
        </div>
        <div class="flex flex-grow-0 justify-end align-content-end">
            <Button
                @click="globalStore.toggleRulesModal"
                icon="pi pi-book"
                severity="help"
                aria-label="Game Rules"
                size="small"
            />
        </div>
    </Message>
    <DialogGameRules />
    <NuxtPage />
</template>
<script setup lang="ts">
    import { useGlobalStore } from "~/stores/useGlobalStore";

    const globalStore = useGlobalStore();
</script>
<style scoped>
    .p-message.p-message-info {
        background: rgba(0, 0, 0, 0.15);
        background-blend-mode: multiply;
        color: #ffffff;
        box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2),
            0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12);
        border: unset;
    }
    :deep(.p-message-text) {
        width: 100%;
        display: flex;
        justify-content: center;
    }
</style>
