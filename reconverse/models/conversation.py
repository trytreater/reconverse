from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base import Base


conversation_participants = Table(
    "conversation_participants",
    Base.metadata,
    Column("conversation_id", Integer, ForeignKey("conversations.id")),
    Column("entity_id", Integer, ForeignKey("entities.id")),
)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    # Optional conversation title
    title = Column(String)

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    # Relationships
    participants = relationship("Entity", secondary=conversation_participants)
    messages = relationship(
        "Message", back_populates="conversation", order_by="Message.sequence_number"
    )
    memories = relationship("Memory", back_populates="conversation")
