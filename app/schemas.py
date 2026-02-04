from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    email: str
    phoneNum: str
    description: str
    budget: str | None = None
    deadline: str | None = None



# # schemas.py
# from pydantic import BaseModel, EmailStr, validator
# from typing import Optional
# from datetime import datetime

# class ProjectRequestBase(BaseModel):
#     name: str
#     email: EmailStr
#     phone: Optional[str] = None
#     company: Optional[str] = None
#     project_type: str
#     budget: str
#     timeline: str
#     description: str
    
#     @validator('phone')
#     def validate_phone(cls, v):
#         if v and not v.replace(' ', '').replace('-', '').replace('+', '').isdigit():
#             raise ValueError('شماره تلفن نامعتبر است')
#         return v

# class ProjectRequestCreate(ProjectRequestBase):
#     pass

# class ProjectRequestUpdate(BaseModel):
#     status: str

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class AdminUserCreate(BaseModel):
#     username: str
#     password: str
#     email: Optional[EmailStr] = None