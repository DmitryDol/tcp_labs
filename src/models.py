from sqlalchemy import String, Text, ForeignKey, Enum, Integer, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import Optional, List
import enum


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    avatar: Mapped[str] = mapped_column(String, nullable=False)
    
    owned_roadmaps: Mapped[List["Roadmap"]] = relationship(back_populates="owner")
    roadmaps: Mapped[List["UserRoadmap"]] = relationship(back_populates="user")
    cards: Mapped[List["UserCard"]] = relationship(back_populates="user")


class Roadmap(Base):
    __tablename__ = 'roadmaps'
    
    class DifficultyEnum(enum.Enum):
        easy = "easy"
        medium = "medium"
        hard = "hard"

    class VisibilityEnum(enum.Enum):
        public = "public"
        link_only = "link only"
        private = "private"

    class EditPermissionEnum(enum.Enum):
        view_only = "view_only"
        can_edit = "can_edit"
    
    roadmap_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    difficulty: Mapped[DifficultyEnum] = mapped_column(Enum(DifficultyEnum), nullable=False)
    
    edit_permission: Mapped[EditPermissionEnum] = mapped_column(Enum(EditPermissionEnum), nullable=False)
    visibility: Mapped[VisibilityEnum] = mapped_column(Enum(VisibilityEnum), nullable=False)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship(back_populates="owned_roadmaps")
    cards: Mapped[List["Card"]] = relationship(back_populates="roadmap")
    users: Mapped[List["UserRoadmap"]] = relationship(back_populates="roadmap")

class Card(Base):
    __tablename__ = 'cards'
    
    card_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    roadmap_id: Mapped[int] = mapped_column(Integer, ForeignKey('roadmaps.roadmap_id', ondelete="CASCADE"), nullable=False)
    order_position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    roadmap: Mapped["Roadmap"] = relationship(back_populates="cards")
    users: Mapped[List["UserCard"]] = relationship(back_populates="card")
    links: Mapped[List["CardLink"]] = relationship(back_populates="card")
    
    __table_args__ = (
        #order_pos will be unique in the roadmap
        UniqueConstraint('roadmap_id', 'order_position', name='uq_roadmap_card_position'),
    )


class UserRoadmap(Base):
    __tablename__ = 'user_roadmaps'
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)
    roadmap_id: Mapped[int] = mapped_column(Integer, ForeignKey('roadmaps.roadmap_id', ondelete="CASCADE"), primary_key=True)
    background: Mapped[str] = mapped_column(String, nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="roadmaps")
    roadmap: Mapped["Roadmap"] = relationship(back_populates="users")


class UserCard(Base):
    __tablename__ = 'user_cards'
    
    class StatusEnum(enum.Enum):
        in_progress = "in_progress"
        completed = "completed"
        pending = "pending"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey('cards.card_id', ondelete="CASCADE"), primary_key=True)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="cards")
    card: Mapped["Card"] = relationship(back_populates="users")


class CardLink(Base):
    __tablename__ = 'card_links'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey('cards.card_id', ondelete="CASCADE"), nullable=False)
    link_title: Mapped[Optional[str]] = mapped_column(String)
    link_content: Mapped[Optional[str]] = mapped_column(String)
    
    card: Mapped["Card"] = relationship(back_populates="links")
