from fastapi import APIRouter, status
from rdkit.Chem import MolFromSmiles, RDKFingerprint
from rdkit.DataStructs import FingerprintSimilarity

from app import main, schemas

smiles_router = APIRouter()


@smiles_router.post("/add-to-hash", status_code=status.HTTP_201_CREATED)
async def add(payload: schemas.CompoundsListSchema, redis_hash: str):
    """

    :param payload:
    :param redis_hash:
    :return:
    """
    mols = {
        x.value.sval: "SMILES"
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

    similarity = {
        smile: FingerprintSimilarity(RDKFingerprint(MolFromSmiles(smile)), mol)
        for smile in mol_hash.keys()
    }

    return {
        "number_of_smiles_to_compare": len(similarity),
        "similarity": dict(
            sorted(similarity.items(), key=lambda item: item[1], reverse=True)
        ),
    }
