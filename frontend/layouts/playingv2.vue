<template>
    <div class="grid">
        <div class="flex flex-column col-8 pt-0">
            <div class="flex justify-content-center">
                <SvgSpotlightWithPlayer />
            </div>
        </div>
        <div class="col-4">
            <ListWords />
        </div>
        <div class="col-3">
            <div class="grid justify-content-center">
                <TimerTurnGame :time-left="timeLeft" :max-time="maxTime" />
            </div>
        </div>
        <div class="col-9">
            <ListGamePlayers />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from "vue";

    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();

    const timeLeft = computed(() => {
        return gameStore.gameTurnTimeLeft;
    });

    const maxTime = computed(() => {
        return gameStore.gameTurnDuration;
    });
</script>

<style scoped></style>
