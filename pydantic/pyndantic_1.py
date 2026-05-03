from pydantic import BaseModel,EmailStr,Field
from typing import List, Optional, Dict
class Patient(BaseModel):
    id: str
    name: str=Field(max_length=100, description="The name of the patient")
    email: EmailStr
    age: int
    weight: float 
    married: bool 
    contact_details: Dict[str, str]
    medical_history: List[str]
    allergies: Optional[List[str]] = None

def insert_patient(patient: Patient) -> Patient:
   print(patient.id)
   print(patient.name)
   print(patient.email)
   print(patient.age)
   print(patient.weight)
   print(patient.married)
   print(patient.contact_details)
   print(patient.medical_history)
   print(patient.allergies)   
   print("Patient inserted successfully.")

def update_patient(patient: Patient) -> Patient:
   print(patient.id)
   print(patient.name)
   print(patient.email)
   print(patient.age)
   print(patient.weight)
   print("Patient updated successfully.")

patient_data = {"id": "P001", "name": "John Doe", "email": "john.doe@example.com", "age": 30, "weight": 70.5, "married": True, "contact_details": { "phone": "123-456-7890"}, "medical_history": ["Hypertension", "Diabetes"], "allergies": ["Peanuts", "Shellfish"]}
patient = Patient(**patient_data)
insert_patient(patient)
update_patient(patient)