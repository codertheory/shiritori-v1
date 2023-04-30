<template>
    <Field
        name="word"
        v-slot="{ field, errorMessage }"
        :validate-on-blur="false"
        :validate-on-change="false"
        :validate-on-input="false"
    >
        <div class="field">
            <div class="col-12">
                <div class="p-inputgroup">
                    <InputText
                        ref="inputRef"
                        v-bind="field"
                        aria-describedby="word-help"
                        class="bubble text-center"
                        :class="{ 'p-invalid': errorMessage }"
                        :placeholder="gameStore.lastLetter"
                        autocomplete="off"
                        autocorrect="off"
                        autocapitalize="off"
                    />
                </div>
            </div>

            <small id="word-help" class="p-error">{{ errorMessage }}</small>
        </div>
    </Field>
</template>

<script setup lang="ts">
    import { ref, watch } from "vue";
    import { Field } from "vee-validate";
    import { useGameStore } from "~/stores/useGameStore";
    import InputText from "primevue/inputtext/InputText.vue";

    const inputRef = ref<InputText | null>(null);
    const gameStore = useGameStore();

    watch(
        () => gameStore.currentPlayer,
        () => {
            if (gameStore.isCurrentPlayerMe) {
                inputRef.value?.$el?.focus();
            }
        }
    );
</script>

<style scoped>
    .bubble {
        height: 5rem;
        border-radius: var(--border-radius-smooth) !important;
        font-size: 2rem !important;
        background: var(--primary-color) !important;
    }
    ::placeholder {
        /* Most modern browsers support this now. */
        color: var(--text-color) !important;
    }
</style>
