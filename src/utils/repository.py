from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_primary_key_columns(self) -> list:
        """Get primary key columns for the model"""
        if hasattr(self.model, "__table__") and hasattr(
            self.model.__table__, "primary_key"
        ):
            return [
                getattr(self.model, c.name)
                for c in self.model.__table__.primary_key.columns
            ]
        return [self.model.id]

    async def add_one(self, data: dict[str, Any]) -> dict[str, Any] | int:
        """
        Add a single record and return its primary key(s)

        Args:
            data: Dictionary with data to insert

        Returns:
            For single primary key: the scalar value
            For composite keys: dictionary of primary key fields and values
        """
        pk_columns = self._get_primary_key_columns()

        stmt = insert(self.model).values(**data).returning(*pk_columns)
        res = await self.session.execute(stmt)

        if len(pk_columns) == 1:
            return res.scalar_one()
        else:
            return res.mappings().one()

    async def edit_one(
        self, id_or_filter: int | dict[str, Any], data: dict[str, Any]
    ) -> dict[str, Any] | int | None:
        """
        Update a record using either a single ID or composite key filters

        Args:
            id_or_filter: Either an integer ID or a dictionary with filter conditions
            data: Dictionary with data to update

        Returns:
            For single primary key: the scalar value
            For composite keys: dictionary of primary key fields and values
            None: if no record found
        """
        pk_columns = self._get_primary_key_columns()

        if isinstance(id_or_filter, dict):
            stmt = (
                update(self.model)
                .values(**data)
                .filter_by(**id_or_filter)
                .returning(*pk_columns)
            )
        else:
            stmt = (
                update(self.model)
                .values(**data)
                .filter_by(id=id_or_filter)
                .returning(*pk_columns)
            )

        res = await self.session.execute(stmt)

        if len(pk_columns) == 1:
            return res.scalar_one_or_none()
        else:
            result = res.mappings().one_or_none()
            return result

    async def find_all(self, filter_by: dict[str, Any] | None = None) -> list[Any]:
        """
        Find all records with optional filtering

        Args:
            filter_by: Optional dictionary with filter conditions

        Returns:
            List of model instances
        """
        stmt = select(self.model)

        if filter_by:
            stmt = stmt.filter_by(**filter_by)

        res = await self.session.execute(stmt)

        results = res.scalars().all()
        if results and hasattr(results[0], "to_read_model"):
            return [item.to_read_model() for item in results]
        return results

    async def find_one(self, **filter_by) -> Any | None:
        """
        Find a single record by filter criteria

        Args:
            **filter_by: Filter conditions as keyword arguments

        Returns:
            Single model instance or None if not found
        """
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        result = res.scalar_one_or_none()

        if result and hasattr(result, "to_read_model"):
            return result.to_read_model()
        return result

    async def delete_one(
        self, id_or_filter: int | dict[str, Any]
    ) -> dict[str, Any] | int | None:
        """
        Delete a record using either a single ID or composite key filters

        Args:
            id_or_filter: Either an integer ID or a dictionary with filter conditions

        Returns:
            For single primary key: the scalar value
            For composite keys: dictionary of primary key fields and values
            None: if no record found
        """
        pk_columns = self._get_primary_key_columns()

        if isinstance(id_or_filter, dict):
            stmt = delete(self.model).filter_by(**id_or_filter).returning(*pk_columns)
        else:
            stmt = delete(self.model).filter_by(id=id_or_filter).returning(*pk_columns)

        res = await self.session.execute(stmt)

        if len(pk_columns) == 1:
            return res.scalar_one_or_none()
        else:
            result = res.mappings().one_or_none()
            return result
