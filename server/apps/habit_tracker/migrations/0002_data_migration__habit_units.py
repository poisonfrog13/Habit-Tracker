# Generated by Django 5.0.2 on 2024-03-26 00:15

from django.db import migrations

from server.apps.habit_tracker import enums

HABIT_UNITS = (
    (enums.HabitUnitName.CALORIES, enums.HabitUnitType.INT),
    (enums.HabitUnitName.COUNT, enums.HabitUnitType.INT),
    (enums.HabitUnitName.GR, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.HR, enums.HabitUnitType.INT),
    (enums.HabitUnitName.ITEMS, enums.HabitUnitType.INT),
    (enums.HabitUnitName.KG, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.KM, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.L, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.M, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.MILES, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.MIN, enums.HabitUnitType.INT),
    (enums.HabitUnitName.ML, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.PAGES, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.PERCENTAGE, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.REPETITIONS, enums.HabitUnitType.INT),
    (enums.HabitUnitName.SEC, enums.HabitUnitType.FLOAT),
    (enums.HabitUnitName.SERVINGS, enums.HabitUnitType.INT),
    (enums.HabitUnitName.SETS, enums.HabitUnitType.INT),
    (enums.HabitUnitName.STEPS, enums.HabitUnitType.INT),
    (enums.HabitUnitName.YES_NO, enums.HabitUnitType.BOOLEAN),
    (enums.HabitUnitName.WORDS, enums.HabitUnitType.INT),
)

def forwards(apps, schema_editor):
    model = apps.get_model('habit_tracker', 'HabitUnit')
    for habit_name, habit_unit in HABIT_UNITS:
        model.objects.create(name=habit_name.name, type=habit_unit)

def backwards(apps, schema_editor):
    model = apps.get_model('habit_tracker', 'HabitUnit')
    for habit_name, habit_unit in HABIT_UNITS:
        model.objects.get(name=habit_name.name, type=habit_unit).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('habit_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
