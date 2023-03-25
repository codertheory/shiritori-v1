<template>
    <div v-tooltip.top="tooltipMessage" style="display: inline-block">
        <Button
            :disabled="!gameStore.canStart"
            :loading="isSubmitting"
            icon="pi pi-check"
            label="Start Game"
            type="submit"
        />
    </div>
</template>

<script setup lang="ts">
    import { computed } from "vue";
    import { useGameStore } from "~/stores/useGameStore";
    import { useIsSubmitting } from "vee-validate";

    const gameStore = useGameStore();
    const isSubmitting = useIsSubmitting();

    const tooltipMessage = computed(() => {
        if (!gameStore.isHost) {
            return "Only the host can start the game";
        }
        if (!gameStore.canStart) {
            return "You need least 2 players to start the game";
        }
        return "";
    });
</script>

<style scoped></style>
