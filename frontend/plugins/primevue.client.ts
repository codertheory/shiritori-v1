import Tooltip from "primevue/tooltip";

export default defineNuxtPlugin((nuxtApp) => {
    // Doing something with nuxtApp
    nuxtApp.vueApp.directive("tooltip", Tooltip);
});
