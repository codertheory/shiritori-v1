<template>
    <Button
        label="Create Game"
        class="rounded-text-input"
        type="submit"
        :disabled="!formIsValid"
        :loading="isSubmitting"
    />
</template>

<script setup lang="ts">
    import { useIsFormValid, useIsSubmitting } from "vee-validate";

    const isSubmitting = useIsSubmitting();
    const formIsValid = useIsFormValid();
</script>

<style scoped>
    :deep(.p-button) {
        border-radius: 40px !important;
    }
</style>
