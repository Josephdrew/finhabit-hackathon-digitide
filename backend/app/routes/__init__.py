from fastapi import APIRouter
from app.routes import net_worth
from app.routes import budget
from app.routes import banner
from app.routes import goal
from app.routes import notification

api_router = APIRouter()

api_router.include_router(net_worth.router, tags=["Net Worth"])
api_router.include_router(budget.router, tags=["Budget"])
api_router.include_router(banner.router, tags=["Banner"])
api_router.include_router(goal.router, tags=["Goal"])
api_router.include_router(notification.router, tags=["Notification"])