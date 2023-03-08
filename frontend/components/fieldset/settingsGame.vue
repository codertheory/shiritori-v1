<template>
    <div>
        <InputFieldSlider
            field-name="word_length"
            field-label="Word Length"
            tooltip="The length of the words to guess."
            :min="3"
            :max="5"
            :disabled="disabled"
        />
        <InputFieldSlider
            field-name="turn_time"
            field-label="Turn Time (seconds)"
            tooltip="The time each player has to play a word."
            :min="30"
            :max="120"
            :disabled="disabled"
        />
        <InputFieldSlider
            field-name="max_turns"
            field-label="Max Turns"
            tooltip="The maximum number of rounds per game."
            :min="5"
            :max="20"
            :disabled="disabled"
        />
    </div>
</template>

<script setup lang="ts">
    defineProps({
        disabled: {
            type: Boolean,
            default: false,
        },
    });
</script>

<style scoped></style>
