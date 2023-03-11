<template>
    <Card>
        <template #title>
            <h3>{{ player.name }} - {{ player.score }}</h3>
            <TimerTurnGame />
        </template>
        <template #content>
            <InputFieldWord />
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
