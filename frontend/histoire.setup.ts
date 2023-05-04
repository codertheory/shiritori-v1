import { createPinia } from "pinia";
import { defineSetupVue3 } from "@histoire/plugin-vue";
import PrimeVue from "primevue/config";
import Tooltip from "primevue/tooltip";

export const setupVue3 = defineSetupVue3(({ app }) => {
    const pinia = createPinia();
    app.use(pinia); // Add Pinia store
    app.use(PrimeVue);

    app.directive("tooltip", Tooltip);
});
