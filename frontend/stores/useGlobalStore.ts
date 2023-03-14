import { defineStore } from "pinia";
import { ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
    const loading = ref(false);
    const showSidebar = ref(true);
    const setLoading = (l: boolean) => {
        loading.value = l;
    };

    const toggleSidebar = () => {
        showSidebar.value = !showSidebar.value;
    };

    return { loading, showSidebar, setLoading, toggleSidebar };
});
