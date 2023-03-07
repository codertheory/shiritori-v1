<template>
    <Button
        icon="pi pi-check"
        label="Create Game"
        type="submit"
        :disabled="!formIsValid"
        :loading="loading"
    />
</template>

<script setup lang="ts">
    import { useIsFormValid } from "vee-validate";
    import { useCreateGameForm } from "~/composeables/useCreateGameForm";

    const formIsValid = useIsFormValid();
    const { loading } = useCreateGameForm();
</script>

<style scoped></style>
