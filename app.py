from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File storage configuration
BIRTHDAYS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "birthdays.json"
)


class Birthday(BaseModel):
    name: str
    date: str


def load_birthdays() -> List[dict]:
    try:
        if os.path.exists(BIRTHDAYS_FILE):
            with open(BIRTHDAYS_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading birthdays: {e}")
        return []


def save_birthdays(birthdays: List[dict]) -> None:
    try:
        with open(BIRTHDAYS_FILE, "w") as f:
            json.dump(birthdays, f, indent=2)
    except Exception as e:
        print(f"Error saving birthdays: {e}")


# Initialize birthdays from file
birthdays = load_birthdays()


@app.get("/")
async def root():
    return {"message": "Birthday Reminder API is running"}


@app.get("/birthdays")
async def get_birthdays() -> List[Birthday]:
    return birthdays


@app.post("/birthdays")
async def add_birthday(birthday: Birthday):
    try:
        # Validate date format
        datetime.strptime(birthday.date, "%Y-%m-%d")

        # Check for duplicates
        if any(b["name"].lower() == birthday.name.lower() for b in birthdays):
            raise HTTPException(
                status_code=400, detail=f"Birthday for {birthday.name} already exists"
            )

        birthdays.append(birthday.dict())
        save_birthdays(birthdays)
        return {"message": "Birthday added successfully"}
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )


@app.put("/birthdays/{name}")
async def update_birthday(name: str, birthday: Birthday):
    try:
        # Validate date format
        datetime.strptime(birthday.date, "%Y-%m-%d")

        # Find and update existing birthday
        for i, b in enumerate(birthdays):
            if b["name"].lower() == name.lower():
                birthdays[i] = birthday.dict()
                save_birthdays(birthdays)
                return {"message": "Birthday updated successfully"}

        raise HTTPException(status_code=404, detail=f"Birthday for {name} not found")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )


@app.get("/birthdays/week")
async def get_birthdays_this_week() -> List[Birthday]:
    today = datetime.now()
    week_birthdays = []

    for bday in birthdays:
        bday_date = datetime.strptime(bday["date"], "%Y-%m-%d").replace(year=today.year)
        days_diff = (bday_date - today).days
        if 0 <= days_diff <= 7:
            week_birthdays.append(bday)

    return week_birthdays


@app.get("/birthdays/month")
async def get_birthdays_this_month() -> List[Birthday]:
    today = datetime.now()
    return [
        bday
        for bday in birthdays
        if datetime.strptime(bday["date"], "%Y-%m-%d").month == today.month
    ]
