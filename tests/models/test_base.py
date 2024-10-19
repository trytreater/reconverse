from sqlalchemy.sql import text


def test_connection(db_session):
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
