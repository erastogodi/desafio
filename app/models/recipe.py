from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Recipe(Base):
    """
    Tabela principal de receitas.
    """
    __tablename__ = "recipes"

    # TheMealDB usa idMeal (string numérica); mantemos como string
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False, index=True)  # ex: "themealdb"
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(2083), nullable=False)
    published_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)  # ex: "Chicken"
    area: Mapped[str | None] = mapped_column(String(64), nullable=True)      # ex: "Indian"
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)

    # textos
    description: Mapped[str | None] = mapped_column(Text, nullable=True)  # resumo/primeiras linhas
    content: Mapped[str | None] = mapped_column(Text, nullable=True)      # instruções completas

    imported_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # relacionamento 1:N com ingredientes
    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class RecipeIngredient(Base):
    """
    Ingredientes de cada receita (1:N).
    """
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipe_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    ingredient: Mapped[str] = mapped_column(String(128), nullable=False)
    measure: Mapped[str | None] = mapped_column(String(128), nullable=True)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
