import typing as t
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.base_class import Base

ModelType = t.TypeVar("ModelType", bound=Base)
CreateSchemaType = t.TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(t.Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: t.Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args
            model (Type[ModelType]): A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: int) -> t.Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> t.List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    # def update(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: ModelType,
    #     obj_in: t.Union[UpdateSchemaType, Dict[str, Any]]
    # ):
    #     pass
