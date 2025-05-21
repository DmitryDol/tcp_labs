import enum

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import settings
from dto import CardDTO, CardLinkDTO, RoadmapDTO, UserCardDTO, UserDTO, UserRoadmapDTO


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # Set your default UUID to avatar
    avatar: Mapped[str] = mapped_column(
        String,
        nullable=True,
        server_default=text(f"'{settings.DEFAULT_AVATAR}'"),
    )

    owned_roadmaps: Mapped[list["Roadmap"]] = relationship(
        back_populates="owner", passive_deletes=True
    )
    roadmaps: Mapped[list["UserRoadmap"]] = relationship(
        back_populates="user", passive_deletes=True
    )
    cards: Mapped[list["UserCard"]] = relationship(
        back_populates="user", passive_deletes=True
    )

    def to_read_model(self) -> UserDTO:
        return UserDTO.model_validate(self, from_attributes=True)


class Roadmap(Base):
    __tablename__ = "roadmaps"

    class DifficultyEnum(enum.Enum):
        easy = "easy"
        medium = "medium"
        hard = "hard"

    class VisibilityEnum(enum.Enum):
        public = "public"
        link_only = "link only"
        private = "private"

    class EditPermissionEnum(enum.Enum):
        view_only = "view only"
        can_edit = "can edit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    difficulty: Mapped[DifficultyEnum] = mapped_column(
        Enum(DifficultyEnum), nullable=False
    )
    edit_permission: Mapped[EditPermissionEnum] = mapped_column(
        Enum(EditPermissionEnum), nullable=False
    )
    visibility: Mapped[VisibilityEnum] = mapped_column(
        Enum(VisibilityEnum), nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner: Mapped["User"] = relationship(
        back_populates="owned_roadmaps", passive_deletes=True
    )
    cards: Mapped[list["Card"]] = relationship(
        back_populates="roadmap", passive_deletes=True
    )
    users: Mapped[list["UserRoadmap"]] = relationship(
        back_populates="roadmap", passive_deletes=True
    )

    def to_read_model(self) -> RoadmapDTO:
        return RoadmapDTO.model_validate(self, from_attributes=True)


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    roadmap_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False
    )
    order_position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    roadmap: Mapped["Roadmap"] = relationship(
        back_populates="cards", passive_deletes=True
    )
    users: Mapped[list["UserCard"]] = relationship(
        back_populates="card", passive_deletes=True
    )
    links: Mapped[list["CardLink"]] = relationship(
        back_populates="card", passive_deletes=True
    )

    __table_args__ = (
        # order_pos will be unique in the roadmap
        UniqueConstraint("roadmap_id", "order_position", name="uq_roadmap_card_position"),
    )

    def to_read_model(self) -> CardDTO:
        return CardDTO.model_validate(self, from_attributes=True)


class UserRoadmap(Base):
    __tablename__ = "user_roadmaps"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    roadmap_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roadmaps.id", ondelete="CASCADE"),
        primary_key=True,
    )
    background: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default=text(f"'{settings.DEFAULT_BACKGROUND}'"),
    )

    user: Mapped["User"] = relationship(back_populates="roadmaps", passive_deletes=True)
    roadmap: Mapped["Roadmap"] = relationship(
        back_populates="users", passive_deletes=True
    )

    def to_read_model(self) -> UserRoadmapDTO:
        return UserRoadmapDTO.model_validate(self, from_attributes=True)


class UserCard(Base):
    __tablename__ = "user_cards"

    class StatusEnum(enum.Enum):
        in_progress = "in progress"
        done = "done"
        to_do = "to do"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    card_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True
    )
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False, server_default=text("'to_do'")
    )

    user: Mapped["User"] = relationship(back_populates="cards", passive_deletes=True)
    card: Mapped["Card"] = relationship(back_populates="users", passive_deletes=True)

    def to_read_model(self) -> UserCardDTO:
        return UserCardDTO.model_validate(self, from_attributes=True)


class CardLink(Base):
    __tablename__ = "card_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False
    )
    link_title: Mapped[str | None] = mapped_column(String(256))
    link_content: Mapped[str | None] = mapped_column(String)

    card: Mapped["Card"] = relationship(back_populates="links", passive_deletes=True)

    def to_read_model(self) -> CardLinkDTO:
        return CardLinkDTO.model_validate(self, from_attributes=True)
