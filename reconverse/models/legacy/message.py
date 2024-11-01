from sqlalchemy import JSON, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base import Base

message_recipients = Table(
    "message_recipients",
    Base.metadata,
    Column("message_id", Integer, ForeignKey("messages.id")),
    Column("entity_id", Integer, ForeignKey("entities.id")),
)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    content = Column(String, nullable=False)
    meta = Column(JSON)
    # Order in conversation
    sequence_number = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("Entity", foreign_keys=[sender_id])
    recipients = relationship("Entity", secondary=message_recipients)
    memories = relationship("Memory", back_populates="message")
