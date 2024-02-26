from django.contrib import admin

from server.apps.habit_tracker.models import HabitUnit, HabitRecord, Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    pass


@admin.register(HabitUnit)
class HabitUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(HabitRecord)
class HabitRecordAdmin(admin.ModelAdmin):
    pass
