
import os
import time
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

EMAIL = "24f2009140@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-yglk52.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_headers(request, call_next):
    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    elapsed = time.perf_counter() - start
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        nums = [int(v.strip()) for v in values.split(",")]
        if not nums or any(v == "" for v in values.split(",")):
            raise ValueError
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"detail": "values must be comma-separated integers"},
        )

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
