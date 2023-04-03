<template>
    <div class="pt-6">
        <div class="w-full" v-tooltip.top="tooltipMessage" style="">
            <Button
                :disabled="!gameStore.canStart"
                :loading="isSubmitting"
                class="w-full h-4rem"
                label="Start Game"
                type="submit"
            />
        </div>
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

<style scoped>
    :deep(.p-button) {
        border-radius: 40px !important;
    }
</style>
