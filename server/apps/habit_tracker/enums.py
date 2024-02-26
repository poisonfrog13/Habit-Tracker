from enum import StrEnum
from re import T


class _BaseDjangoChoice(StrEnum):
    @classmethod
    def as_django_choices(cls) -> list[tuple[str, str]]:
        return [(choice.name, choice.value) for choice in cls]


class HabitUnitType(_BaseDjangoChoice):
    INT = "Integer"
    FLOAT = "Float"
    BOOLEAN = "Boolean"
    TIME = "Time"


class HabitUnitName(_BaseDjangoChoice):
    # DISTANCE
    KM = "Kilometers"
    M = "Meters"
    MILES = "Miles"
    STEPS = "Steps"

    # DURATION
    HR = "Hours"
    MIN = "Minutes"
    SEC = "Seconds"

    # Quantity
    COUNT = "Count"
    REPETITIONS = "Repititions"
    ITEMS = "Items"
    SERVINGS = "Servings"
    SETS = "Sets"
    PERCENTAGE = "Percentage"
    PAGES = "Pages"
    WORDS = "Words"
    L = "Litres"
    ML = "Mililitres"

    # TRUE/FALSE
    YES_NO = "Yes / No"

    # ENERGY
    CALORIES = "Calories"

    # WEIGHT
    KG = "Kilograms"
    GR = "Grams"

    @classmethod
    def as_sorted_django_choices(cls) -> list[tuple[str, str]]:
        choices = cls.as_django_choices()
        return sorted(choices)
