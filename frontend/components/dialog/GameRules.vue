<template>
    <Dialog
        :visible="globalStore.isRulesModalOpen"
        :draggable="false"
        modal
        close-on-escape
        @update:visible="globalStore.isRulesModalOpen = $event"
    >
        <template #header>
            <div class="flex justify-between">
                <div>Game Rules</div>
            </div>
        </template>
        <template #default>
            <div class="flex flex-grow-1 text-plain">
                <p class="line-height-4">
                    These are the rules of the game.<br />
                    Each player will have a turn to type in a word that
                    starts<br />
                    with the last letter of the previous word.<br />
                    The goal of the game is to score the highest
                </p>
            </div>
            <Divider layout="horizontal" type="solid" />
            <div class="flex flex-grow-1 text-plain">Score Modifiers:</div>
            <div class="flex flex-grow-1 text-plain line-height-4">
                <ul>
                    <li>
                        Word length:
                        <Tag value="1.25" severity="info" />
                    </li>
                    <li>
                        Elapsed time:
                        <ul>
                            <li>
                                0-5 seconds:
                                <Tag value="1.8" severity="info" />
                            </li>
                            <li>
                                6-10 seconds:
                                <Tag value="1.5" severity="info" />
                            </li>
                            <li>
                                11-15 seconds:
                                <Tag value="1.2" severity="info" />
                            </li>
                            <li>
                                >15 seconds:
                                <Tag value="1.0" severity="info" />
                            </li>
                        </ul>
                    </li>
                    <li>
                        Letter that ends with an unused letter:
                        <Tag value="1.5" severity="info" />
                    </li>
                </ul>
            </div>
        </template>
    </Dialog>
</template>

<script setup lang="ts">
    import { useGlobalStore } from "~/stores/useGlobalStore";

    const globalStore = useGlobalStore();
</script>

<style scoped>
    .text-plain {
        color: var(--text-color);
    }
</style>
