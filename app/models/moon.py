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
    orbital_period: Mapped[int]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moons")

    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "description": self.description,
            "orbital_period": self.orbital_period
        }

    @classmethod
    def from_dict(cls, moon_data):
        return cls(
            size=moon_data["size"],
            description=moon_data["description"],
            orbital_period=moon_data["orbital_period"]
        )