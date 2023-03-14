<template>
    <div>
        <div class="grid">
            <div class="col-12">
                <div class="align-center">
                    <h1>Game {{ $route.params.id }}</h1>
                    <TimerTurnGame />
                    <Button label="Words" @click="globalStore.toggleSidebar" />
                </div>
            </div>
            <div class="col-12">
                <Form @submit="gameTurnForm.onSubmit">
                    <div class="grid">
                        <div class="grid-item">
                            <h2>Players</h2>
                            <div class="grid">
                                <div
                                    class="grid-item"
                                    v-for="player in gameStore.players"
                                    :key="player.id"
                                >
                                    <ListItemGamePlayer :player="player" />
                                </div>
                            </div>
                        </div>
                    </div>
                </Form>
            </div>
        </div>
        <ListWords />
    </div>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useGameStore } from "~/stores/useGameStore";
    import { useGameTurnForm } from "~/composeables/useGameTurnForm";
    import { useGlobalStore } from "~/stores/useGlobalStore";

    const globalStore = useGlobalStore();
    const gameStore = useGameStore();
    const gameTurnForm = useGameTurnForm();
</script>

<style scoped></style>
