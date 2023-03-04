<template>
    <Button
        icon="pi pi-check"
        type="button"
        label="Start Game"
        :disabled="!formIsValid"
        :loading="loading"
    />
</template>

<script setup lang="ts"></script>

<style scoped></style>
