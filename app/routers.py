from typing import AnyStr

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from starlette.responses import JSONResponse, Response
from wurlitzer import pipes
from fastapi import APIRouter, status
from rdkit.Chem import MolFromSmiles, RDKFingerprint
from rdkit.DataStructs import CreateFromBitString, FingerprintSimilarity

from app import main, schemas

smiles_router = APIRouter(prefix="/smiles")


@smiles_router.post("/add-to-hash", status_code=status.HTTP_201_CREATED)
async def add(payload: schemas.CompoundsListSchema, redis_hash: str):
    """

    :param payload:
    :param redis_hash:
    :return:
    """
    mols = {
        x.value.sval: RDKFingerprint(MolFromSmiles(x.value.sval)).ToBitString()
        for compound in payload.PC_Compounds
        for x in compound.props
        if x.urn.label == "SMILES"
    }

    await main.app.state.mols_repo.set_multiple(redis_hash, mols)

    hash_len = await main.app.state.mols_repo.len(redis_hash)
    return {"number_of_inserted_keys": hash_len, "hash_name": redis_hash}


@smiles_router.get("/compare-to-hash")
async def get_and_compare(compound: str, redis_hash: str):
    """

    :param compound:
    :param redis_hash:
    :return:
    """
    mol = RDKFingerprint(MolFromSmiles(compound))

    mol_hash = await main.app.state.mols_repo.get_all(redis_hash)

    similarity = {smile: FingerprintSimilarity(CreateFromBitString(fp), mol) for smile, fp in mol_hash.items()}

    return {
        "number_of_smiles_to_compare": len(similarity),
        "similarity": dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True)),
    }


@smiles_router.get("/draw-smiles")
async def draw(smiles: AnyStr, size: int):
    """
    Convert SMILE code to 2D molecule image in SVG format
    :param smiles:
    :param size:
    :return:
    """

    try:
        # Capture C-level stdout/stderr pipes
        # TODO: make is a part of pydantic validation
        with pipes() as (out, err):
            # convert from smiles to molecule class
            molecule = Chem.MolFromSmiles(smiles)
        stderr: str = err.read()
        if molecule:
            molecule = rdMolDraw2D.PrepareMolForDrawing(molecule)
            # start drawing molecule image
            drawer = rdMolDraw2D.MolDraw2DSVG(size, size)
            drawer.drawOptions().addStereoAnnotation = True
            drawer.drawOptions().addAtomIndices = True
            drawer.DrawMolecule(molecule)
            drawer.FinishDrawing()
            # response as proper svg+xml
            svg = drawer.GetDrawingText()
            return Response(content=svg, media_type="image/svg+xml")
        else:
            data = {"API Error": stderr.splitlines()[1]}
            return JSONResponse(content=data, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as ex:
        print(ex)
