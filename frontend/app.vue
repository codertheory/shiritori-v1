<template>
    <NuxtPage />
    <Message class="p-card" severity="info" sticky :closable="false">
        <div class="flex justify-center align-center text-center">
            Please note that this is a beta version of the website which is
            still undergoing final testing before its official release.
        </div>
    </Message>
</template>
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
