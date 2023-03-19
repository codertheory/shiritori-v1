from django.db import InterfaceError, models

from shiritori.utils import NanoIdField


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        try:
            return super().delete(using, keep_parents)
        except InterfaceError:
            return 0, {}


class NanoIdModel(models.Model):
    id = NanoIdField()

    class Meta:
        abstract = True
