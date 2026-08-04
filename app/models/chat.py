from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Text content of the message")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's symptoms, problem description, or question")
    image_url: Optional[str] = Field(None, description="Optional image URL of face/skin or product bottle")
    image_base64: Optional[str] = Field(None, description="Optional base64 encoded image string")
    skin_type: Optional[str] = Field(None, description="Optional skin type: 'Dry', 'Oily', 'Combination', 'Sensitive', 'Normal'")
    history: Optional[List[ChatMessage]] = Field(default_factory=list, description="Prior conversation history")
    include_chart: Optional[bool] = Field(True, description="Whether to include skin suitability chart data")
    voice_enabled: Optional[bool] = Field(True, description="Whether to generate voice speech script output")


class ChartDataset(BaseModel):
    label: str = Field(..., description="Dataset label")
    data: List[Union[int, float]] = Field(..., description="Numeric values for each label category")
    backgroundColor: Optional[List[str]] = Field(None, description="List of hex/RGB color strings for each bar/slice")
    borderColor: Optional[List[str]] = Field(None, description="Border colors for bars or lines")


class ChartData(BaseModel):
    type: str = Field(..., description="Chart type: 'bar', 'pie', 'doughnut', or 'line'")
    title: str = Field(..., description="Chart display title")
    labels: List[str] = Field(..., description="Category labels for the X axis or chart slices")
    datasets: List[ChartDataset] = Field(..., description="Array of chart datasets")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Conversational Markdown diagnosis and product recommendations in Bengali & English")
    voice_text: Optional[str] = Field(None, description="Voice-optimized speech script for Web Speech TTS in Bengali")
    voice_audio_url: Optional[str] = Field(None, description="Free Google Translate TTS Audio MP3 URL for direct playback")
    image_analysis_type: Optional[str] = Field(None, description="'Skin Analysis' or 'Product Recognition'")
    detected_features: List[str] = Field(default_factory=list, description="List of detected skin concerns or product features")
    recommended_products: List[Dict[str, Any]] = Field(default_factory=list, description="Matched skincare products catalog items")
    routine_steps: Optional[Dict[str, List[str]]] = Field(default_factory=dict, description="Personalized AM & PM skincare routine steps")
    chart: Optional[ChartData] = Field(None, description="Structured Chart data object for UI rendering")
    summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Symptom & skin analysis summary")
    suggested_questions: Optional[List[str]] = Field(default_factory=list, description="Suggested follow-up queries")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
