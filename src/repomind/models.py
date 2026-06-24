import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector 
from repomind.database import Base

def utc_now() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    github_url = Column(String, nullable=False)
    default_branch = Column(String, nullable=True)
    local_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    file_path = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    
    # We generated 384-dimensional vectors with BGE-Small
    embedding = Column(Vector(384), nullable=False) 
    
    generated_at = Column(DateTime(timezone=True), default=utc_now)

class RepositoryHealth(Base):
    __tablename__ = "repository_health"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    architecture_score = Column(Integer, nullable=False)
    testing_score = Column(Integer, nullable=False)
    security_score = Column(Integer, nullable=False)
    documentation_score = Column(Integer, nullable=False)
    scalability_score = Column(Integer, nullable=False)
    maturity_score = Column(Integer, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=utc_now)


class Finding(Base):
    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # e.g., Testing, Security, Technical Debt
    severity = Column(String, nullable=False)  # e.g., High, Medium, Low
    description = Column(Text, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=utc_now)


from sqlalchemy import Boolean

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    impact_score = Column(Float, nullable=False)
    effort_score = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    cost_score = Column(Float, nullable=False)
    priority_score = Column(Float, nullable=False)
    is_recommended = Column(Boolean, default=False)
    generated_at = Column(DateTime(timezone=True), default=utc_now)


class Blueprint(Base):
    __tablename__ = "blueprints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id = Column(UUID(as_uuid=True), ForeignKey("recommendations.id"), nullable=False)
    content = Column(JSONB, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=utc_now)