<template>
    <div class="root">
        <svg
            class="svg"
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
        >
            <g class="circle">
                <circle class="time-elapsed-path" cx="50" cy="50" r="45" />
                <path
                    class="time-left-path"
                    v-if="timeLeft > 0"
                    d="
            M 50, 50
            m -45, 0
            a 45,45 0 1,0 90,0
            a 45,45 0 1,0 -90,0
          "
                    :style="{ strokeDasharray }"
                ></path>
            </g>
        </svg>
        <div class="time-left-container">
            <span class="time-left-label">{{ timeLeftString }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from "vue";

    const props = defineProps({
        timeLeft: {
            type: Number,
            required: true,
        },
        maxTime: {
            type: Number,
            required: true,
        },
    });

    const padToTwo = (num: number) => {
        return num.toString().padStart(2, "0");
    };

    const timeLeftString = computed(() => {
        const minutes = Math.floor(props.timeLeft / 60);
        const seconds = props.timeLeft % 60;
        if (minutes > 0) {
            return `${minutes}m:${padToTwo(seconds)}s`;
        }
        return `${seconds}s`;
    });

    const strokeDasharray = computed(() => {
        const radius = 45;
        const total = 2 * Math.PI * radius;
        const timeFraction = props.timeLeft / props.maxTime;
        const adjTimeFraction =
            timeFraction - (1 - timeFraction) / props.maxTime;
        const elapsedDash = Math.floor(adjTimeFraction * total);
        return `${elapsedDash} ${total}`;
    });
</script>

<style scoped>
    /** Sets the container's height and width */
    .root {
        height: 150px;
        width: 150px;
        position: relative;
    }
    /** Removes SVG styling that would hide the time label */
    .circle {
        fill: white;
        stroke: none;
    }
    /** The SVG path that displays the timer's progress */
    .time-elapsed-path {
        stroke-width: 6px;
        stroke: var(--surface-b);
    }
    .time-left-container {
        /** Size should be the same as that of parent container */
        height: inherit;
        width: inherit;
        /** Place container on top of circle ring */
        position: absolute;
        top: 0;
        /** Center content (label) vertically and horizontally  */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .time-left-label {
        font-size: 32px;
        font-weight: bold;
        color: var(--primary-color);
    }
    .time-left-path {
        /* Same thickness as the original ring */
        stroke-width: 7px;
        /* Rounds the path endings  */
        stroke-linecap: square;
        /* Makes sure the animation starts at the top of the circle */
        transform: rotate(90deg);
        transform-origin: center;
        /* One second aligns with the speed of the countdown timer */
        transition: 1s linear all;
        /* Colors the ring */
        stroke: var(--primary-color);
    }
</style>
