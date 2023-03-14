<template>
    <Card>
        <template #title>
            <h3>{{ player.name }} - {{ player.score }}</h3>
        </template>
        <template #content>
            <InputFieldWord v-if="player.isCurrent" :player-id="player.id" />
        </template>
    </Card>
</template>

<script setup lang="ts">
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
