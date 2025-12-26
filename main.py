from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 1. Створюємо додаток (ЦЬОГО РЯДКА ЗАРАЗ НЕ ВИСТАЧАЄ)
app = FastAPI()

# 2. Налаштовуємо "місток" для фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Модель даних
class Drug(BaseModel):
    name: str
    quantity: int
    status: str

# 4. Твоя база даних у пам'яті
inventory = [
    {"id": 1, "name": "Amoxicillin 500mg", "quantity": 450, "status": "In Stock"},
    {"id": 2, "name": "Lisinopril 10mg", "quantity": 28, "status": "Low Stock"},
]

# 5. Твої маршрути (Endpoints)
@app.get("/api/inventory")
async def get_inventory():
    return inventory

@app.post("/api/inventory")
async def add_drug(drug: Drug):
    new_drug = {
        "id": len(inventory) + 1,
        "name": drug.name,
        "quantity": drug.quantity,
        "status": drug.status
    }
    inventory.append(new_drug)
    return new_drug