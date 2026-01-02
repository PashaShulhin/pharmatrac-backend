from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Dict, Any
from pydantic import BaseModel

# 1. Ініціалізація додатка (МАЄ БУТИ ТУТ, щоб працювали декоратори нижче)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Налаштування бази даних
SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Моделі даних
class DrugDB(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    expiryDate = Column(String)
    location = Column(String)
    status = Column(String)
    serialNumber = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic модель для логіна
class LoginData(BaseModel):
    username: str
    password: str

# Dependency для отримання сесії БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. Маршрути для авторизації

@app.post("/api/login")
def login(data: LoginData):
    # Користувачі для MVP
    users = {
        "admin": {"password": "123", "role": "admin"},
        "user": {"password": "456", "role": "provider"}
    }
    
    user = users.get(data.username)
    if user and user["password"] == data.password:
        return {"status": "success", "role": user["role"], "username": data.username}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 5. Маршрути для інвентаризації (CRUD)

@app.get("/api/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return db.query(DrugDB).all()

@app.post("/api/inventory")
def add_drug(drug: Dict[Any, Any], db: Session = Depends(get_db)):
    new_drug = DrugDB(
        name=drug.get("name"),
        quantity=int(drug.get("quantity", 0)),
        expiryDate=drug.get("expiryDate"),
        location=drug.get("location"),
        status=drug.get("status", "in-stock"),
        serialNumber=drug.get("serialNumber")
    )
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)
    return new_drug

@app.put("/api/inventory/{item_id}")
def update_item(item_id: int, updated_data: Dict[Any, Any], db: Session = Depends(get_db)):
    db_item = db.query(DrugDB).filter(DrugDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in updated_data.items():
        if hasattr(db_item, key):
            setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/inventory/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(DrugDB).filter(DrugDB.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"ok": True}
    raise HTTPException(status_code=404, detail="Not found")