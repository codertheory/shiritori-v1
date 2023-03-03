<template>
  <Form
    :validation-schema="validationSchema"
    :initial-values="initialValues"
    :validate-on-mount="false"
    @submit="onSubmit"
  >
    <div class="flex justify-content-center">
      <Card class="card">
        <template #title>Create Game</template>
        <template #content>
          <InputUsername />
          <Divider />
          <h1>Settings</h1>
          <InputSlider
            field-name="word_length"
            field-label="Word Length"
            :min="3"
            :max="5"
          />
          <InputSlider
            field-name="turn_time"
            field-label="Turn Time (seconds)"
            :min="30"
            :max="120"
          />
          <InputSlider
            field-name="max_turns"
            field-label="Max Turns"
            :min="5"
            :max="20"
          />
        </template>
        <template #footer>
          <ButtonCreateGame />
        </template>
      </Card>
    </div>
  </Form>
</template>

<script setup lang="ts">
import { Form } from "vee-validate";
import { useCreateGameForm } from "~/composeables/useCreateGameForm";
const { validationSchema, initialValues, onSubmit } = useCreateGameForm();
</script>

<style scoped></style>
