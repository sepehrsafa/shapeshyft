from .audit import AuditableModel
from enum import Enum
from tortoise import fields, models
import uuid


class FoodType(Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACK = "SNACK"


class Food(AuditableModel):
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.UserAccount", related_name="foods")
    type = fields.CharEnumField(FoodType)
    name = fields.CharField(max_length=100)
    unit = fields.CharField(max_length=100)
    calories = fields.CharField(max_length=100)
    fat = fields.CharField(max_length=100)
    carbs = fields.CharField(max_length=100)
    protein = fields.CharField(max_length=100)
    link = fields.CharField(max_length=100)
    number_of_units = fields.IntField()

class Meals(AuditableModel):
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.UserAccount", related_name="mealplan")
    breakfast = fields.CharField(max_length = 100)
    lunch = fields.CharField(max_length = 100)
    dinner = fields.CharField(max_length = 100)
    snack = fields.CharField(max_length = 100)
    calories = fields.CharField(max_length = 10)
    class Meta: 
        table = "DailyMealPlan"