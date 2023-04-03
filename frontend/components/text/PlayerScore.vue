<template>
    <p>{{ tweened.number.toFixed(0) }}</p>
</template>

<script setup lang="ts">
    import { reactive, watch } from "vue";
    import gsap from "gsap";

    const props = defineProps({
        number: {
            type: Number,
            required: true,
        },
    });

    const tweened = reactive({
        number: 0,
    });

    watch(
        () => props.number,
        (n) => {
            if (Number.isNaN(n)) {
                return;
            }
            gsap.to(tweened, { duration: 0.5, number: n });
        }
    );
</script>

<style scoped></style>
