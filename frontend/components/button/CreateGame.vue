<template>
  <Button
    icon="pi pi-check"
    type="submit"
    label="Create Game"
    :disabled="!formIsValid"
  />
</template>

<script setup lang="ts">
import { useIsFormValid } from "vee-validate";

const formIsValid = useIsFormValid();
</script>

<style scoped></style>
