from pydantic import BaseModel, Field, field_validator, validator, EmailStr
from typing import List, Optional, Dict,Annotated

class Patient(BaseModel):
    id: str
    name: str = Field(max_length=100, description="The name of the patient")
    email: EmailStr
    age: int
    weight: float 
    married: bool 
    contact_details: Dict[str, str]
    medical_history: List[str]
    allergies: Optional[List[str]] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_value=["superior.edu.pk","jsbank.com",]
        domain = value.split('@')[-1]
        if domain not in valid_value:
            raise ValueError(f"Email domain must be one of {valid_value}.")
        return value

def patient_view(patient):
    print(f"Patient ID: {patient.id}")
    print(f"Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}")
    print(f"Married: {patient.married}")
    print(f"Contact Details: {patient.contact_details}")
    print(f"Medical History: {patient.medical_history}")
    print(f"Allergies: {patient.allergies}")


patient_data = {"id": "P001", "name": "John Doe", "email": "john.doe@superior.edu.pk", "age": 30, "weight": 70.5, "married": True, "contact_details": { "phone": "123-456-7890"}, "medical_history": ["Hypertension", "Diabetes"], "allergies": ["Peanuts", "Shellfish"]}

patient1 = Patient(**patient_data)
patient_view(patient1)