from pydantic import BaseModel, Field, field_validator, validator, EmailStr,model_validator,computed_field
from typing import List, Optional, Dict,Annotated

class Patient(BaseModel):
    id: str
    name: str = Field(max_length=100, description="The name of the patient")
    email: EmailStr
    age: int
    weight: float 
    height: float
    married: bool 
    contact_details: Dict[str, str]
    medical_history: List[str]
    allergies: Optional[List[str]] = None

    @computed_field
    @property   
    def bmi(self) -> float:
        height_in_meters = self.height / 100
        return round(self.weight / (height_in_meters ** 2), 2)

def patient_view(patient):
    print(f"Patient ID: {patient.id}")
    print(f"Name: {patient.name}")
    print(f"Email: {patient.email}")
    print(f"BMI: {patient.bmi}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight}")
    print(f"Height: {patient.height}")
    print(f"Married: {patient.married}")
    print(f"Contact Details: {patient.contact_details}")
    print(f"Medical History: {patient.medical_history}")
    print(f"Allergies: {patient.allergies}")


patient_data = {"id": "P001", "name": "John Doe", "email": "john.doe@superior.edu.pk", "age": 30, "weight": 70.5, "height": 175.0, "married": True, "contact_details": { "phone": "123-456-7890"}, "medical_history": ["Hypertension", "Diabetes"], "allergies": ["Peanuts", "Shellfish"]}

patient1 = Patient(**patient_data)
patient_view(patient1)