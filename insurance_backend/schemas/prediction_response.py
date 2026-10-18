
from pydantic import BaseModel, Field
from typing import Dict


class PredictionResponse(BaseModel):

    predicted_category: str = Field(
        ...,
        description="The predicted insurance premium category",
        examples=["High"]
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Model confidence score for the predicted class (0 to 1)",
        examples=[0.84]
    )

    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        examples=[
            {
                "Low": 0.01,
                "Medium": 0.15,
                "High": 0.84
            }
        ]
    )
