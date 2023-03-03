<template>
  <Field :name="fieldName" v-slot="{ field, value, errorMessage }">
    <div class="field">
      <div class="col-12 md:col-4">
        <div class="p-inputgroup">
          <h5>{{ fieldLabel }}: {{ value }}</h5>
          <Slider
            v-bind="{ ...field, ...$attrs }"
            aria-describedby="max_turns-help"
            :class="{ 'p-invalid': errorMessage }"
            placeholder="max_turns"
          />
        </div>
      </div>

      <small id="max_turns-help" class="p-error">{{ errorMessage }}</small>
    </div>
  </Field>
</template>

<script setup lang="ts">
import { Field } from "vee-validate";
defineProps({
  fieldName: {
    type: String,
    required: true,
  },
  fieldLabel: {
    type: String,
    required: true,
  },
});
</script>

<style scoped></style>
