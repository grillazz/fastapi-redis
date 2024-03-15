from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PropsValueSchema(BaseModel):
    # TODO: add validation for sval - check if it is correct SMILES
    sval: Optional[str] = None


class PropsUrnSchema(BaseModel):
    label: Optional[str] = None
    name: Optional[str] = None
    datatype: Optional[int] = None
    version: Optional[str] = None
    software: Optional[str] = None
    source: Optional[str] = None
    release: Optional[str] = None


class PropsSchema(BaseModel):
    urn: PropsUrnSchema = Field(...)
    value: PropsValueSchema = Field(...)


class CompoundSchema(BaseModel):
    id: Dict = Field(...)
    atoms: Dict = Field(...)
    bonds: Optional[Dict] = None
    stereo: Optional[List] = None
    coords: List = Field(...)
    charge: int = Field(...)
    props: List[PropsSchema] = Field(...)
    count: Dict = Field(...)


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
                                    "release": "2019.06.18",
                                },
                                "value": {
                                    "sval": "CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4"
                                },
                            },
                            {
                                "urn": {
                                    "label": "SMILES",
                                    "name": "Canonical",
                                    "datatype": 1,
                                    "version": "2.1.5",
                                    "software": "OEChem",
                                    "source": "openeye.com",
                                    "release": "2019.06.18",
                                },
                                "value": {
                                    "sval": "CSC1=NC2=NN=C(C(=O)N2N1)[N+](=O)[O-]"
                                },
                            },
                        ],
                        "count": {},
                    },
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
                                    "release": "2019.06.18",
                                },
                                "value": {
                                    "sval": "CCS(=O)(=O)N1CC(C1)(CC#N)N2C=C(C=N2)C3=C4C=CNC4=NC=N3"
                                },
                            },
                        ],
                        "count": {},
                    },
                ]
            }
        }
