import asyncio
from app.services import calculate_pow, calculate_fibonacci, calculate_factorial
from app.firebase_client import db

operation_queue = asyncio.Queue()


async def worker():
    while True:
        task = await operation_queue.get()
        operation = task["operation"]
        parameters = task["parameters"]
        logger = task["logger"]

        logger.info(f"Worker processing: {operation}({parameters})")

        if operation == "pow":
            x, y = map(int, parameters.split(","))
            result = calculate_pow(x, y)
        elif operation == "fib":
            result = calculate_fibonacci(int(parameters))
        elif operation == "fact":
            result = calculate_factorial(int(parameters))
        else:
            result = None

        if result is not None:
            entry = {
                "operation": operation,
                "parameters": parameters,
                "result": result
            }
            db.collection("operations").add(entry)
            logger.info(f"Worker saved: {entry}")

        operation_queue.task_done()
