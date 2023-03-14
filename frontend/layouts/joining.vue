<template>
    <Form
        :validation-schema="validationSchema"
        :validate-on-mount="false"
        @submit="onSubmit"
    >
        <Dialog
            :header="`Joining game ${$route.params.id}`"
            :breakpoints="{ '960px': '75vw', '640px': '90vw' }"
            :style="{ width: '50vw' }"
            :modal="true"
            :closable="false"
            :keep-in-view-port="true"
            :visible="true"
            :draggable="false"
        >
            <template #default>
                <InputFieldUsername />
            </template>
            <template #footer>
                <Button
                    label="Cancel"
                    icon="pi pi-times"
                    @click="cancel"
                    class="p-button-text"
                />
                <ButtonJoinGame />
            </template>
        </Dialog>
    </Form>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useJoinGameForm } from "~/composeables/useJoinGameForm";

    const { validationSchema, onSubmit } = useJoinGameForm();

    const cancel = async () => {
        const router = useRouter();
        await router.push({ name: "index", replace: true });
    };
</script>

<style scoped></style>
