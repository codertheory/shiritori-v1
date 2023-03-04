<template>
    <Form
        :validation-schema="validationSchema"
        :initial-values="initialValues"
        :validate-on-mount="false"
        @submit="onSubmit"
    >
        <FieldsetSettingsGame />
    </Form>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useGameSettingsForm } from "~/composeables/useGameSettingsForm";

    const { validationSchema, initialValues, onSubmit } = useGameSettingsForm();
</script>

<style scoped></style>
