<template>
    <BlockUI :blocked="disabled">
        <InputFieldSelect
            field-name="turn_time"
            field-label="Turn Timer"
            tooltip="The time each player has to play a word."
            :options="turnTimeOptions"
        />
        <InputFieldSelect
            field-name="word_length"
            field-label="Minimum Word Length"
            tooltip="The minimum length of words to play."
            :options="wordLengthOptions"
        />
        <InputFieldSelect
            field-name="max_turns"
            field-label="Rounds"
            tooltip="The number of rounds to play."
            :options="roundOptions"
        />
    </BlockUI>
</template>

<script setup lang="ts">
    import { ref } from "vue";
    defineProps({
        disabled: {
            type: Boolean,
            default: false,
        },
    });

    const turnTimeOptions = ref([
        {
            label: "5",
            value: 5,
        },
        {
            label: "15",
            value: 15,
        },
        {
            label: "30",
            value: 30,
        },
        {
            label: "60",
            value: 60,
        },
    ]);

    const wordLengthOptions = ref([
        {
            label: "3",
            value: 3,
        },
        {
            label: "4",
            value: 4,
        },
        {
            label: "5",
            value: 5,
        },
    ]);

    const roundOptions = ref([
        {
            label: "5",
            value: 5,
        },
        {
            label: "10",
            value: 10,
        },
        {
            label: "15",
            value: 15,
        },
    ]);
</script>

<style scoped></style>
