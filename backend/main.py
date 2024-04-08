from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (change as needed)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Add OPTIONS method
    allow_headers=["*"],
)

class UserRegistration(BaseModel):
    username: str
    password: str
    confirmPassword: str
    email: str
    phoneNumber: str

@app.post('/register')
async def register_user(user_data: UserRegistration):
    # Check if username, email, and phone number are already taken
    with open('users.json', 'r') as file:
        existing_users = [json.loads(line) for line in file if line.strip()]
        for existing_user in existing_users:
            if existing_user["username"] == user_data.username:
                raise HTTPException(status_code=400, detail="Username already exists")
            if existing_user["email"] == user_data.email:
                raise HTTPException(status_code=400, detail="Email already exists")
            if existing_user["phoneNumber"] == user_data.phoneNumber:
                raise HTTPException(status_code=400, detail="Phone number already exists")
    
    if len(user_data.username) <= 5:
        raise HTTPException(status_code=400, detail="Username must be more than 5 characters")
    if len(user_data.password) <= 6:
        raise HTTPException(status_code=400, detail="Password must be more than 6 characters")
    if user_data.password != user_data.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if not user_data.phoneNumber.isdigit() or len(user_data.phoneNumber) != 11:
        raise HTTPException(status_code=400, detail="Phone number must have exactly 11 digits")
    
    with open('users.json', 'a') as file:
        json.dump(user_data.dict(), file)
        file.write('\n')
    return {"message": "User registered successfully"}
