from pydantic import BaseModel, Field, field_validator, validator, EmailStr,model_validator,computed_field
from typing import List, Optional, Dict,Annotated


class address_model(BaseModel):
    street: str
    city: str
    state: str
    zip_code: int

class patient_details(BaseModel):
    id: str
    name: str = Field(max_length=100, description="The name of the patient")
    email: EmailStr
    age: int
    address: address_model

def patient_view(patient):
    print(f"Patient ID: {patient.id}")
    print(f"Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"Age: {patient.age}")
    print(f"Address: {patient.address.street}, {patient.address.city}, {patient.address.state} - {patient.address.zip_code}")


patient_data = {"id": "P001", "name": "John Doe", "email": "john.doe@superior.edu.pk", "age": 30, "address": {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip_code": 12345}}

patient1 = patient_details(**patient_data)
patient_view(patient1)