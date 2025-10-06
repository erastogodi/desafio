from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(String, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    ingredient = Column(String(255), nullable=False)
    measure = Column(String(255), nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")
