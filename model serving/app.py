from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import computed_field, Field,BaseModel
import pickle
import pandas as pd
from  typing import Literal,Annotated

app=FastAPI()


tier_1_city=['Hyderabad','Delhi', 'Chandigarh','Pune','Kolkata', 'Bangalore']
tier_2_city=[
    'Jaipur','Chennai','Indore','Mumbai','Kota',
    'Lucknow','Gaya', 'Jalandhar','Mysore', 
]
                                        

def load_model():
    with open("model.pkl","rb") as f:
       model= pickle.load(f)
    return model

class UserInput(BaseModel):    
    age:Annotated[int,Field(...,gt=0,lt=120 ,description="age of the user")]
    weight:Annotated[float,Field(...,gt=0,description="weight of the user")]
    height:Annotated[float,Field(...,gt=0,lt=2.5 ,description="height of the user")]
    income_lpa:Annotated[int,Field(...,gt=0,description="Annual salary of the user")]
    smoker:Annotated[bool,Field(... ,description="is usesr a smoker")]
    city:Annotated[str,Field(...,description="the city that user belong to")]
    occupation:Annotated[Literal['retired','freelancer','student','government_job','business_owner','unemployed','private_job'],Field(...,description="occupation of the user")]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def life_style_risk(self)->str:
        if self.bmi> 30 and self.smoker:
            return 'high risk'
        elif self.bmi >27 and self.smoker:
            return 'medium risk'
        else:
            return 'low risk'

    @computed_field
    @property
    def age_category(self)->str:
        if self.age<25:
            return 'young'
        elif self.age<40:
            return 'adult'
        else:
            return 'old'   

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_city:
            return 1
        elif self.city in tier_2_city:
            return 2
        else: 
            return 3


@app.post("/predict")
def Predict_premium(data: UserInput):
    try:
        model = load_model()

        input_df = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_category,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation,
            'lifestyleRisk': data.life_style_risk,
            'city_tier': data.city_tier,
        }])

        prediction = model.predict(input_df)[0]

        return {"predicted_category": prediction}

    except Exception as e:
        return {"error": str(e)}