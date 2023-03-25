<template>
    <Sidebar
        v-model:visible="globalStore.showSidebar"
        :modal="false"
        :position="position"
        :dismissable="device.isMobileOrTablet"
    >
        <h2>Words Used</h2>
        <ListItemGameWord />
    </Sidebar>
</template>

<script setup lang="ts">
    import { computed, onMounted } from "vue";
    import { useGlobalStore } from "~/stores/useGlobalStore";
    import { SidebarProps } from "primevue/sidebar";

    const globalStore = useGlobalStore();

    const device = useDevice();

    const position = computed<SidebarProps["position"]>(() => {
        if (device.isMobileOrTablet) {
            return "bottom";
        }
        return "right";
    });

    onMounted(() => {
        if (device.isMobileOrTablet) {
            globalStore.showSidebar = false;
        }
    });
</script>

<style scoped></style>
