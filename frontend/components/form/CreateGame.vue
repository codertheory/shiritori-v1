<template>
    <Form
        :validation-schema="validationSchema"
        :initial-values="initialValues"
        :validate-on-mount="false"
        @submit="onSubmit"
    >
        <div class="flex justify-content-center">
            <Card>
                <template #title>Create Game</template>
                <template #content>
                    <InputFieldUsername />
                    <Divider />
                    <h1>Settings</h1>
                    <FieldsetSettingsGame />
                </template>
                <template #footer>
                    <ButtonCreateGame />
                </template>
            </Card>
        </div>
    </Form>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useCreateGameForm } from "~/composeables/useCreateGameForm";
    const { validationSchema, initialValues, onSubmit } = useCreateGameForm();
</script>

<style scoped></style>
