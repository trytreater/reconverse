from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# ---------------------------- Email ------------------------------------- #
class Person(BaseModel):
    name: str = Field(..., description="The name of the person")
    company: str = Field(..., description="Where the person works")
    job_title: Optional[List[str]] = Field(..., description="The person's job title in the company")
    responsibilities: Optional[Dict] = Field("The person's responsibilities")
    experience: List[str] = Field(..., description="Relevant experience and abilities to their role")
    email: str = Field(..., description="The person's email address")

class Email(BaseModel):
    sender: Person = Field(..., description="The person who sent the email")
    recipients: List[Person] = Field(..., description="The addresses of of the people receiving the email")
    cc:  Optional[List[Person]] = Field(..., description="People who were cc'd in the email")
    bcc:  Optional[List[Person]] = Field(..., description="People who were bcc'd in the email")
    topic: str = Field(..., description="The topic of the email")
    summary: str = Field(..., description="The summary of the email")

