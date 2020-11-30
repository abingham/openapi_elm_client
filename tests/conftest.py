from pathlib import Path

import pytest

THIS_DIR = Path(__file__).parent
CORPUS_DIR = THIS_DIR / 'corpus'
FULL_CORPUS = list(CORPUS_DIR.glob("*yaml"))


@pytest.fixture(params=FULL_CORPUS)
def corpus_spec(request):
    yield request.param
