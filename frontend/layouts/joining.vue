<template>
    <Form
        :validation-schema="validationSchema"
        :validate-on-mount="false"
        @submit.prevent="onSubmit"
    >
        <div
            class="grid justify-content-center align-content-center flex-wrap h-screen"
        >
            <div class="flex flex-column align-center justify-content-center">
                <SvgSecondaryLogo />
                <div class="mt-5">
                    <InputFieldUsername />
                </div>
                <ButtonJoinGame />
            </div>
        </div>
    </Form>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useJoinGameForm } from "~/composeables/useJoinGameForm";

    const { validationSchema, onSubmit } = useJoinGameForm();
</script>

<style scoped></style>
