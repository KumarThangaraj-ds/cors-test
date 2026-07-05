from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid, time

app = FastAPI(title="CORS GA2")

# These are frontend origins allowed to call this API from browser
origins = [
    "https://dash-650zd5.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],          # Do not use ["*"] for real apps with login/cookies
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    
    start_time = time.perf_counter()

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

    return response

def GetResponseJson (number_list):
    count = 0 # it counts the numbers in the list
    min = 0 
    max = 0
    sum = 0
    mea = 0
    for num in number_list:
        if count == 0:
            min = num

        if (min > num):
            min = num
        if (max < num):
            max = num
        
        sum = sum + num
        
        count = count+1

    mea = round (sum/count, 2)

    responsejson = {"email":"23ds1000074@ds.study.iitm.ac.in", "count":count, "sum" : sum, "min" : min, "max" : max, "mean" : mea}

    return responsejson

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stats")
def stats(values: str | None = None):

    if values:
        number_list = [int(num) for num in values.split(",")]
        response_json = GetResponseJson (number_list)
        return response_json

    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    return {
        "received": payload,
        "label": "demo"
    }

