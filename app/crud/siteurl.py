from app.crud.crud_base import CRUDBase

from app import models
from app import schemas
from sqlalchemy.orm import Session


class CRUDSiteUrl(CRUDBase[models.SiteUrl, schemas.SiteUrlCreate]):
    def get_by_url(self, db: Session, *, url: str) -> models.SiteUrl:
        return db.query(self.model).filter(self.model.url == url).first()

    def update_text(self, db: Session, *, url: str, text: str) -> models.SiteUrl:
        db_obj = self.get_by_url(db, url=url)
        db_obj.text = text
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_urls_by_domain(self, db: Session, *, domain: str) -> list[models.SiteUrl]:
        return (
            db.query(self.model)
            .filter(self.model.domain == domain)
            .order_by(self.model.ts_created)
            .all()
        )


siteurl = CRUDSiteUrl(models.SiteUrl)
