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
    stereo: list = Field(...)
    coords: list = Field(...)
    charge: int = Field(...)
    props: List[PropsSchema] = Field(...)
    count: dict = Field(...)


class CompoundsListSchema(BaseModel):
    PC_Compounds: List[CompoundSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "PC_Compounds": [
                    {
                        "id": {},
                        "atoms": {},
                        "bonds": {},
                        "stereo": [],
                        "coords": [],
                        "charge": 0,
                        "props": [
                            {
                                "urn": {
                                    "label": "SMILES",
                                    "name": "Canonical",
                                    "datatype": 1,
                                    "version": "2.1.5",
                                    "software": "OEChem",
                                    "source": "openeye.com",
                                    "release": "2019.06.18"
                                },
                                "value": {
                                    "sval": "CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4"
                                }
                            },
                        ],
                        "count": {}
                    },
                ]
            }
        }