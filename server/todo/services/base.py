from fastapi import Depends, HTTPException
from fastapi import status
from pydantic import BaseModel

from todo.database import Session, get_session
from todo import models


class BaseService:
    model = models.Base

    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def _get(self, item_id: int) -> model:
        item = self.session.query(self.model).filter_by(id=item_id).first()

        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return item

    def first(self) -> model:
        return self.session.query(self.model).first()

    def get(self, item_id: int) -> model:
        return self._get(item_id)

    def get_all(self) -> list[model]:
        return self.session.query(self.model).all()

    def create(self, item_data: BaseModel) -> model:
        task = self.model(**item_data.dict())
        self.session.add(task)
        self.session.commit()
        return task

    def update(self, item_id: int, item_data: BaseModel) -> model:
        task = self._get(item_id)
        for field, value in item_data:
            setattr(task, field, value)
        self.session.commit()
        return task

    def delete(self, item_id: int) -> None:
        task = self._get(item_id)
        self.session.delete(task)
        self.session.commit()
