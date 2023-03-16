<template>
    <Button
        icon="pi pi-check"
        label="Create Game"
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

<style scoped></style>
