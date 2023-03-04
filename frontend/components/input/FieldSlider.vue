<template>
    <Field :name="fieldName" v-slot="{ field, value, errorMessage }">
        <div class="field">
            <div class="col-12">
                <h5>{{ fieldLabel }}: {{ value }}</h5>
                <Slider
                    v-bind="{ ...field, ...$attrs }"
                    v-tooltip="tooltip"
                    :aria-describedby="`${fieldName}-help`"
                    :class="{ 'p-invalid': errorMessage }"
                    :model-value="value"
                />
            </div>

            <small :id="`${fieldName}-help`" class="p-error">{{
                errorMessage
            }}</small>
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
        tooltip: {
            type: String,
            required: false,
            default: "",
        },
    });
</script>

<style scoped></style>
