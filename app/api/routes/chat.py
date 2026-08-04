import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.models.chat import ChatRequest, ChatResponse
from app.models.skincare import SymptomAnalysisRequest
from app.services.skincare_ai_service import (
    process_skincare_symptom_analysis,
    process_skincare_vision_analysis,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat_skincare_advisor(body: ChatRequest):
    """
    Skincare Multimodal Voice, Text & Vision AI Symptom Advisor Chat endpoint.

    - **message**: User skin symptoms, questions, or voice transcript.
    - **image_url**: Optional image URL of skin/face or skincare product bottle.
    - **image_base64**: Optional base64 encoded image string.
    - **skin_type**: Optional skin type filter ('Dry', 'Oily', 'Combination', 'Sensitive', 'Normal').
    - **history**: Conversation history.
    - **include_chart**: Set true to generate visual suitability chart JSON.
    - **voice_enabled**: Set true to generate Web Speech API TTS voice script output in Bengali.
    """
    try:
        # Check if an image was submitted for Vision AI analysis
        if body.image_url or body.image_base64:
            result = await process_skincare_vision_analysis(
                image_url=body.image_url,
                image_base64=body.image_base64,
                user_message=body.message,
                skin_type=body.skin_type,
            )
            return ChatResponse(**result)

        history_list = [h.model_dump() for h in body.history] if body.history else []
        result = await process_skincare_symptom_analysis(
            user_message=body.message,
            skin_type=body.skin_type,
            history=history_list,
            include_chart=body.include_chart if body.include_chart is not None else True,
            voice_enabled=body.voice_enabled if body.voice_enabled is not None else True,
        )
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error processing Skincare AI Advisor chat: {e}")
        raise HTTPException(status_code=500, detail=f"Skincare AI error: {str(e)}")


@router.post("/analyze-image", response_model=ChatResponse)
async def analyze_skincare_image(body: ChatRequest):
    """
    Dedicated Multimodal Vision AI endpoint for Skin Photo Analysis or Product Recognition in Bengali.
    """
    try:
        if not body.image_url and not body.image_base64:
            raise HTTPException(status_code=400, detail="Please provide either 'image_url' or 'image_base64'")

        result = await process_skincare_vision_analysis(
            image_url=body.image_url,
            image_base64=body.image_base64,
            user_message=body.message,
            skin_type=body.skin_type,
        )
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=f"Vision AI error: {str(e)}")


@router.post("/analyze-symptoms", response_model=ChatResponse)
async def analyze_skin_symptoms(body: SymptomAnalysisRequest):
    """Dedicated endpoint for Skin Symptom Analysis & E-Commerce Product Recommendations."""
    try:
        result = await process_skincare_symptom_analysis(
            user_message=body.symptoms,
            skin_type=body.skin_type,
            voice_enabled=body.voice_enabled if body.voice_enabled is not None else True,
        )
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error analyzing skin symptoms: {e}")
        raise HTTPException(status_code=500, detail=f"Symptom analysis error: {str(e)}")


@router.get("/charts/concerns")
async def get_concerns_chart():
    """Get skin concern suitability distribution chart for dashboard."""
    return {
        "type": "pie",
        "title": "Most Common Skin Concerns Analyzed",
        "labels": ["Acne & Pores", "Dryness & Dehydration", "Dark Spots & Pigmentation", "Redness & Sensitivity", "Aging & Fine Lines"],
        "datasets": [
            {
                "label": "Analysis Request %",
                "data": [35, 25, 20, 12, 8],
                "backgroundColor": ["#10B981", "#8B5CF6", "#F59E0B", "#EC4899", "#3B82F6"],
            }
        ],
    }
