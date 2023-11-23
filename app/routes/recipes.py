from fastapi import APIRouter, HTTPException, Security
from app.schemas.recipes import Recipe, RecipeSearchResponse, NutInfo


from typing import Annotated
from app.services.auth.utils import get_current_user
#from app.models.recipes import Recipe, Recipe as RecipeModel
from app.utils.response import responses
from app.utils.exception import ShapeShyftException
from app.services.auth import hash_password
from fatsecret import Fatsecret
from app.models.user import UserAccount
from decimal import Decimal

fs = Fatsecret("0047da412ebd469c9dd1895c7d3159d8", "2f91d6bcbaa94e72bea327eb4d6b0546")

router = APIRouter(
    tags=["Recipes"],
)

@router.get("/search", response_model=RecipeSearchResponse, responses=responses)
async def search_recipe_database(
    query: str, current_user: UserAccount = Security(get_current_user)
):
    """
    This endpoint searches for recipes based on the query string
    """
    recipes = fs.recipes_search(query)
    recipes_array = []
    for recipe in recipes:

        nut_info = NutInfo(
            cals=recipe["recipe_nutrition"]["calories"],
            carbs=recipe["recipe_nutrition"]["carbohydrate"],
            fat=recipe["recipe_nutrition"]["fat"],
            protein=recipe["recipe_nutrition"]["protein"],
        )
        _recipe = Recipe(
                name=recipe["recipe_name"],
                image=recipe.get("recipe_image", ""),
                description=recipe["recipe_description"],
                nutInfo=nut_info,
            )

        if recipe.get("recipe_image"):
            recipes_array.append(_recipe)
        
        if recipe.get("recipe_ingredients"):
            print(recipe.get("recipe_ingredients"))

    return RecipeSearchResponse(items=recipes_array)
        