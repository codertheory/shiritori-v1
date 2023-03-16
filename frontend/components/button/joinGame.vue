<template>
    <Button
        :loading="isSubmitting"
        icon="pi pi-check"
        label="Join Game"
        :disabled="!formIsValid"
        type="submit"
        @click="submitForm"
    />
</template>

<script setup lang="ts">
    import {
        useIsFormValid,
        useIsSubmitting,
        useSubmitForm,
    } from "vee-validate";
    import { useJoinGameForm } from "~/composeables/useJoinGameForm";

    const formIsValid = useIsFormValid();

    const { onSubmit } = useJoinGameForm();
    const isSubmitting = useIsSubmitting();

    const submitForm = useSubmitForm(onSubmit);
</script>

<style scoped></style>
