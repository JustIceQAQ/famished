import asyncio
import datetime
import os
from collections import ChainMap
import pathlib
import json

import httpx
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from helper.breakfast_process import (DailyBreakfast, OnlyToast, YosSoyMilk, BrunchFirst, McdonaldBreakfast)
from helper.lunch_dinner_process import (Mini12, McdonaldFullMenu, SuShiTakeOut, Omrice888, TonGanCurry)
from debug_toolbar.middleware import DebugToolbarMiddleware

ROOT_DIR = pathlib.Path(__file__).resolve(strict=True).parent

app = FastAPI(debug=False)
app.add_middleware(DebugToolbarMiddleware)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def root(request: Request):
    temp_json_file = TempJsonFile(overwrite=False)
    if temp_json_file.is_expired:
        async with httpx.AsyncClient() as client:
            breakfast_task = [
                DailyBreakfast(use_client=client).run(),
                OnlyToast(use_client=client).run(),
                YosSoyMilk(use_client=client).run(),
                BrunchFirst(use_client=client).run(),
                McdonaldBreakfast(use_client=client).run(),
            ]
            lunch_dinner_task = [
                Mini12(use_client=client).run(),
                McdonaldFullMenu(use_client=client).run(),
                SuShiTakeOut(use_client=client).run(),
                Omrice888(use_client=client).run(),
                TonGanCurry(use_client=client).run(),
            ]
            breakfast_gather = asyncio.gather(*breakfast_task)
            lunch_dinner_gather = asyncio.gather(*lunch_dinner_task)
            breakfast, lunch_dinner = await asyncio.gather(breakfast_gather, lunch_dinner_gather)

            meal = {
                "breakfast": dict(ChainMap(*breakfast)),
                "lunch_dinner": dict(ChainMap(*lunch_dinner))
            }
            temp_json_file.commit(meal)
    meal = temp_json_file.read()
    return templates.TemplateResponse(
        'index.html',
        {"request": request, "datas": meal}
    )


@app.get("/file")
async def file():
    temp_json_file = TempJsonFile()
    return {"qaq": temp_json_file.read()}


class TempJsonFile:
    def __init__(self, filename="data.json", path="static", overwrite=False):
        self.filename = filename
        self.data_path = ROOT_DIR / path / filename
        if not self.data_path.is_file():
            with open(self.data_path, "a", encoding="utf-8") as f:
                pass
        self.overwrite = overwrite

    @property
    def is_expired(self):
        if self.overwrite:
            return self.overwrite

        runtime_now = (
            datetime.datetime.utcnow()
                .replace(tzinfo=datetime.timezone.utc)
                .astimezone(datetime.timezone(datetime.timedelta(hours=8)))
        )
        edit_time = (
            datetime.datetime.fromtimestamp(self.data_path.stat().st_mtime, tz=datetime.timezone.utc)
                .astimezone(datetime.timezone(datetime.timedelta(hours=8)))
        )
        timedelta = runtime_now - edit_time

        return bool(timedelta.days)

    def read(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            datas = json.load(f)
        return datas

    def commit(self, _dict):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(_dict, f, indent=2)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=8002)), log_level="info")
