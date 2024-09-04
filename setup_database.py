import sys 
import os
import importlib
from unittest import mock 

MOCK_POSTGRES_PATH: str = f"postgresql://postgres:admin@localhost:5432/postgres"
MODULE_PATH: str = "src"

sys.path.append(os.path.dirname(MODULE_PATH))
mname = os.path.splitext(os.path.basename(MODULE_PATH))[0]
imported = importlib.import_module(mname)                       
sys.path.pop()

from src.infra.config import *
from src.infra.entities import *

@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_POSTGRES_PATH})
def generate_tables():    
    conn = DBConnectionHandler()
    engine = conn.get_engine()
    Base.metadata.create_all(engine)

generate_tables()