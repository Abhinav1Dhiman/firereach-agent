from pydantic import BaseModel

class OutreachRequest(BaseModel):
    company: str
    icp: str
    email: str