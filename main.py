# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import listings, users
from controllers import inquiries
# from controllers import auctions, inquiries 

app = FastAPI()

# ✅ Allow your React dev server(s) to call the API
origins = [
    "http://localhost:5173",
    # Later, add your deployed frontend origin, e.g.:
    # "https://your-frontend.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Which sites can call this API
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # Allow all headers (e.g., Content-Type, Authorization)
    # NOTE: We are NOT using credentials in this simple lesson,
    # so we are not setting allow_credentials.
)

app.include_router(users.router)
app.include_router(listings.router)
app.include_router(inquiries.router)

@app.get("/")
def home():
    return {"message": "Welcome to Aurevia Car Auction API"}