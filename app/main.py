import logging
import asyncio
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends
from app.schemas import PowInput, FibInput, FactInput, OperationResult
from app.services import calculate_pow, calculate_fibonacci, calculate_factorial
from app.firebase_client import db
from app.worker import worker, operation_queue
from app.auth import verify_api_key

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Lifespan-based startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(worker())
    yield

app = FastAPI(lifespan=lifespan)

# Caching helper
def check_cache(operation: str, parameters: str):
    query = db.collection("operations")\
              .where("operation", "==", operation)\
              .where("parameters", "==", parameters)\
              .limit(1).get()
    if query:
        return query[0].to_dict()
    return None

@app.post("/pow", response_model=OperationResult)
async def pow_op(payload: PowInput, auth=Depends(verify_api_key)):
    params = f"{payload.x},{payload.y}"
    logger.info(f"Checking cache for pow({params})")
    cached = check_cache("pow", params)
    if cached:
        logger.info("Returning cached result")
        return cached

    result = calculate_pow(payload.x, payload.y)
    entry = {
        "operation": "pow",
        "parameters": params,
        "result": result
    }
    db.collection("operations").add(entry)
    logger.info(f"Saved: {entry}")
    return entry

@app.post("/fib", response_model=OperationResult)
async def fib_op(payload: FibInput, auth=Depends(verify_api_key)):
    params = str(payload.n)
    logger.info(f"Checking cache for fib({params})")
    cached = check_cache("fib", params)
    if cached:
        logger.info("Returning cached result")
        return cached

    result = calculate_fibonacci(payload.n)
    entry = {
        "operation": "fib",
        "parameters": params,
        "result": result
    }
    db.collection("operations").add(entry)
    logger.info(f"Saved: {entry}")
    return entry

@app.post("/fact", response_model=OperationResult)
async def fact_op(payload: FactInput, auth=Depends(verify_api_key)):
    params = str(payload.n)
    logger.info(f"Checking cache for fact({params})")
    cached = check_cache("fact", params)
    if cached:
        logger.info("Returning cached result")
        return cached

    result = calculate_factorial(payload.n)
    entry = {
        "operation": "fact",
        "parameters": params,
        "result": result
    }
    db.collection("operations").add(entry)
    logger.info(f"Saved: {entry}")
    return entry

@app.post("/task")
async def async_task(operation: str, parameters: str, auth=Depends(verify_api_key)):
    await operation_queue.put({
        "operation": operation,
        "parameters": parameters,
        "logger": logger
    })
    logger.info(f"Task queued: {operation}({parameters})")
    return {"status": "Task queued"}

@app.get("/history", response_model=List[OperationResult])
async def get_history(auth=Depends(verify_api_key)):
    docs = db.collection("operations").order_by("parameters").stream()
    results = [doc.to_dict() for doc in docs]
    logger.info(f"Returned {len(results)} operations from history")
    return results
