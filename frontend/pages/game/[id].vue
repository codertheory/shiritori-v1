<template>
  <h1>Game {{ $route.params.id }}</h1>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["game-exists"],
});
</script>

<style scoped></style>
