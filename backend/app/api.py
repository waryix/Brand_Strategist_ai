from fastapi import APIRouter, HTTPException
from .services import analyze_brand, generate_guide, generate_content
from .schemas import (
    BrandAnalysisRequest, 
    BrandAnalysisResponse,
    GuideGenerationRequest,
    GuideGenerationResponse,
    ContentGenerationRequest,
    ContentGenerationResponse
)

router = APIRouter()

@router.post("/analyze-brand", response_model=BrandAnalysisResponse)
async def handle_brand_analysis(request: BrandAnalysisRequest):
    """ Receives brand text, analyzes it, and returns the brand profile. """
    if not request.brand_text or not request.brand_text.strip():
        raise HTTPException(status_code=400, detail="Brand text cannot be empty.")
    try:
        analysis_result = await analyze_brand(request.brand_text)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")

@router.post("/generate-guide", response_model=GuideGenerationResponse)
async def handle_guide_generation(request: GuideGenerationRequest):
    """ Receives brand analysis data and generates a full brand guide. """
    try:
        analysis_dict = request.model_dump() 
        guide_result = await generate_guide(analysis_dict)
        return GuideGenerationResponse(guide_markdown=guide_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during guide generation: {str(e)}")

@router.post("/generate-content", response_model=ContentGenerationResponse)
async def handle_content_generation(request: ContentGenerationRequest):
    """ Receives a brand guide and a prompt to generate on-brand content. """
    if not request.brand_guide or not request.user_request:
        raise HTTPException(status_code=400, detail="Brand guide and user request cannot be empty.")
    try:
        content_result = await generate_content(request.brand_guide, request.user_request)
        return ContentGenerationResponse(generated_content=content_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during content generation: {str(e)}")
