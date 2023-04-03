<template>
    <Field
        name="word"
        v-slot="{ field, errorMessage }"
        :validate-on-blur="false"
        :validate-on-change="false"
        :validate-on-input="false"
    >
        <div
            class="field"
            :style="{
                width: `${fieldWith}rem` || '18rem',
            }"
        >
            <div class="col-12">
                <div class="p-inputgroup">
                    <InputText
                        ref="inputRef"
                        v-bind="field"
                        aria-describedby="word-help"
                        class="bubble"
                        :class="{ 'p-invalid': errorMessage }"
                        :placeholder="gameStore.lastLetter"
                        :disabled="!gameStore.isCurrentPlayerMe"
                        autocomplete="off"
                    />
                </div>
            </div>

            <small id="word-help" class="p-error">{{ errorMessage }}</small>
        </div>
    </Field>
</template>

<script setup lang="ts">
    import { ref, VNodeRef, watch, computed } from "vue";
    import { Field, useForm } from "vee-validate";
    import { useGameStore } from "~/stores/useGameStore";

    const inputRef = ref<VNodeRef | null>(null);
    const gameStore = useGameStore();
    const form = useForm();

    watch(
        () => gameStore.isCurrentPlayerMe,
        (isCurrentPlayerMe) => {
            if (isCurrentPlayerMe) {
                inputRef?.value?.focus();
            }
        }
    );

    const fieldWith = computed(() => {
        const { word } = form.values;
        let width = 225;
        if (word) {
            width = word.length * 20 + 50;
        }
        if (width > 400) {
            width = 400;
        }
        if (width < 225) {
            width = 225;
        }
        // Convert px to rem
        return width / 16;
    });
</script>

<style scoped>
    .bubble {
        height: 5rem;
        border-radius: var(--border-radius-smooth) !important;
        font-size: 2rem !important;
        background: var(--primary-color) !important;
    }
    ::-webkit-input-placeholder {
        /* WebKit, Blink, Edge */
        color: var(--text-color) !important;
    }
    :-moz-placeholder {
        /* Mozilla Firefox 4 to 18 */
        color: var(--text-color) !important;
    }
    ::-moz-placeholder {
        /* Mozilla Firefox 19+ */
        color: var(--text-color) !important;
    }
    :-ms-input-placeholder {
        /* Internet Explorer 10-11 */
        color: var(--text-color) !important;
    }
    ::-ms-input-placeholder {
        /* Microsoft Edge */
        color: var(--text-color) !important;
    }

    ::placeholder {
        /* Most modern browsers support this now. */
        color: var(--text-color) !important;
    }
</style>
