<template>
    <div>
        <h1>Game {{ $route.params.id }}</h1>
        <div class="grid">
            <div class="col">
                <Card>
                    <template #title>Settings</template>
                    <template #content>
                        <FormSettingsGame />
                    </template>
                    <template #footer>
                        <div class="flex flex-end justify-content-end">
                            <ButtonStartGame />
                        </div>
                    </template>
                </Card>
            </div>
            <div class="col">
                <Card>
                    <template #title>Players</template>
                    <template #content>
                        <ListLobbyPlayers />
                    </template>
                </Card>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts"></script>

<style scoped></style>
