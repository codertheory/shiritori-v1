<template>
  <Field name="username" v-slot="{ field, errorMessage }">
    <div class="field">
      <div class="col-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-user"></i>
          </span>
          <InputText
            v-bind="field"
            aria-describedby="username-help"
            :class="{ 'p-invalid': errorMessage }"
            placeholder="username"
          />
        </div>
      </div>

      <small id="username-help" class="p-error">{{ errorMessage }}</small>
    </div>
  </Field>
</template>

<script setup lang="ts">
import { Field } from "vee-validate";
</script>

<style scoped></style>
