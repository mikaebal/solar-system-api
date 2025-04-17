class Planet: 
    def __init__(self, id, name, description, atmosphere):
        self.id = id 
        self.name = name
        self.description = description
        self.atmosphere = atmosphere

planets = [
    Planet(1, "Mercury", "Highly eccentric orbit", "thin"),
    Planet(2, "Venus", "Slightly smaller than Earth", "thick"),
    Planet(3, "Earth", "Third planet from the Sun", "middle"),
    Planet(4, "Mars", "Nicknamed the Red Planet", "thin"),
    Planet(5, "Jupiter", "Largest planet", "very thick"),
    Planet(6, "Saturn", "Has many moons", "thick"),
    Planet(7, "Uranus", "Ice giant", "thick"),
    Planet(8, "Neptune", "Dark, cold planet", "thick")
]