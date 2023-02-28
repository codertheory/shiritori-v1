# pylint: disable=cyclic-import
from typing import Any

from django.db import models

from shiritori.utils import generate_id


class NanoIdField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 21)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('primary_key', True)
        kwargs.setdefault('default', generate_id)
        super().__init__(*args, **kwargs)

    def get_default(self) -> Any:
        return generate_id(self.max_length)
