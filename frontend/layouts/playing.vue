<template>
    <div class="grid">
        <div
            class="flex flex-column col-2 justify-content-center align-items-center"
        >
            <div class="col">
                <TimerTurnGame />
            </div>
            <div class="col">
                <p class="text-xl font-bold">
                    Turn: {{ gameStore.currentRound }} /
                    {{ gameStore.maxTurns }}
                </p>
            </div>
            <div class="col">
                <Button label="Words" @click="globalStore.toggleSidebar" />
            </div>
        </div>
        <div
            class="flex flex-row col-8 justify-content-center align-items-center"
        >
            <div v-if="gameStore.isCurrentPlayerMe">
                <Form @submit="gameTurnForm.onSubmit">
                    <InputFieldWord />
                </Form>
            </div>
            <div
                v-else
                class="flex flex-column justify-content-center align-items-center"
            >
                <p class="m-2 text-5xl w-min text-primary font-bold">
                    {{ gameStore.currentPlayer?.name || "" }}
                </p>
                <p class="m-2 text-5xl font-italic">is thinking of a word...</p>
            </div>
        </div>
        <div class="col-12">
            <div
                class="grid justify-content-center align-content-center flex-wrap"
            >
                <ListGamePlayers />
            </div>
        </div>
        <ListWords />
    </div>
</template>

<script setup lang="ts">
    import { Form } from "vee-validate";
    import { useGameTurnForm } from "~/composeables/useGameTurnForm";
    import { useGlobalStore } from "~/stores/useGlobalStore";
    import { useGameStore } from "~/stores/useGameStore";

    const globalStore = useGlobalStore();
    const gameStore = useGameStore();
    const gameTurnForm = useGameTurnForm();
</script>

<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.5s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
