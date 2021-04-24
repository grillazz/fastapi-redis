from typing import List, Optional

from pydantic import BaseModel, Field


class PropsValueSchema(BaseModel):
    sval: str = Field(...)


class PropsUrnSchema(BaseModel):
    label: Optional[str] = Field(...)
    name: Optional[str] = Field(...)
    datatype: Optional[int] = Field(...)
    version: Optional[str] = Field(...)
    software: Optional[str] = Field(...)
    source: Optional[str] = Field(...)
    release: Optional[str] = Field(...)


class PropsSchema(BaseModel):
    urn: PropsUrnSchema = Field(...)
    value: PropsValueSchema = Field(...)


class CompoundSchema(BaseModel):
    id: dict = Field(...)
    atoms: dict = Field(...)
    bonds: dict = Field(...)
    stereo: dict = Field(...)
    cords: dict = Field(...)
    charge: int = Field(...)
    props: List[PropsSchema] = Field(...)
    count: dict = Field(...)
