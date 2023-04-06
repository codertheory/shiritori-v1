<template>
    <Card
        class="flex flex-column justify-content-center align-items-center"
        :class="{ 'active-player': gameStore.isPlayerCurrent(player.id) }"
        style="min-width: 15.625rem"
    >
        <template #title>
            <div
                class="flex col-12 flex-row justify-content-center align-items-center"
                :class="{ disconnected: !player.isConnected }"
            >
                <h3 class="align-center">{{ player.name }} -</h3>
                <div class="ml-2">
                    <PlayerScore :number="player.score" />
                </div>
            </div>
        </template>
    </Card>
</template>

<script setup lang="ts">
    import { components } from "~/schema";
    import type { PropType } from "vue";
    import PlayerScore from "~/components/text/PlayerScore.vue";
    import { useGameStore } from "~/stores/useGameStore";

    defineProps({
        player: {
            type: Object as PropType<components["schemas"]["ShiritoriPlayer"]>,
            required: true,
        },
    });

    const gameStore = useGameStore();
</script>

<style scoped>
    :deep(.p-card-body) {
        width: 100%;
    }
    .active-player {
        border: 2px solid var(--primary-color);
    }
</style>
