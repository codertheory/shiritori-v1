<template>
    <Button
        icon="pi pi-check"
        label="Join Game"
        :disabled="!formIsValid"
        autofocus
        @click="submitForm"
    />
</template>

<script setup lang="ts">
    import { useIsFormValid, useSubmitForm } from "vee-validate";
    import { useJoinGameForm } from "~/composeables/useJoinGameForm";

    const formIsValid = useIsFormValid();

    const { onSubmit } = useJoinGameForm();

    const submitForm = useSubmitForm(onSubmit);
</script>

<style scoped></style>
