import pytest
from dotenv import load_dotenv


def pytest_configure(config):
    load_dotenv(".env.development.test")


@pytest.fixture(scope="session")
def engine():
    return get_engine()


@pytest.fixture(scope="session")
def tables(engine):
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def knowledge_graph():
    manager = KnowledgeGraphManager()
    with manager.transactional_graph() as graph:
        yield graph
        graph.rollback()
    manager.close()
