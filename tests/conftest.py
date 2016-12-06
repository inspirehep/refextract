import os

import pytest

@pytest.fixture
def pdf_files():
    path_to_pdfs = os.path.join(os.path.dirname(__file__), 'data')
    pdfs = os.listdir(path_to_pdfs)
    pdfs.sort()
    return [os.path.join(path_to_pdfs, pdf) for pdf in pdfs]
