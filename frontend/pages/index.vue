<template>
    <div class="grid">
        <div class="col-3 p-0">
            <SvgLogo />
        </div>
        <div class="col-9 justify-content-center align-center flex">
            <FormCreateGame />
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { useHead } from "unhead";

    useHead({
        title: "Shiritori",
        meta: [
            { key: "og:type", property: "og:type", content: "website" },
            {
                key: "og:title",
                property: "og:title",
                content: "Play Shiritori with Friends",
            },
            {
                key: "og:url",
                property: "og:url",
                content: "https://shiritoriwithfriends.com/",
            },

            {
                key: "description",
                name: "description",
                content:
                    "Shiritori is a Japanese word game " +
                    "where players take turns adding to a chain of words.",
            },
        ],
    });
</script>

<style scoped></style>
