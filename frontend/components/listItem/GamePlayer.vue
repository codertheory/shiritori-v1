<template>
    <Card>
        <template #title>
            <h3>{{ player.name }} - {{ player.score }}</h3>
            <TimerTurnGame
                v-if="player.is_current"
                :is-current="player.is_current"
            />
        </template>
        <template #content>
            <InputFieldWord v-if="player.is_current" :player-id="player.id" />
        </template>
    </Card>
</template>

<script setup lang="ts">
    import { defineProps } from "vue";
    import { components } from "~/schema";
    import type { PropType } from "vue";

    defineProps({
        player: {
            type: Object as PropType<components["schemas"]["ShiritoriPlayer"]>,
            required: true,
        },
    });
</script>

<style scoped></style>
