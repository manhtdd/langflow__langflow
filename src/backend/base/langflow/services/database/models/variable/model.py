from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from pydantic import model_validator
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from langflow.services.database.models.variable.constants import IS_READABLE_MAP, VariableCategories

if TYPE_CHECKING:
    from langflow.services.database.models.user.model import User


def utc_now():
    return datetime.now(timezone.utc)


class VariableBase(SQLModel):
    name: Optional[str] = Field(None, description="Name of the variable")
    value: Optional[str] = Field(None, description="Encrypted value of the variable")
    category: VariableCategories = Field(sa_column=Column(Enum(VariableCategories)), description="Type of the variable")


class Variable(VariableBase, table=True):
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique ID for the variable",
    )
    # name is unique per user
    created_at: datetime = Field(default_factory=utc_now, description="Creation time of the variable")
    updated_at: Optional[datetime] = Field(None, description="Last update time of the variable")
    # foreign key to user table
    user_id: UUID = Field(description="User ID associated with this variable", foreign_key="user.id")
    user: "User" = Relationship(back_populates="variables")
    is_readable: Optional[bool] = Field(
        default=True,
        description="Whether the variable is readable by the user. If False, the variable is only readable by the system.",
    )

    @model_validator(mode="before")
    def validate_type_and_is_readable(cls, data):
        # Is readable is never passed and should be set according to the type
        if data.get("category") in IS_READABLE_MAP:
            data["is_readable"] = IS_READABLE_MAP[data.get("category")]
        else:
            raise ValueError(f"Invalid variable type {data.get('category')}")
        return data


class VariableCreate(VariableBase):
    type: Optional[str] = Field(None, description="Type of the variable")


class VariableRead(SQLModel):
    id: UUID
    name: Optional[str] = Field(None, description="Name of the variable")
    category: VariableCategories = Field(sa_column=Column(Enum(VariableCategories)), description="Type of the variable")


class VariableUpdate(SQLModel):
    id: UUID  # Include the ID for updating
    name: Optional[str] = Field(None, description="Name of the variable")
    value: Optional[str] = Field(None, description="Encrypted value of the variable")
    category: VariableCategories = Field(sa_column=Column(Enum(VariableCategories)), description="Type of the variable")
