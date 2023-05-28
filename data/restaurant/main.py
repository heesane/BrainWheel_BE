import fastapi
from starlette.middleware.cors import CORSMiddleware


from routes.user import user_router
from routes.food import food_router
from routes.ingredient import ingredient_router

app = fastapi.FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(food_router.router)


