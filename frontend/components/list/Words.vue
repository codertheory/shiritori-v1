<template>
    <Sidebar
        v-model:visible="globalStore.showSidebar"
        :modal="false"
        position="right"
    >
        <div class="flex flex-column justify-content-center align-items-center">
            <h2 class="mt-0">Words Used</h2>
        </div>
        <divider class="mt-0" />
        <ListItemGameWord :words="gameStore.wordsTimeLine" />
    </Sidebar>
</template>

<script setup lang="ts">
    // import { computed, onMounted } from "vue";
    import { useGlobalStore } from "~/stores/useGlobalStore";
    // import { SidebarProps } from "primevue/sidebar";
    import { useGameStore } from "~/stores/useGameStore";

    const gameStore = useGameStore();

    const globalStore = useGlobalStore();

    // const device = useDevice();
    //
    // const position = computed<SidebarProps["position"]>(() => {
    //     if (device.isMobileOrTablet) {
    //         return "bottom";
    //     }
    //     return "right";
    // });
    //
    // onMounted(() => {
    //     if (device.isMobileOrTablet) {
    //         globalStore.showSidebar = false;
    //     }
    // });
</script>

<style scoped></style>
