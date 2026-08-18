import logging
from typing import List, Dict, Any
from app.core.database import get_db

logger = logging.getLogger(__name__)

CURATED_SKINCARE_PRODUCTS: List[Dict[str, Any]] = []


async def seed_skincare_database():
    """Seed MongoDB with curated skincare e-commerce product database."""
    db = get_db()
    if db is None:
        logger.warning("MongoDB database connection not available for seeding.")
        return 0

    try:
        collection = db["skincare_products"]
        count = await collection.count_documents({})
        if count == 0:
            result = await collection.insert_many(CURATED_SKINCARE_PRODUCTS)
            inserted_count = len(result.inserted_ids)
            logger.info(f"✅ Successfully seeded {inserted_count} skincare products into MongoDB!")
            return inserted_count
        else:
            logger.info(f"Skincare database already contains {count} products. Skipping initial seed.")
            return count
    except Exception as e:
        logger.error(f"Error seeding skincare products into MongoDB: {e}")
        return 0
