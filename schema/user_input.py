
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier_1_cities, tier_2_cities


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt= 0, lt = 120, description ='Age of the user') ]
    weight: Annotated[float, Field(..., gt= 0, description ='your weight') ]
    height:  Annotated[float, Field(..., gt= 0, description ='your HEIGHT') ]
    city:  Annotated[str, Field(..., description='your city')]
    income_lpa:  Annotated[float, Field(..., gt= 0, description ='Annula salary in lakhs') ]
    smoker:  Annotated[bool, Field(..., description ='Do you smoke?') ]
    occupation:  Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description ='occupation of the user') ]
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v
    
    @computed_field
    @property
    def bmi(self)-> float:
        return self.weight /(self.height ** 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45: 
            return "adult"
        elif self.age < 60:
            return "middle aged"
        return "senior citizen"
    
    @computed_field
    @property

    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def get_city_tier(self) -> str:
        if self.city in tier_1_cities:
            return '1'
        elif self.city in tier_2_cities:
            return '2'
        return '3'