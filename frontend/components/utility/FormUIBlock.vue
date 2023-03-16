<template>
    <BlockUI :blocked="isSubmitting">
        <slot />
    </BlockUI>
</template>

<script lang="ts" setup>
    import { useIsSubmitting } from "vee-validate";

    const isSubmitting = useIsSubmitting();
</script>

<style scoped></style>
