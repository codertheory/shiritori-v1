<template>
    <div>
        <h1>Game {{ $route.params.id }}</h1>
        <div class="grid">
            <div class="col">
                <Form
                    :initial-values="initialValues"
                    :validate-on-mount="false"
                    :validation-schema="validationSchema"
                    @submit="onSubmit"
                >
                    <Card>
                        <template #title>Settings</template>
                        <template #content>
                            <FormSettingsGame :disabled="!gameStore.isHost" />
                        </template>
                        <template #footer>
                            <div class="flex flex-end justify-content-end">
                                <ButtonStartGame />
                            </div>
                        </template>
                    </Card>
                </Form>
            </div>
            <div class="col">
                <Card>
                    <template #title>Players</template>
                    <template #content>
                        <ListLobbyPlayers />
                    </template>
                </Card>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useGameStore } from "~/stores/useGameStore";
    import { useGameSettingsForm } from "~/composeables/useGameSettingsForm";

    const gameStore = useGameStore();
    const { validationSchema, initialValues, onSubmit } = useGameSettingsForm();
</script>

<style scoped></style>
