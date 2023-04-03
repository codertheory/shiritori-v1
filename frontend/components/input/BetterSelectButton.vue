<template>
    <div class="grid gap-3 justify-content-evenly">
        <ToggleButton
            v-for="option in options"
            :key="option.value"
            :option="option"
            :model-value="currentSelected === option.value"
            :on-label="option.label"
            :off-label="option.label"
            @update:model-value="handleUpdate(option)"
        />
    </div>
</template>

<script setup lang="ts">
    import { PropType } from "vue";

    defineProps({
        options: {
            type: Array as PropType<{ label: string; value: any }[]>,
            required: true,
        },
        currentSelected: {
            type: undefined,
            required: true,
        },
    });

    const emit = defineEmits(["change"]);

    const handleUpdate = (option: any) => {
        emit("change", option);
    };
</script>

<style scoped>
    :deep(.p-button) {
        border-radius: 1.875rem !important;
        min-width: 4.688rem !important;
    }
</style>
