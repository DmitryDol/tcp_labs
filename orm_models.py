from sqlalchemy import Enum, Text, ForeignKey, Column, Integer, String, DateTime
from database import Base
import enum


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    avatar = Column(String, nullable=False)

class Roadmap(Base):
    __tablename__ = 'roadmaps'

    class DifficultyEnum(enum.Enum):
        easy = "easy"
        medium = "medium"
        hard = "hard"

    roadmap_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)

class Card(Base):
    __tablename__ = 'cards'

    card_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)

class UserRoadmap(Base):
    __tablename__ = 'user_roadmaps'

    class RoleEnum(enum.Enum):
        public = "public"
        link_only = "link only"
        private = "private"

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key = True)
    roadmap_id = Column(Integer, ForeignKey('roadmaps.roadmap_id'), primary_key = True)
    role = Column(Enum(RoleEnum), nullable=False)
    background = Column(String, nullable=False)

class RoadmapCard(Base):
    __tablename__ = 'roadmap_cards'

    roadmap_id = Column(Integer, ForeignKey('roadmaps.roadmap_id'), primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.card_id'), primary_key=True)
    order_position = Column(Integer, nullable=False)

class UserCard(Base):
    __tablename__ = 'user_cards'

    class StatusEnum(enum.Enum):
        in_progress = "in_progress"
        completed = "completed"
        pending = "pending"

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.card_id'), primary_key=True)
    status = Column(Enum(StatusEnum), nullable=False)

class CardLink(Base):
    __tablename__ = 'card_links'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    card_id = Column(Integer, ForeignKey('cards.card_id'), nullable=False) 
    link_title = Column(String)
    link_content = Column(String)
