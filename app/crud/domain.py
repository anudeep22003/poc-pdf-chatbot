from app.crud.crud_base import CRUDBase

from app import models
from app import schemas
from sqlalchemy.orm import Session


class CRUDDomain(CRUDBase[models.Domain, schemas.DomainCreate]):
    def get_domain_by_name(self, db: Session, *, domain: str) -> models.Domain:
        return db.query(self.model).filter(self.model.domain == domain).first()


domain = CRUDDomain(models.Domain)
