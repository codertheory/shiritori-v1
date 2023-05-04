<template>
    <Story title="Game Word List">
        <template #controls>
            Word: <HstText v-model="wordForm.word" /> Score:
            <HstNumber v-model="wordForm.score" />
            Player Name: <HstText v-model="wordForm.playerName" />
            <HstButton @click="addWord(wordForm)">Add Word</HstButton>
            <HstButton @click="removeLastWord()">Remove Last Word</HstButton>
        </template>
        <ListItemGameWord :words="state" />
    </Story>
</template>

<script setup lang="ts">
    import { ref, reactive } from "vue";
    import { TimeLineWord } from "~/schema";

    const state = ref<TimeLineWord[]>([
        {
            word: "test",
            score: 1,
            playerName: "Player A",
        },
    ]);

    const wordForm = reactive({
        word: "",
        score: 0,
        playerName: "",
    });

    const addWord = ({ word, score, playerName }: TimeLineWord) => {
        state.value.push({ word, score, playerName });
        wordForm.word = "";
        wordForm.score = 0;
        wordForm.playerName = "";
    };

    const removeLastWord = () => {
        state.value.pop();
    };
</script>

<style scoped></style>
