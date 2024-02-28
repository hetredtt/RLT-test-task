from pydantic import BaseModel

class Req(BaseModel):
    dt_from: str
    dt_upto: str 
    group_type: str