from django.db import models

from .constants import (
    INGREDIENT_MEASURE_UNIT_MAX_LENGTH,
    INGREDIENT_NAME_MAX_LENGTH
)


class Ingredient(models.Model):
    """
    Модель для ингредиентов
    """
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        blank=False,
        null=False,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=INGREDIENT_MEASURE_UNIT_MAX_LENGTH,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_mu'
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}, {self.measurement_unit}"
