<template>
    <Story title="Shiritori Game">
        <Variant title="Lobby" :setup-app="setupLobby">
            <Lobby />
        </Variant>
        <Variant title="Game">
            <Playing />
        </Variant>
        <Variant title="Finished">
            <Finished />
        </Variant>
    </Story>
</template>

<script setup lang="ts">
    import Lobby from "~/layouts/lobby.vue";
    import Finished from "~/layouts/finished.vue";
    import Playing from "~/layouts/playing.vue";

    function setupLobby({ app }: { app: import("vue").App }) {
        // noinspection TypeScriptValidateTypes - this is a hack to get the historie to work
        // @ts-ignore
        app.config.globalProperties.$route = { params: { id: "abcd" } };
    }
</script>

<style scoped></style>
