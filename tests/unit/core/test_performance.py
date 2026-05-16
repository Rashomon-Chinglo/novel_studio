from app.core.llm import get_llm
from app.persistence.db.vector import get_vector_store


def test_llm_is_cached():
    llm1 = get_llm()
    llm2 = get_llm()
    assert llm1 is llm2


def test_vector_store_is_cached():
    vs1 = get_vector_store()
    vs2 = get_vector_store()
    assert vs1 is vs2
