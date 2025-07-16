from pydantic import BaseModel

class PowInput(BaseModel):
    x: int
    y: int

class FibInput(BaseModel):
    n: int

class FactInput(BaseModel):
    n: int

class OperationResult(BaseModel):
    operation: str
    parameters: str
    result: float
