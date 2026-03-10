from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base   # import Base from db.py

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=True)
    file = Column(String, nullable=False)  # file path
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    chunks = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    embedding = Column(LargeBinary, nullable=False)
    page_number = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)

    document = relationship("Document", back_populates="chunks")
