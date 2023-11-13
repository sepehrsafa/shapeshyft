from fastapi import APIRouter, HTTPException, Security
from app.models.health import WaterEntries, SleepEntries
from app.schemas.health import wEntry, wEntryResponse, wGetResponse, sEntry, sEntryResponse, tipResponse
from app.models.user import UserAccount
from app.services.auth.utils import get_current_user
from app.utils.exception import ShapeShyftException
from datetime import date,datetime, time
from  app.services.recommender.recommend import water_rec,sleep_rec,bmi_rec

from app.utils.response import responses
from app.utils.exception import ShapeShyftException


router = APIRouter(
    tags=["Health profile"],
)

#Get all the entries of water associated with the account.
@router.get("/getWater", response_model=list[wGetResponse], responses=responses)
async def get_water(current_user: UserAccount = Security(get_current_user)):
    """
    This endpoint returns list of water entries for the user
    """
    waterLog = await WaterEntries.all().filter(user=current_user)
    return waterLog 

#Update the water entry for current date.
@router.post("/ceWater", response_model=wEntryResponse, responses=responses)
async def create_or_edit_water_amount(data: wEntry, current_user: UserAccount = Security(get_current_user)):
    """
    This endpoint is used to create/edit a water entry for today's date
    """
    hydration_log, created = await WaterEntries.get_or_create(user=current_user,date=date.today(),defaults={"amt": 0})
    hydration_log.amt = data.amt
    await hydration_log.save()

    return hydration_log

#get sleep log based on date
@router.get("/getSleep", response_model=list[sEntryResponse], responses=responses)
async def get_sleep(date: date, current_user: UserAccount=Security(get_current_user)):
    """
    This endpoint returns the list of sleep entries for the user
    """
    sleep_entry = await SleepEntries.all.filter(user=current_user)
    return sleep_entry

#create sleep entry for today
@router.post("/ceSleep", response_model=sEntryResponse, responses=responses)
async def create_or_edit_sleep(data : sEntry, current_user: UserAccount = Security(get_current_user)):
    """
    This endpoint is used to create/edit a sleep entry for today's date,
    Time format should be something like "12:04PM" for the strings
    """
    sleep_entry, created = await SleepEntries.get_or_create(user=current_user,date=date.today(), defaults={'s_time': time.min, 'e_time': time.min, 'h_slept': 0})
    #expected format to be something like 12:04PM
    string1=data.s_time +" "+ date.today().strftime("%Y-%m-%d")
    string2=data.e_time +" "+ date.today().strftime("%Y-%m-%d")
    start = datetime.strptime(string1,'%I:%M%p %Y-%m-%d')
    end = datetime.strptime(string2,'%I:%M%p %Y-%m-%d')

    #calculate hours of sleep in float val
    s=start.time()
    e=end.time()
    duration=end-start
    duration_s=duration.total_seconds()
    hours=duration_s/3600

    #PM to AM check
    if(hours<0):
        hours_in=24+hours
    else:
        hours_in=hours

    sleep_entry.s_time=s
    sleep_entry.e_time=e
    sleep_entry.h_slept=hours_in
    await sleep_entry.save()

    return sleep_entry

@router.get("/tips",response_model=tipResponse, responses=responses)
async def tips(height:float, weight:float, current_user: UserAccount = Security(get_current_user)):
    s_entry, created= await SleepEntries.get_or_create(user=current_user,date=date.today(),defaults={'s_time': time.min, 'e_time': time.min, 'h_slept': 0})
    w_entry, created2= await WaterEntries.get_or_create(user=current_user,date=date.today(),defaults={"amt":0})
    rec1={
        "w_rec": water_rec(w_entry.amt),
        "s_rec": sleep_rec(18,s_entry.h_slept) 
    }
    rec2=bmi_rec(height,weight)
    tips={**rec1,**rec2}
    return tips