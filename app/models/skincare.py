from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SkincareProduct(BaseModel):
    id: Optional[str] = Field(None, description="Product unique ID")
    product_name: str = Field(..., description="Full name of skincare product")
    brand: str = Field(..., description="Brand name e.g. CeraVe, Cosrx, La Roche-Posay")
    category: str = Field(..., description="Category e.g. Cleanser, Serum, Moisturizer, Sunscreen, Treatment")
    skin_types: List[str] = Field(..., description="Target skin types e.g. ['Dry', 'Oily', 'Sensitive', 'Combination']")
    targeted_concerns: List[str] = Field(..., description="Targeted skin concerns e.g. ['Acne', 'Dark Spots', 'Redness', 'Dryness']")
    key_ingredients: List[str] = Field(..., description="Active ingredients e.g. ['Salicylic Acid', 'Niacinamide', 'Centella']")
    price: float = Field(..., description="Product price")
    currency: str = Field("USD", description="Currency symbol/code")
    rating: float = Field(4.8, description="User rating (1-5)")
    image_url: str = Field(..., description="Product image URL")
    am_pm_routine: str = Field("Both", description="Routine application time: 'AM', 'PM', or 'Both'")
    description: str = Field(..., description="Product description & benefits")
    how_to_use: str = Field(..., description="Usage instructions")
    match_score: Optional[int] = Field(None, description="AI symptom match score percentage (0-100%)")
    suitability_reason: Optional[str] = Field(None, description="AI explanation of why this product suits user's symptoms")


class SkincareProductCreate(BaseModel):
    product_name: str
    brand: str
    category: str
    skin_types: List[str]
    targeted_concerns: List[str]
    key_ingredients: List[str]
    price: float
    currency: str = "USD"
    rating: float = 4.8
    image_url: str
    am_pm_routine: str = "Both"
    description: str
    how_to_use: str


class SymptomAnalysisRequest(BaseModel):
    symptoms: str = Field(..., description="Description of skin symptoms or concerns (text or voice-transcribed)")
    skin_type: Optional[str] = Field(None, description="User skin type: 'Dry', 'Oily', 'Combination', 'Sensitive', 'Normal'")
    budget_max: Optional[float] = Field(None, description="Max budget limit")
    voice_enabled: Optional[bool] = Field(True, description="Generate voice speech text output for Web Speech TTS")


# --- Feature 2: Ingredient Safety & Conflict Checker Schemas ---
class SafetyCheckRequest(BaseModel):
    product_ids: Optional[List[str]] = Field(default_factory=list, description="Product IDs selected in cart")
    product_names: Optional[List[str]] = Field(default_factory=list, description="Product names or ingredient lists to check")


class ConflictDetail(BaseModel):
    ingredient_a: str
    ingredient_b: str
    severity: str = Field(..., description="'High', 'Medium', or 'Low'")
    risk_description: str
    solution: str


class SafetyCheckResponse(BaseModel):
    is_safe: bool = Field(..., description="Whether combination is safe to use together")
    conflicts: List[ConflictDetail] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    safe_usage_tips: List[str] = Field(default_factory=list)


# --- Feature 3: Side-by-Side Product Comparison Schemas ---
class ProductCompareRequest(BaseModel):
    product_id_a: str = Field(..., description="First product ID or name")
    product_id_b: str = Field(..., description="Second product ID or name")


class ProductCompareResponse(BaseModel):
    product_a: Dict[str, Any]
    product_b: Dict[str, Any]
    comparison_summary: str
    key_differences: List[str]
    winner_for_dry_skin: str
    winner_for_oily_skin: str
    winner_for_sensitive_skin: str
    value_verdict: str


# --- Feature 4: Weekly Routine Scheduler Schemas ---
class RoutineScheduleRequest(BaseModel):
    product_ids: Optional[List[str]] = Field(default_factory=list, description="Selected skincare products")
    skin_type: Optional[str] = Field("Combination", description="User's skin type")


class DaySchedule(BaseModel):
    AM: List[str]
    PM: List[str]


class RoutineScheduleResponse(BaseModel):
    weekly_schedule: Dict[str, DaySchedule] = Field(..., description="Monday through Sunday AM/PM routine grid")
    usage_guidelines: List[str]
    sunscreen_reminder: str


# --- Sales Feature 1: Routine Bundle Builder Schemas ---
class BundleRecommendationRequest(BaseModel):
    product_id: str = Field(..., description="Base product ID added to cart or selected")


class BundleRecommendationResponse(BaseModel):
    base_product: Dict[str, Any]
    bundle_items: List[Dict[str, Any]]
    original_total: float
    discount_percentage: float = 15.0
    discounted_total: float
    savings_amount: float
    bundle_name: str
    why_bundle_works: str


# --- Sales Feature 2: Restock & Replenishment Schemas ---
class RestockCalculationRequest(BaseModel):
    product_id: str = Field(..., description="Skincare product ID")
    volume_ml: float = Field(50.0, description="Product bottle volume in ml")
    usage_frequency_per_day: int = Field(2, description="Applications per day")


class RestockCalculationResponse(BaseModel):
    product_name: str
    estimated_days_lasts: int
    recommended_restock_date: str
    restock_reminder_message: str


# --- Sales Feature 3: Gift Finder Quiz Schemas ---
class GiftFinderRequest(BaseModel):
    recipient_skin_type: Optional[str] = Field("Dry", description="Recipient skin type")
    budget_max: Optional[float] = Field(50.0, description="Max budget")
    occasion: Optional[str] = Field("Birthday", description="Occasion name")


class GiftFinderResponse(BaseModel):
    gift_box_title: str
    included_products: List[Dict[str, Any]]
    total_price: float
    gift_card_message: str


# --- Sales Feature 4: Confidence Stats Schema ---
class ConfidenceStatsResponse(BaseModel):
    product_id: str
    user_satisfaction_rate: str = "94%"
    acne_reduction_rate: str = "92% in 2 weeks"
    moisture_barrier_improvement: str = "96%"
    verified_purchasers_count: int = 1420


# --- Direct Chatbot Order Placement Schemas ---
class OrderItem(BaseModel):
    product_id: Optional[str] = None
    product_name: str
    brand: Optional[str] = None
    quantity: int = 1
    unit_price: float
    total_price: float


class OrderCreateRequest(BaseModel):
    items: List[OrderItem]
    is_inside_dhaka: bool = Field(True, description="True for Inside Dhaka ($2.00 / 60 BDT), False for Outside Dhaka ($4.00 / 120 BDT)")
    customer_name: str
    customer_phone: str
    customer_address: str
    customer_email: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    id: Optional[str] = None
    order_id: str = Field(..., description="Unique Order Number e.g. ORD-2026-A1B2")
    items: List[OrderItem]
    item_subtotal: float
    delivery_fee: float
    location_type: str = Field(..., description="'Inside Dhaka' or 'Outside Dhaka'")
    grand_total: float
    currency: str = "USD"
    customer_name: str
    customer_phone: str
    customer_address: str
    customer_email: Optional[str] = None
    status: str = Field("Pending Admin Confirmation", description="Order status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    message: str
