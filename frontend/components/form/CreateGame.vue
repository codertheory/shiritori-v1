<template>
    <Form
        :validation-schema="validationSchema"
        :initial-values="initialValues"
        :validate-on-mount="false"
        @submit="onSubmit"
    >
        <div class="flex flex-column col-3 justify-content-center w-full">
            <InputFieldUsername />
            <Card>
                <template #content>
                    <UtilityFormUIBlock>
                        <FieldsetSettingsGame />
                    </UtilityFormUIBlock>
                </template>
            </Card>
            <div class="pt-6">
                <ButtonCreateGame class="w-full h-4rem" />
            </div>
        </div>
    </Form>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useCreateGameForm } from "~/composeables/useCreateGameForm";

    const { validationSchema, initialValues, onSubmit } = useCreateGameForm();
</script>

<style scoped>
    :deep(.p-card-body) {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    :deep(.p-card-content) {
        padding-top: 0 !important;
    }
</style>
