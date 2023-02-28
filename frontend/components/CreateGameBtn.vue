<template>
  <Button @click="createGame"> Create Game </Button>
</template>

<script setup lang="ts">
import { useApi } from "~/composeables/useApi";

const { createGame } = useApi();
</script>

<style scoped></style>
