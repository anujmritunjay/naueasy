from fastapi import FastAPI,APIRouter, Request
from routes import user_routes
import datetime
import pytz
from models.error_model import ErrorResponse
from utilities.error_handler import UnicornException, unicorn_exception_handler
from config.database import engine, Base


startup_time: datetime = None
app = FastAPI(
    title='naueasy',
    description='This is the assignment from the nauesy.',
)

@app.exception_handler(UnicornException)
async def global_exception_handler(request, exc):
    return unicorn_exception_handler(request, exc)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    global startup_time
    current_time = datetime.datetime.now(pytz.utc)
    ist = pytz.timezone('Asia/Kolkata')

    startup_time = current_time.astimezone(ist).strftime("%d/%m/%Y, %H:%M:%S")
    print('Server Started: ', str(datetime.datetime.now()))
@app.on_event("shutdown")
async def shutdown_event():
    print('Server Shutdown: ', datetime.datetime.now())


api_router = APIRouter()
app.include_router(user_routes.router, prefix="/user", tags=["User"])



@app.get("/")
def read_root():
    return {
        "up": startup_time,
        "server": "naueasy",
        }
