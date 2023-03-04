<template>
    <div>
        <h1>{{ player.name }}</h1>
    </div>
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
