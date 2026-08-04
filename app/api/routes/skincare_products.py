import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId

from app.core.database import get_db
from app.models.skincare import (
    SkincareProduct,
    SkincareProductCreate,
    SafetyCheckRequest,
    SafetyCheckResponse,
    ProductCompareRequest,
    ProductCompareResponse,
    RoutineScheduleRequest,
    RoutineScheduleResponse,
    BundleRecommendationRequest,
    BundleRecommendationResponse,
    RestockCalculationRequest,
    RestockCalculationResponse,
    GiftFinderRequest,
    GiftFinderResponse,
    ConfidenceStatsResponse,
)
from app.services.skincare_seed import seed_skincare_database, CURATED_SKINCARE_PRODUCTS

router = APIRouter()
logger = logging.getLogger(__name__)


def serialize_doc(doc: dict) -> dict:
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


@router.get("/", response_model=List[SkincareProduct])
async def list_skincare_products(
    concern: Optional[str] = Query(None, description="Filter by targeted skin concern (e.g. Acne, Dryness, Redness, Dark Spots)"),
    skin_type: Optional[str] = Query(None, description="Filter by skin type (e.g. Dry, Oily, Sensitive, Combination)"),
    category: Optional[str] = Query(None, description="Filter by category (e.g. Cleanser, Serum, Moisturizer, Sunscreen)"),
    brand: Optional[str] = Query(None, description="Filter by brand name"),
    search: Optional[str] = Query(None, description="Search by product name or ingredient"),
):
    """List all skincare products in the e-commerce store with optional concern/skin type filtering."""
    db = get_db()
    query = {}

    if concern:
        query["targeted_concerns"] = {"$regex": concern, "$options": "i"}
    if skin_type:
        query["skin_types"] = {"$regex": skin_type, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}
    if search:
        query["$or"] = [
            {"product_name": {"$regex": search, "$options": "i"}},
            {"key_ingredients": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
        ]

    products = []
    if db is not None:
        try:
            products = await db["skincare_products"].find(query).to_list(length=100)
        except Exception as e:
            logger.error(f"Error querying skincare_products collection: {e}")

    if not products:
        # Fallback to curated in-memory products if database is empty or not connected
        filtered = []
        for p in CURATED_SKINCARE_PRODUCTS:
            if concern and not any(concern.lower() in c.lower() for c in p.get("targeted_concerns", [])):
                continue
            if skin_type and not any(skin_type.lower() in st.lower() for st in p.get("skin_types", [])):
                continue
            if category and category.lower() not in p.get("category", "").lower():
                continue
            if brand and brand.lower() not in p.get("brand", "").lower():
                continue
            filtered.append(p)
        return [SkincareProduct(**p) for p in filtered]

    return [SkincareProduct(**serialize_doc(p)) for p in products]


@router.get("/{product_id}", response_model=SkincareProduct)
async def get_skincare_product(product_id: str):
    """Get single skincare product by ID."""
    db = get_db()
    if db is not None and ObjectId.is_valid(product_id):
        product = await db["skincare_products"].find_one({"_id": ObjectId(product_id)})
        if product:
            return SkincareProduct(**serialize_doc(product))

    # Check curated list fallback
    for p in CURATED_SKINCARE_PRODUCTS:
        if p.get("id") == product_id or p.get("product_name") == product_id:
            return SkincareProduct(**p)

    raise HTTPException(status_code=404, detail="Skincare product not found")


@router.post("/", response_model=SkincareProduct)
async def create_skincare_product(item: SkincareProductCreate):
    """Add a new skincare product to the e-commerce catalog."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")

    doc = item.model_dump()
    result = await db["skincare_products"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return SkincareProduct(**doc)


@router.post("/seed")
async def seed_products():
    """Manually trigger database seeding for skincare products."""
    count = await seed_skincare_database()
    return {"message": f"Successfully seeded {count} skincare products into database.", "count": count}


@router.post("/check-safety", response_model=SafetyCheckResponse)
async def check_products_safety(body: SafetyCheckRequest):
    """
    AI Ingredient Safety & Conflict Checker.
    Evaluates whether selected cart products or active ingredients can be safely used together.
    """
    try:
        from app.services.skincare_ai_service import check_ingredient_safety
        result = await check_ingredient_safety(
            product_ids=body.product_ids,
            product_names=body.product_names,
        )
        return SafetyCheckResponse(**result)
    except Exception as e:
        logger.error(f"Error checking ingredient safety: {e}")
        raise HTTPException(status_code=500, detail=f"Safety check error: {str(e)}")


@router.post("/compare", response_model=ProductCompareResponse)
async def compare_products(body: ProductCompareRequest):
    """
    AI Side-by-Side Product Comparison.
    Compares 2 products side-by-side on active ingredients, price value, and skin type suitability.
    """
    try:
        from app.services.skincare_ai_service import compare_skincare_products
        result = await compare_skincare_products(
            product_id_a=body.product_id_a,
            product_id_b=body.product_id_b,
        )
        return ProductCompareResponse(**result)
    except Exception as e:
        logger.error(f"Error comparing products: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")


@router.post("/routine-schedule", response_model=RoutineScheduleResponse)
async def generate_routine_schedule(body: RoutineScheduleRequest):
    """
    AI Weekly Routine Scheduler.
    Generates a personalized Monday-Sunday AM & PM skincare routine schedule grid.
    """
    try:
        from app.services.skincare_ai_service import generate_weekly_routine_schedule
        result = await generate_weekly_routine_schedule(
            product_ids=body.product_ids,
            skin_type=body.skin_type,
        )
        return RoutineScheduleResponse(**result)
    except Exception as e:
        logger.error(f"Error generating routine schedule: {e}")
        raise HTTPException(status_code=500, detail=f"Routine scheduler error: {str(e)}")


@router.post("/bundle-recommendation", response_model=BundleRecommendationResponse)
async def recommend_routine_bundle(body: BundleRecommendationRequest):
    """
    Sales Feature 1: AI Smart Routine Bundle Builder.
    Suggests a complete 3-step routine bundle with 15% discount when a user selects a base product.
    """
    try:
        from app.services.skincare_ai_service import generate_smart_bundle_recommendation
        result = await generate_smart_bundle_recommendation(product_id=body.product_id)
        return BundleRecommendationResponse(**result)
    except Exception as e:
        logger.error(f"Error generating bundle recommendation: {e}")
        raise HTTPException(status_code=500, detail=f"Bundle error: {str(e)}")


@router.post("/restock-calculator", response_model=RestockCalculationResponse)
async def calculate_restock(body: RestockCalculationRequest):
    """
    Sales Feature 2: AI Product Restock & Replenishment Calculator.
    Calculates product volume depletion and estimates restock date with discount reminder.
    """
    try:
        from app.services.skincare_ai_service import calculate_product_restock_date
        result = await calculate_product_restock_date(
            product_id=body.product_id,
            volume_ml=body.volume_ml,
            usage_frequency_per_day=body.usage_frequency_per_day,
        )
        return RestockCalculationResponse(**result)
    except Exception as e:
        logger.error(f"Error calculating restock: {e}")
        raise HTTPException(status_code=500, detail=f"Restock error: {str(e)}")


@router.post("/gift-finder", response_model=GiftFinderResponse)
async def find_gift_set(body: GiftFinderRequest):
    """
    Sales Feature 3: AI Skincare Gift Finder Quiz.
    Generates a personalized skincare gift box for loved ones based on budget and skin type.
    """
    try:
        from app.services.skincare_ai_service import find_skincare_gift_set
        result = await find_skincare_gift_set(
            recipient_skin_type=body.recipient_skin_type,
            budget_max=body.budget_max,
            occasion=body.occasion,
        )
        return GiftFinderResponse(**result)
    except Exception as e:
        logger.error(f"Error finding gift set: {e}")
        raise HTTPException(status_code=500, detail=f"Gift finder error: {str(e)}")


@router.get("/{product_id}/confidence-stats", response_model=ConfidenceStatsResponse)
async def get_confidence_stats(product_id: str):
    """
    Sales Feature 4: AI Social Proof Confidence Stats.
    Returns verified customer results statistics (e.g. 92% acne reduction rate in 14 days).
    """
    try:
        from app.services.skincare_ai_service import get_product_confidence_stats
        result = await get_product_confidence_stats(product_id=product_id)
        return ConfidenceStatsResponse(**result)
    except Exception as e:
        logger.error(f"Error fetching confidence stats: {e}")
        raise HTTPException(status_code=500, detail=f"Confidence stats error: {str(e)}")
