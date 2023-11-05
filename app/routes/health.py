from fastapi import APIRouter, HTTPException, Security
from app.models.water import WaterEntries
from app.schemas.water import Create_wEntry, Edit_wEntry, wEntryResponse
from app.models.user import UserAccount
from app.services.auth.utils import get_current_user
from app.utils.exception import ShapeShyftException
from datetime import date,datetime

from app.utils.response import responses
from app.utils.exception import ShapeShyftException

router = APIRouter(
    tags=["Health profile"],
)

#Water
@router.post("/createWater", response_model=wEntryResponse,responses=responses)
async def create_water(data: Create_wEntry, current_user: UserAccount = Security(get_current_user)):
    data = data.dict()
    if(await WaterEntries.exists(email=current_user.email, date=date.today())==False):
        water = await WaterEntries.create(**data, email=current_user.email, date=date.today())
        return water
    else:
        raise ShapeShyftException("E1024", 400)
    
    
    
    
    
#Get all the entries of water associated with the account.
@router.get("/getWater", response_model=list[wEntryResponse], responses=responses)
async def get_water(current_user: UserAccount = Security(get_current_user)):
    waterLog = await WaterEntries.all().filter(email=current_user.email)
    return waterLog 

#Update the water entry for current date.
@router.put("/updateWater", response_model=wEntryResponse, responses=responses)
async def update_water_amount(data : int, current_user: UserAccount = Security(get_current_user)):
    hydration_log = await WaterEntries.get(email=current_user.email,date=date.today())
    hydration_log.amt = data
    await hydration_log.save()

    return hydration_log