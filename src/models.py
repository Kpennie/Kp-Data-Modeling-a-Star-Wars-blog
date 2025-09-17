from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

# Association table for many-to-many relationship between User and Character favorites
user_favorite_characters = Table(
    'user_favorite_characters',
    db.Model.metadata,
    mapped_column('user_id', ForeignKey('user.id'), primary_key=True),
    mapped_column('character_id', ForeignKey('character.id'), primary_key=True)
)

# Association table for many-to-many relationship between User and Planet favorites
user_favorite_planets = Table(
    'user_favorite_planets',
    db.Model.metadata,
    mapped_column('user_id', ForeignKey('user.id'), primary_key=True),
    mapped_column('planet_id', ForeignKey('planet.id'), primary_key=True)
)

class User(db.Model):
    """
    Represents blog users who can login and save favorites
    Think of this as a person's profile card!
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    
    # Relationships - like connections between boxes!
    blog_posts: Mapped[list["BlogPost"]] = relationship("BlogPost", back_populates="author", cascade="all, delete-orphan")
    favorite_characters: Mapped[list["Character"]] = relationship("Character", secondary=user_favorite_characters, back_populates="favorited_by")
    favorite_planets: Mapped[list["Planet"]] = relationship("Planet", secondary=user_favorite_planets, back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "favorite_characters_count": len(self.favorite_characters),
            "favorite_planets_count": len(self.favorite_planets),
            "blog_posts_count": len(self.blog_posts)
            # Never serialize password for security!
        }

class Character(db.Model):
    """
    Represents Star Wars characters like Luke Skywalker, Darth Vader
    Think of this as character trading cards!
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    height: Mapped[str] = mapped_column(String(20), nullable=True)  # e.g., "172 cm"
    mass: Mapped[str] = mapped_column(String(20), nullable=True)    # e.g., "77 kg"
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)  # e.g., "19BBY"
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    
    # Foreign key to planet (homeworld)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)
    
    # Relationships
    homeworld: Mapped["Planet"] = relationship("Planet", back_populates="residents")
    favorited_by: Mapped[list["User"]] = relationship("User", secondary=user_favorite_characters, back_populates="favorite_characters")
    blog_posts: Mapped[list["BlogPost"]] = relationship("BlogPost", back_populates="featured_character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "image_url": self.image_url,
            "homeworld": self.homeworld.serialize() if self.homeworld else None,
            "favorited_by_count": len(self.favorited_by),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Planet(db.Model):
    """
    Represents Star Wars planets like Tatooine, Hoth, Coruscant
    Think of this as planet information cards!
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)  # e.g., "arid", "frozen"
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)  # e.g., "desert", "mountains"
    surface_water: Mapped[str] = mapped_column(String(20), nullable=True)  # e.g., "1%"
    population: Mapped[str] = mapped_column(String(50), nullable=True)  # e.g., "200000"
    diameter: Mapped[str] = mapped_column(String(20), nullable=True)   # e.g., "10465 km"
    rotation_period: Mapped[str] = mapped_column(String(20), nullable=True)  # e.g., "23 hours"
    orbital_period: Mapped[str] = mapped_column(String(20), nullable=True)   # e.g., "304 days"
    gravity: Mapped[str] = mapped_column(String(20), nullable=True)    # e.g., "1 standard"
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    
    # Relationships
    residents: Mapped[list["Character"]] = relationship("Character", back_populates="homeworld")
    favorited_by: Mapped[list["User"]] = relationship("User", secondary=user_favorite_planets, back_populates="favorite_planets")
    blog_posts: Mapped[list["BlogPost"]] = relationship("BlogPost", back_populates="featured_planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "image_url": self.image_url,
            "residents_count": len(self.residents),
            "favorited_by_count": len(self.favorited_by),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class BlogPost(db.Model):
    """
    Represents blog posts that users write about Star Wars
    Think of this as story pages in your notebook!
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=True)  # Short description
    is_published: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign keys
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    featured_character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=True)
    featured_planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)
    
    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="blog_posts")
    featured_character: Mapped["Character"] = relationship("Character", back_populates="blog_posts")
    featured_planet: Mapped["Planet"] = relationship("Planet", back_populates="blog_posts")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "is_published": self.is_published,
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "author": {
                "id": self.author.id,
                "username": self.author.username,
                "first_name": self.author.first_name,
                "last_name": self.author.last_name
            } if self.author else None,
            "featured_character": self.featured_character.serialize() if self.featured_character else None,
            "featured_planet": self.featured_planet.serialize() if self.featured_planet else None
        }