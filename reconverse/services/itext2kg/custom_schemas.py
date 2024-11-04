from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# ---------------------------- Memo ------------------------------------- #

from typing import List
from pydantic import BaseModel, Field

class Employee(BaseModel):
    name: str = Field(description="The name of the employee.")
    title: str = Field(description="The job title of the employee.")
    specialty: str = Field(description="The employee's area of expertise or specialization.")
    affiliation: str = Field(description="The company or store where the employee works, linking them to a specific brand or retail location.")

class ProductLine(BaseModel):
    name: str = Field(description="The name of the product line.")
    features: List[str] = Field(description="A list of features or attributes that describe the product line.")

class Store(BaseModel):
    name: str = Field(description="The name of the retail store.")
    location: str = Field(description="The location of the store.")
    manager: Employee = Field(description="The store manager responsible for the day-to-day operations.")
    deputy_manager: Employee = Field(description="The deputy store manager who assists the store manager.")
    product_lines: List[ProductLine] = Field(description="Product lines that the store currently stocks, aiming to include or exclude new products.")

class Brand(BaseModel):
    name: str = Field(description="The name of the brand.")
    manager: Employee = Field(description="The brand manager who oversees the brand's market presence.")
    product_lines: List[ProductLine] = Field(description="A list of product lines offered by the brand.")
    sales_director: Employee = Field(description="The sales director responsible for strategic sales initiatives and negotiations with retail stores.")

class Memo(BaseModel):
    brand: Brand = Field(description="The brand seeking to place their products in retail stores.")
    target_store: Store = Field(description="The retail store targeted for product placement.")
    intent: str = Field(description="The intention behind the interaction, e.g., to introduce a new product line to the store.")
    involved_employees: List[Employee] = Field(description="A list of all employees involved in the interaction from both the brand and the retail store.")


# ---------------------------- Email ------------------------------------- #
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class Contact(BaseModel):
    name: str = Field(description="The full name of the contact person.")
    email: str = Field(description="The email address of the contact person.")
    phone: Optional[str] = Field(None, description="The phone number of the contact person, if available.")

class ContentDetail(BaseModel):
    content_type: str = Field(description="The type of content shared in the email, such as 'Meeting Request', 'Product Proposal', 'Project Update', etc.")
    description: Optional[str] = Field(None, description="A brief description of the content, if necessary.")
    documents: Optional[List[str]] = Field(None, description="List of documents or attachments mentioned or included in the email.")

class MeetingDetails(BaseModel):
    meeting_type: Optional[str] = Field(None, description="Type of meeting, e.g., in-person, video call.")
    date: Optional[str] = Field(None, description="Proposed or scheduled date for the meeting.")
    location: Optional[str] = Field(None, description="Location for the meeting, if applicable.")
    agenda: Optional[str] = Field(None, description="Agenda or purpose of the meeting.")

class EmailInteraction(BaseModel):
    subject: str = Field(description="The subject of the email, summarizing the purpose of the communication.")
    sender: Contact = Field(description="Contact details of the sender.")
    recipients: List[Contact] = Field(description="List of primary recipients of the email.")
    cc: Optional[List[Contact]] = Field(None, description="List of contacts who are copied on the email.")
    content_details: ContentDetail = Field(description="Details about the main content of the email.")
    meeting_details: Optional[MeetingDetails] = Field(None, description="Detailed information about a meeting if the email pertains to one.")
    additional_notes: Optional[str] = Field(None, description="Any additional notes or comments mentioned in the email.")

