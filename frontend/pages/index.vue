<template>
    <h1>Shiritori</h1>
    <FormCreateGame />
</template>

<script lang="ts" setup>
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
