<template>
  <Form
    :validation-schema="validationSchema"
    :initial-values="initialValues"
    :validate-on-mount="false"
    @submit="onSubmit"
  >
    <div class="flex justify-content-center">
      <Card>
        <template #title>Create Game</template>
        <template #content>
          <InputFieldUsername />
          <Divider />
          <h1>Settings</h1>
          <InputFieldSlider
            field-name="word_length"
            field-label="Word Length"
            tooltip="The length of the words to guess."
            :min="3"
            :max="5"
          />
          <InputFieldSlider
            field-name="turn_time"
            field-label="Turn Time (seconds)"
            tooltip="The time each player has to play a word."
            :min="30"
            :max="120"
          />
          <InputFieldSlider
            field-name="max_turns"
            field-label="Max Turns"
            tooltip="The maximum number of rounds per game."
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
