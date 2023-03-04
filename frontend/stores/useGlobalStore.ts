import { defineStore } from "pinia";
import { ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
    const loading = ref(false);
    const setLoading = (l: boolean) => {
        loading.value = l;
    };
    return { loading, setLoading };
});
