from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .moon import Moon

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    atmosphere: Mapped[str]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "atmosphere": self.atmosphere,
            "moons": [moon.to_dict() for moon in self.moons]
        }

    @classmethod
    def from_dict(cls, planet_data):
        return cls(
            name=planet_data["name"],
            description=planet_data["description"],
            atmosphere=planet_data["atmosphere"],
            moons=planet_data.get("moons", [])
        )
    
# class Planet: 
#     def __init__(self, id, name, description, atmosphere):
#         self.id = id 
#         self.name = name
#         self.description = description
#         self.atmosphere = atmosphere

# planets = [
#     Planet(1, "Mercury", "Highly eccentric orbit", "thin"),
#     Planet(2, "Venus", "Slightly smaller than Earth", "thick"),
#     Planet(3, "Earth", "Third planet from the Sun", "middle"),
#     Planet(4, "Mars", "Nicknamed the Red Planet", "thin"),
#     Planet(5, "Jupiter", "Largest planet", "very thick"),
#     Planet(6, "Saturn", "Has many moons", "thick"),
#     Planet(7, "Uranus", "Ice giant", "thick"),
#     Planet(8, "Neptune", "Dark, cold planet", "thick")
# ]