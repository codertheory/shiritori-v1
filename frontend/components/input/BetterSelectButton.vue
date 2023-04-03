<template>
    <div class="grid gap-3 justify-content-evenly">
        <ToggleButton
            v-for="option in options"
            :key="option.value"
            :option="option"
            :model-value="currentSelected === option.value"
            :on-label="option.label"
            :off-label="option.label"
            @update:model-value="(value) => handleUpdate(option)(value)"
        />
    </div>
</template>

<script setup lang="ts">
    defineProps({
        options: {
            type: Array,
            required: true,
        },
        currentSelected: {
            type: undefined,
            required: true,
        },
    });

    const emit = defineEmits(["change"]);

    const handleUpdate = (option: any) => (value: boolean) => {
        if (value) {
            emit("change", option);
        }
    };
</script>

<style scoped>
    :deep(.p-button) {
        border-radius: 1.875rem !important;
        min-width: 4.688rem !important;
    }
</style>
