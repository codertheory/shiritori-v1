import { defineStore } from "pinia";
import { ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
    const loading = ref(false);
    const showSidebar = ref(true);
    const isRulesModalOpen = ref(false);
    const setLoading = (l: boolean) => {
        loading.value = l;
    };

    const toggleSidebar = () => {
        showSidebar.value = !showSidebar.value;
    };

    const toggleRulesModal = () => {
        isRulesModalOpen.value = !isRulesModalOpen.value;
    };

    return {
        loading,
        showSidebar,
        isRulesModalOpen,
        setLoading,
        toggleSidebar,
        toggleRulesModal,
    };
});
