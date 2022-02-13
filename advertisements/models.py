from sqlalchemy import Integer, String, Column, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship, Session
from datetime import datetime

# from sqlalchemy.dialects.sqlite import UU
# from sqlalchemy.orm import relationship

from database import Base


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)  # TODO: postgresql UUID?
    title = Column(String, index=True)
    description = Column(String)  # TODO: length
    date_created = Column(DateTime, index=True)
    date_modified = Column(DateTime, index=True)
    date_start = Column(DateTime, index=True)
    date_end = Column(DateTime, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", lazy="joined", back_populates="advertisements")

    content = Column(Text)  # TODO: specify content type

    views = Column(Integer, default=0, index=True)
    # published

    @property
    def visible(self):
        date = datetime.now()
        return self.date_start <= date

    __table_args__ = (
        Index("advertisements_popular_in_category", "category_id", "views"),
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String, index=True
    )  # TODO: add slug and visual name and unique on slug
    parent_id = Column(Integer, ForeignKey("categories.id"))

    parent = relationship("Category", back_populates="subcategories", remote_side=[id])

    subcategories = relationship("Category", back_populates="parent")

    advertisements = relationship("Advertisement", back_populates="category")

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    @property
    def advertisements_count_active(self):
        date = datetime.now()
        return (
            Session.object_session(self)
            .query(Advertisement)
            .with_parent(self)
            .filter(
                Advertisement.date_start <= date,
                Advertisement.date_end >= date,
            )
            .count()
        )

    @property
    def advertisements_count_archive(self):
        date = datetime.now()
        return (
            Session.object_session(self)
            .query(Advertisement)
            .with_parent(self)
            .filter(
                Advertisement.date_start <= date,
                Advertisement.date_end < date,
            )
            .count()
        )


# class AdvertisementViewCount(Base):
#     __tablename__ = "advertisement_views"
#     advertisement_id = Column(Integer, ForeignKey("Advertisement.id"), primary_key=True, index=True)
#     advertisement = relationship("Advertisement")

#     views = Column(Integer, default=0)
