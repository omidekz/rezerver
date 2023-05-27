from libs.model import Model, fields
from enum import IntEnum


class WeekDay(IntEnum):
    SAT = 0
    SUN = 1
    MON = 2
    TUE = 3
    WED = 4
    THU = 5
    FRI = 6


class Time(Model):
    shop = fields.ForeignKeyField("provider.Shop", "times", fields.CASCADE)
    day = fields.IntEnumField(WeekDay)
    open = fields.TimeField()
    close = fields.TimeField()
