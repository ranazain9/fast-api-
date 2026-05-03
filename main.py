from fastapi import FastAPI,Path, HTTPException,Query
import json

app = FastAPI()


def load_patients():
    with open("D:\\FAST API\\patient.json", "r") as f :
        data = json.load(f)
    return data

@app.get("/")
def read_root():
    return {"message": "Patient management system API is running."}

@app.get("/about")
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}

@app.get("/patients")
def get_patients():
    patients = load_patients()
    return {"patients": patients}

@app.get("/patients/{patient_id}")
def view_patient(patient_id: str= Path(..., description="The ID of the patient to retrieve"), example="P001"):
    patients = load_patients()
    if patient_id in patients:
            return {"patient": patients[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")

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