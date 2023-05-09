<template>
    <Timeline :value="words">
        <template #opposite="slotProps">
            <div
                class="flex flex-row justify-content-start align-items-end pt-sm"
            >
                <span class="font-bold text-primary">
                    {{ slotProps.item.playerName }}
                </span>
            </div>
        </template>
        <template #marker="slotProps">
            <div
                class="flex flex-row justify-content-center align-items-center"
            >
                <Badge :value="slotProps.item.score" />
            </div>
        </template>
        <template #content="slotProps">
            <div
                class="flex flex-row justify-content-center align-items-end pt-sm"
            >
                <span class="font-bold">{{ slotProps.item.word }}</span>
            </div>
        </template>
    </Timeline>
</template>

<script setup lang="ts">
    import { PropType } from "vue";
    import { TimeLineWord } from "~/schema";

    defineProps({
        words: {
            type: Array as PropType<TimeLineWord[]>,
            required: true,
        },
    });
</script>

<style scoped>
    .pt-sm {
        padding-top: 0.1rem;
    }
</style>
