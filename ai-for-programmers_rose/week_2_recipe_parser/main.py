#!/usr/bin/env python3
'''
'''

from openai import OpenAI
from pydantic import BaseModel, Field

from typing import List
from pprint import pprint

import sys, os
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Ingredient(BaseModel):
    """
    An Ingredients model that can be used in the Recipe model with the following properties:
    - amount
    - unit
    - name
    """
    name: str = Field(description="Name of ingredient")
    amount: float = Field(description="Amount in units of ingredient")
    unit: str = Field(description="Unit for amount, e.g., 'g' or 'grams' or 'serving'")

class Recipe(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    title: str = Field(description="Name of the recipe")
    ingredients: List[Ingredient] = Field(description="List of ingredients needed for the recipe")
    # ingredients: List[str] = Field(description="List of ingredients needed for the recipe")
    instructions: List[str] = Field(description="Step-by-step instructions to prepare the recipe")

def get_recipe_from_text(recipe_text: str) -> Recipe:
    """
    Convert recipe text into a structured Recipe object using OpenAI.
    """
    client = OpenAI()

    
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "user", "content": f"Convert this recipe into the specified format:\n\n{recipe_text}"}
        ],
        text_format=Recipe
    )
    # Note: instead of returing/parsing string 'response.choices[0].message.content', using text_format=BaseModel subclass
    # kwarg and returning response.output_parsed
    return response.output_parsed

def main():
    # Example usage
    logging.basicConfig(filename="recipe_parser.log",level=logging.INFO)
    
    # Read recipe text from file
    script_dir = os.path.dirname(os.path.abspath(__file__)) ###
    recipe_path = os.path.join(script_dir, "mac_and_cheese_recipe.txt")
    with open(recipe_path, "r") as file:
        recipe_text = file.read()

    # Get structured recipe
    recipe = get_recipe_from_text(recipe_text)
    
    # Print results
    pprint(recipe.ingredients[0])
    pprint(recipe)
    
def test_parse():
    # Example usage
    logging.basicConfig(filename="recipe_parser.log",level=logging.INFO)
    
    # Read recipe text from file
    script_dir = os.path.dirname(os.path.abspath(__file__)) ###
    recipe_path = os.path.join(script_dir, "mac_and_cheese_recipe.txt")
    with open(recipe_path, "r") as file:
        recipe_text = file.read()

    # Get structured recipe
    recipe = get_recipe_from_text(recipe_text)
    
    assert pprint(recipe.ingredients[0]).strip() == "Ingredient(name='macaroni pasta', amount=16.0, unit='oz')"
    

if __name__ == "__main__":
    sys.exit(main())
    