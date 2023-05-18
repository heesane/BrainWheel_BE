# 가게측에서 사용하는 API를 정의한 파일입니다.

from typing import Optional
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import FileResponse
from influxdb import client as influxdb
import pymysql
from pydantic import BaseModel
import os
import datetime


import models
import tool

from .food import router as food_router
from .ingredient import router as ingredient_router
from .table import router as table_router

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

router.include_router(food_router)
router.include_router(ingredient_router)
router.include_router(table_router)

@router.get("/")
async def restaurant_mainpage():
    return "Restaurant Router"
