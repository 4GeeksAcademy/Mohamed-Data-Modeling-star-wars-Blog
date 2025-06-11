from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    # Relationships
    favorites = relationship("Favorite", back_populates="user")
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[float] = mapped_column(nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    homeworld_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)

    # Relationships
    homeworld = relationship("Planet", back_populates="characters")
    favorites = relationship("Favorite", back_populates="character")


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[float] = mapped_column(nullable=True)
    rotation_period: Mapped[int] = mapped_column(nullable=True)
    orbital_period: Mapped[int] = mapped_column(nullable=True)
    population: Mapped[int] = mapped_column(nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relationships
    characters = relationship("Character", back_populates="homeworld")
    favorites = relationship("Favorite", back_populates="planet")


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    # created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(
        String(50), nullable=False)  # e.g., "Starfighter", "Speeder"
    length: Mapped[float] = mapped_column(nullable=True)  # in meters
    crew: Mapped[int] = mapped_column(nullable=True)
    passengers: Mapped[int] = mapped_column(nullable=True)
    max_atmosphering_speed: Mapped[int] = mapped_column(nullable=True)
    cargo_capacity: Mapped[float] = mapped_column(nullable=True)
    pilot_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=True)

    # Relationships
    manufacturer = relationship("Planet", back_populates="vehicles")
    pilot = relationship("Character", back_populates="vehicles")
    favorites = relationship("Favorite", back_populates="vehicle")
