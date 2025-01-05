from sqlalchemy import (
    Column,
    Integer,
    Sequence,
    Text,
    UniqueConstraint,
    ForeignKey
)
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship


Base = declarative_base()


class Mutation(Base):
    __tablename__ = "mutations"
    __table_args__ = (
        # UniqueConstraint("hugo_symbol", "variant_type", "reference_allele"),
        {"schema": "main"},
    )

    id = Column(
        Integer,
        Sequence("main.mutations_id_seq", quote=False),
        primary_key=True,
    )
    hugo_symbol = Column(Text, nullable=False)
    variant_type = Column(Text, nullable=False)
    reference_allele = Column(Text, nullable=False)
    # allele = Column(Text, nullable=False)
    chromosome = Column(Integer, nullable=True)
    start_position = Column(Integer, nullable=True)
    end_position = Column(Integer, nullable=True)

    reference_id = Column(ForeignKey("main.references.id"), nullable=False)
    reference: Mapped["Reference"] = relationship("Reference", back_populates="mutations", uselist=False)


class Metric(Base):
    __tablename__ = "metrics"
    __table_args__ = (
        UniqueConstraint("name", "version", "value"),
        {"schema": "main"},
    )

    id = Column(
        Integer,
        Sequence("main.metrics_id_seq", quote=False),
        primary_key=True,
    )
    name = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    value = Column(Text, nullable=False)

    sample_id = Column(ForeignKey("main.samples.id"), nullable=False)
    sample: Mapped["Sample"] = relationship("Sample", back_populates="metrics")


class Sample(Base):
    __tablename__ = "samples"
    __table_args__ = (
        UniqueConstraint("name"),
        {"schema": "main"},
    )

    id = Column(
        Integer,
        Sequence("main.samples_id_seq", quote=False),
        primary_key=True,
    )
    name = Column(Text, nullable=False)

    metrics: Mapped[List["Metric"]] = relationship("Metric", back_populates="sample")
    reference: Mapped["Reference"] = relationship("Reference", back_populates="samples")


class Reference(Base):
    __tablename__ = "references"
    __table_args__ = (
        UniqueConstraint("name"),
        {"schema": "main"},
    )

    id = Column(
        Integer,
        Sequence("main.references_id_seq", quote=False),
        primary_key=True,
    )
    name = Column(Text, nullable=False)

    sample_id = Column(ForeignKey("main.samples.id"), nullable=False)

    samples: Mapped[List["Reference"]] = relationship("Sample", back_populates="reference")
    mutations: Mapped[List["Mutation"]] = relationship("Mutation", back_populates="reference")


