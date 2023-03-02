<template>
  <Button @click="newGame"> Create Game </Button>
</template>

<script setup lang="ts">
import { useApi } from "~/composeables/useApi";

const { createGame } = useApi();

const newGame = () => {
  createGame({
    settings: {
      locale: "en",
      max_turns: 10,
      turn_time: 60,
      word_length: 5,
    },
  });
};
</script>

<style scoped></style>
