from fastapi import Depends, FastAPI
from rdkit.Chem import MolFromSmiles, RDKFingerprint
from rdkit.DataStructs import FingerprintSimilarity

from app import config
from app.schemas import CompoundsListSchema
from app.service import MoleculesRepository
from app.redis import init_redis_pool

global_settings = config.Settings()


app = FastAPI()


@app.on_event("startup")
async def starup_event():
    app.state.redis = await init_redis_pool()
    app.state.mols_repo = MoleculesRepository(app.state.redis)


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get("/health-check")
async def health_check(settings: config.Settings = Depends(config.get_settings)):
    try:
        await app.state.redis.set(str(settings.redis_url), settings.up)
        value = await app.state.redis.get(str(settings.redis_url))
    except:  # noqa: E722
        value = settings.down
    return {settings.web_server: settings.up, str(settings.redis_url): value}


@app.post("/add-smiles-to-hash")
async def add_smiles(payload: CompoundsListSchema, redis_hash: str):
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

    await app.state.mols_repo.set_multiple(redis_hash, mols)

    hash_len = await app.state.mols_repo.len(redis_hash)
    return {"number_of_inserted_keys": hash_len, "hash_name": redis_hash}


@app.get("/compare-smiles-to-hash")
async def get_smiles_and_compare(compound: str, redis_hash: str):
    """

    :param compound:
    :param redis_hash:
    :return:
    """
    mol = RDKFingerprint(MolFromSmiles(compound))

    mol_hash = await app.state.mols_repo.get_all(redis_hash)

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
