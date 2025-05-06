from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .planets import Planet

class Moon(db.Model):
    id: Mapped[int] =  mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[int]
    description: Mapped[str]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planets.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moon")