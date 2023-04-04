<template>
    <Form
        :initial-values="gameStore.settings"
        :validate-on-mount="false"
        :validation-schema="gameSettingsForm.validationSchema"
        @submit="gameSettingsForm.onSubmit"
    >
        <div class="grid">
            <SvgRoomCode :room-code="$route.params.id as string" />
            <div class="col">
                <Card>
                    <template #title>Settings</template>
                    <template #content>
                        <FormSettingsGame :disabled="!gameStore.isHost" />
                        <ButtonStartGame />
                    </template>
                </Card>
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
    </Form>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useGameStore } from "~/stores/useGameStore";
    import { useGameSettingsForm } from "~/composeables/useGameSettingsForm";

    const gameStore = useGameStore();
    const gameSettingsForm = useGameSettingsForm();
</script>

<style scoped>
    :deep(.p-card) {
        height: 100%;
    }
</style>
