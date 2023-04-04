<template>
    <Field name="username" v-slot="{ field, errorMessage }">
        <div class="field">
            <div class="col-12">
                <div class="p-inputgroup">
                    <InputText
                        v-bind="field"
                        aria-describedby="username-help"
                        class="rounded-text-input"
                        :class="{ 'p-invalid': errorMessage }"
                        placeholder="ENTER USERNAME"
                        autofocus
                        autocomplete="off"
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

<style scoped lang="scss"></style>
