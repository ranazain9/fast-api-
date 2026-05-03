from operator import gt

from fastapi import FastAPI,Path, HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,computed_field,Field
from typing import List, Optional, Dict,Annotated,Literal
import json

app = FastAPI()

# Define the Patient model
class patient_Update(BaseModel):
        name:Optional[Annotated[str, Field(default=None)]]= None
        age: Annotated[Optional[int], Field(default=None, gt=0, lt=100)]= None 
        gender:Annotated[Optional[Literal["Male","Female","other"]], Field(default=None, description="The gender of the patient", examples=["Male"])]= None
        blood_group: Annotated[Optional[str], Field(default=None, description="The blood group of the patient", examples=["O+"])]= None
        weight:Annotated[Optional[float], Field(default=None, gt=0, description="The weight of the patient in kg", examples=[70.5])]= None
        height: Annotated[Optional[float], Field(default=None, gt=0, description="The height of the patient in cm", examples=[175.0])]= None



class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="The name of the patient", examples=["John Doe"])]
    age: Annotated[int, Field(gt=0,lt=100, description="The age of the patient", examples=[30])]
    gender: Annotated[Literal["Male","Female","other"], Field(..., description="The gender of the patient", examples=["Male"])]
    blood_group: Annotated[str, Field(..., description="The blood group of the patient", examples=["O+"])]
    weight: Annotated[float, Field(...,gt=0, description="The weight of the patient in kg", examples=[70.5])]
    height: Annotated[float, Field(...,gt=0, description="The height of the patient in cm", examples=[175.0])]
    @computed_field
    @property
    def bmi(self)-> float:
        height_in_meter = self.height / 100
        return self.weight / (height_in_meter ** 2)


# Load patients data from JSON file

def load_patients():
    with open("D:\\FAST API\\patient.json", "r") as f :
        data = json.load(f)
    return data

# Save patients data to JSON file

def save_patients(data):
    with open("D:\\FAST API\\patient.json", "w") as f:
        json.dump(data, f,)

# Root endpoint

@app.get("/")
def read_root():
    return {"message": "Patient management system API is running."}

# About endpoint

@app.get("/about")
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}

# Get all patients
@app.get("/patients")
def get_patients():
    patients = load_patients()
    return {"patients": patients}


# Get patient details by ID
@app.get("/patients/{patient_id}")
def view_patient(patient_id: str= Path(..., description="The ID of the patient to retrieve"), example="P001"):
    patients = load_patients()
    if patient_id in patients:
            return {"patient": patients[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")



# Sort patients by name or age in ascending or descending order
@app.get("/sort")
def sort_patients(sort_by: str = Query("name", description="sort on the basis of name or age"),order: str = Query("asc", description="sort in ascending or descending order")):
    
    valid_sort_fields = ["name", "age"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid fields for sort_by value. Must be one of {valid_sort_fields}.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid value for order. Must be 'asc' or 'desc'.")
    
    patients = load_patients()
    sorted_order= True if order == "desc" else False
    sorted_patients =(sorted(patients.items(), key=lambda x: x[1].get(sort_by,0), reverse=sorted_order))

    return {"sorted_patients": sorted_patients}


# Create a new patient
@app.post("/create")
def create_patient(patient:Patient)->Patient:
    #load existing patients
    data = load_patients()

# check if patient with same ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with the same ID already exists.")
    
    data[patient.id]= patient.model_dump(exclude=['id'])
    save_patients(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": patient.model_dump()})
    

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: patient_Update) -> Patient:
    data = load_patients()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    patient_data = data[patient_id]
    
    updated_patient = patient_update.model_dump(exclude_unset=True, exclude_none=True)
    print(updated_patient)
    patient_data.update(updated_patient)

    patient_pydantic=Patient(id=patient_id, **patient_data)

    updated_patient_data = patient_pydantic.model_dump(exclude=['id'])
    
    data[patient_id] = updated_patient_data
    
    save_patients(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": updated_patient_data})
  

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_patients()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")

    del data[patient_id]
    save_patients(data)

    return {"message": "Patient deleted successfully"}