from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/inventory")
async def get_inventory():
    
    return [
        {"id": 1, "name": "Amoxicillin 500mg", "quantity": 450, "status": "In Stock"},
        {"id": 2, "name": "Lisinopril 10mg", "quantity": 28, "status": "Low Stock"},
        {"id": 3, "name": "Atorvastatin 20mg", "quantity": 0, "status": "Expired"}
    ]