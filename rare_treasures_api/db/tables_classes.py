'''SQLAlchemy tables for the database'''
from typing import Optional, Annotated
from sqlalchemy import Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.schema import ForeignKeyConstraint

Varchar50 = Annotated[str, 50]
Float2 = Annotated[float, 2]
IntPrimary = Annotated[int, mapped_column(primary_key=True)]

# pylint: disable=too-few-public-methods

class Base(DeclarativeBase):
    '''Base class for tables'''
    registry = registry(
        type_annotation_map={
            Varchar50: VARCHAR(50),
            Float2: Float(2),
        }
    )


class Shops(Base):
    '''Shops table'''
    __tablename__ = 'shops'

    shop_id:    Mapped[IntPrimary]
    shop_name:  Mapped[Varchar50]
    owner:      Mapped[Optional[Varchar50]]
    slogan:     Mapped[Optional[str]]


class Treasures(Base):
    '''Treasures table'''
    __tablename__ = 'treasures'
    __table_args__ = (
        ForeignKeyConstraint(
            ['shop_id'],
            ['shops.shop_id'],
            onupdate='CASCADE',
            ondelete='SET NULL'
        ),
    )

    treasure_id:        Mapped[IntPrimary]
    treasure_name:      Mapped[str]
    colour:             Mapped[Optional[Varchar50]]
    age:                Mapped[Optional[int]]
    cost_at_auction:    Mapped[Optional[Float2]]
    shop_id:            Mapped[Optional[int]]
