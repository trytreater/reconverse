import json
from reconverse.models.legacy.entity import Entity


def test_create_entity(db_session):
    entity = Entity(
        name="Test User",
        type="user",
        meta=json.dumps({"email": "test@example.com"}),
    )

    db_session.add(entity)
    db_session.commit()

    saved_entity = db_session.query(Entity).first()
    assert saved_entity.name == "Test User"
    assert saved_entity.type == "user"
    assert json.loads(saved_entity.meta)["email"] == "test@example.com"
