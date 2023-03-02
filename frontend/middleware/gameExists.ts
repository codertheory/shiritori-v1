import { useApi } from "~/composeables/useApi";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { id } = to.params;
  const { getGame } = useApi();
  const { data, error } = await getGame(id as string);
  if (!data.value || error.value) {
    return abortNavigation();
  }
  return true;
});
