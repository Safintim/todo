from fastapi import APIRouter

from todo.api import task_router, task_lists_router


router = APIRouter()
router.include_router(task_router)
router.include_router(task_lists_router)
