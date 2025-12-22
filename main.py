# main.py
from fastapi import FastAPI
from controllers import listings, users
from controllers import inquiries
# from controllers import auctions, inquiries 

app = FastAPI()


app.include_router(users.router)
app.include_router(listings.router)
app.include_router(inquiries.router)

@app.get("/")
def home():
    return {"message": "Welcome to Aurevia Car Auction API"}