<template>
    <Field :name="fieldName" v-slot="{ field, value }">
        <div class="field">
            <div class="col-12">
                <h5>{{ fieldLabel }}</h5>
                <InputBetterSelectButton
                    v-tooltip="tooltip"
                    :model-value="value"
                    :options="options"
                    :current-selected="value"
                    @change="(e) => handleChange(field)(e)"
                />
            </div>
        </div>
    </Field>
</template>

<script setup lang="ts">
    import { defineProps, PropType } from "vue";
    import { Field } from "vee-validate";
    import { SelectButtonChangeEvent } from "primevue/selectbutton";

    defineProps({
        fieldName: {
            type: String,
            required: true,
        },
        fieldLabel: {
            type: String,
            required: true,
        },
        options: {
            type: Array as PropType<{ label: string; value: any }[]>,
            required: true,
        },
        tooltip: {
            type: String,
            required: false,
            default: "",
        },
    });

    const handleChange = (field: any) => (e: SelectButtonChangeEvent) => {
        field.onChange[0](e.value);
    };
</script>
<style scoped></style>
