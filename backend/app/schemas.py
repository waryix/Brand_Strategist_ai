from pydantic import BaseModel, Field
from typing import List, Optional

class BrandAnalysisRequest(BaseModel):
    """ The request model for the brand analysis endpoint. """
    brand_text: str

class BrandAnalysisResponse(BaseModel):
    """ The response model containing the brand analysis. """
    BrandArchetype: Optional[str] = Field("N/A", alias="BrandArchetype")
    ToneAndVoice: List[str] = Field(default_factory=list, alias="ToneAndVoice")
    CoreValues: List[str] = Field(default_factory=list, alias="CoreValues")
    TargetAudience: Optional[str] = Field("N/A", alias="TargetAudience")
    Keywords: List[str] = Field(default_factory=list, alias="Keywords")
    
    class Config:
        populate_by_name = True

class GuideGenerationRequest(BrandAnalysisResponse):
    """ The request model for the guide generation endpoint. """
    pass

class GuideGenerationResponse(BaseModel):
    """ The response model containing the generated guide. """
    guide_markdown: str

class ContentGenerationRequest(BaseModel):
    """ The request model for the content generation endpoint. """
    brand_guide: str
    user_request: str

class ContentGenerationResponse(BaseModel):
    """ The response model containing the generated content. """
    generated_content: str
