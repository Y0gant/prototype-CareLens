from pydantic import BaseModel


class OperationsAnswer(BaseModel):
    answer: str
    department: str
    supporting_metric: str
