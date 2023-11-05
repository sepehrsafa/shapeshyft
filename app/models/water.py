from tortoise import fields, models
import datetime

from .audit import AuditableModel

class WaterEntries(AuditableModel):
    email = fields.CharField(max_length=50)
    amt = fields.IntField(default=0)
    date = fields.DateField()
    time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "hydration_log"
