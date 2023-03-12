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
                    <span class="p-inputgroup-addon">
                        <i class="pi pi-user"></i>
                    </span>
                    <InputText
                        :ref="inputRef"
                        v-bind="field"
                        aria-describedby="word-help"
                        :class="{ 'p-invalid': errorMessage }"
                        :placeholder="gameStore.lastWord"
                        :disabled="!isCurrentPlayerMe"
                    />
                </div>
            </div>

            <small id="word-help" class="p-error">{{ errorMessage }}</small>
        </div>
    </Field>
</template>

<script setup lang="ts">
    import { computed, ref, VNodeRef, watch } from "vue";
    import { Field } from "vee-validate";
    import { useGameStore } from "~/stores/useGameStore";

    const inputRef = ref<VNodeRef | null>(null);
    const gameStore = useGameStore();

    const props = defineProps({
        playerId: {
            type: String,
            required: true,
        },
    });

    const currentPlayer = computed(() =>
        gameStore.players.find((player) => player.id === props.playerId)
    );

    const isCurrentPlayerMe = computed(() => {
        return currentPlayer.value?.id == gameStore?.me?.id;
    });

    watch(
        () => gameStore.currentPlayer,
        (currentPlayer) => {
            if (currentPlayer?.id === props.playerId) {
                inputRef?.value?.focus();
            }
        }
    );
</script>

<style scoped></style>
