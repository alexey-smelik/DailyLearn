from fastapi import APIRouter

from app.api.groups import router as groups_router
from app.api.learning_cards import router as learning_cards_router
from app.api.newsletters import router as newsletters_router
from app.api.users import router as users_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(groups_router)
api_router.include_router(learning_cards_router)
api_router.include_router(newsletters_router)
