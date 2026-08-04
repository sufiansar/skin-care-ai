import logging
from typing import List, Dict, Any
from app.core.database import get_db

logger = logging.getLogger(__name__)

CURATED_SKINCARE_PRODUCTS: List[Dict[str, Any]] = [
    {
        "product_name": "CeraVe Hydrating Facial Cleanser",
        "brand": "CeraVe",
        "category": "Cleanser",
        "skin_types": ["Dry", "Sensitive", "Normal"],
        "targeted_concerns": ["Dryness", "Redness", "Barrier Repair", "Dehydration"],
        "key_ingredients": ["Ceramides", "Hyaluronic Acid", "Glycerin"],
        "price": 14.99,
        "currency": "USD",
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&q=80",
        "am_pm_routine": "Both",
        "description": "Gentle, non-foaming cleansing lotion that restores skin barrier and retains moisture.",
        "how_to_use": "Apply to wet skin, massage gently for 60 seconds, then rinse with lukewarm water."
    },
    {
        "product_name": "COSRX Low pH Good Morning Gel Cleanser",
        "brand": "COSRX",
        "category": "Cleanser",
        "skin_types": ["Oily", "Combination", "Acne-Prone"],
        "targeted_concerns": ["Acne", "Pores", "Excess Oil", "Blackheads"],
        "key_ingredients": ["Tea Tree Oil", "BHA (Betaine Salicylate)", "Botanical Extracts"],
        "price": 12.00,
        "currency": "USD",
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=500&q=80",
        "am_pm_routine": "Both",
        "description": "Mild, sub-acidic gel cleanser that gently controls sebum and clears clogged pores.",
        "how_to_use": "Lather gel with water, massage gently over face, and rinse thoroughly."
    },
    {
        "product_name": "Anua Heartleaf 77% Soothing Toner",
        "brand": "Anua",
        "category": "Toner",
        "skin_types": ["Sensitive", "Acne-Prone", "Redness-Prone", "Combination"],
        "targeted_concerns": ["Redness", "Acne", "Irritation", "Inflammation"],
        "key_ingredients": ["Heartleaf Extract (Houttuynia Cordata)", "Centella Asiatica", "Chamomilla"],
        "price": 19.50,
        "currency": "USD",
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1608248597261-860824859726?w=500&q=80",
        "am_pm_routine": "Both",
        "description": "Calming, anti-inflammatory Korean toner formulated with 77% Heartleaf extract.",
        "how_to_use": "After cleansing, pat toner gently into face using hands or a cotton pad."
    },
    {
        "product_name": "Paula's Choice 2% BHA Liquid Exfoliant",
        "brand": "Paula's Choice",
        "category": "Treatment",
        "skin_types": ["Oily", "Combination", "Acne-Prone"],
        "targeted_concerns": ["Acne", "Blackheads", "Enlarged Pores", "Textured Skin"],
        "key_ingredients": ["Salicylic Acid (BHA 2%)", "Green Tea Extract", "Methylpropanediol"],
        "price": 35.00,
        "currency": "USD",
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&q=80",
        "am_pm_routine": "PM",
        "description": "Cult-favorite leave-on exfoliant that unclogs pores, smooths wrinkles, and clears breakouts.",
        "how_to_use": "Apply once or twice daily after cleansing & toning using a cotton pad. Do not rinse."
    },
    {
        "product_name": "The Ordinary Niacinamide 10% + Zinc 1%",
        "brand": "The Ordinary",
        "category": "Serum",
        "skin_types": ["Oily", "Combination", "Acne-Prone"],
        "targeted_concerns": ["Hyperpigmentation", "Dark Spots", "Excess Oil", "Enlarged Pores", "Acne Scars"],
        "key_ingredients": ["Niacinamide (Vitamin B3)", "Zinc PCA"],
        "price": 6.50,
        "currency": "USD",
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1617897903246-719242758050?w=500&q=80",
        "am_pm_routine": "Both",
        "description": "High-strength vitamin & mineral formula that targets blemishes and brightens skin tone.",
        "how_to_use": "Apply a few drops to face in morning and evening before heavier creams."
    },
    {
        "product_name": "SkinCeuticals C E Ferulic Vitamin C Serum",
        "brand": "SkinCeuticals",
        "category": "Serum",
        "skin_types": ["Dry", "Normal", "Combination", "Aging"],
        "targeted_concerns": ["Dullness", "Dark Spots", "Wrinkles", "Uneven Tone", "Sun Damage"],
        "key_ingredients": ["15% L-Ascorbic Acid (Vitamin C)", "1% Alpha Tocopherol (Vitamin E)", "0.5% Ferulic Acid"],
        "price": 182.00,
        "currency": "USD",
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=500&q=80",
        "am_pm_routine": "AM",
        "description": "Dermatologist-recommended antioxidant serum that brightens skin and neutralizes free radicals.",
        "how_to_use": "In morning, apply 4-5 drops to clean, dry face and neck before sunscreen."
    },
    {
        "product_name": "COSRX Advanced Snail 96 Mucin Power Essence",
        "brand": "COSRX",
        "category": "Serum",
        "skin_types": ["Dry", "Dehydrated", "Sensitive", "Combination"],
        "targeted_concerns": ["Dryness", "Dehydration", "Dullness", "Acne Scars", "Damaged Barrier"],
        "key_ingredients": ["96.3% Snail Secretion Filtrate", "Sodium Hyaluronate", "Allantoin"],
        "price": 25.00,
        "currency": "USD",
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=500&q=80",
        "am_pm_routine": "Both",
        "description": "Ultra-hydrating essence that plumps skin, fades dark spots, and repairs moisture barrier.",
        "how_to_use": "After cleansing and toning, apply a small amount over entire face and pat gently."
    },
    {
        "product_name": "La Roche-Posay Cicaplast Baume B5+ Soothing Cream",
        "brand": "La Roche-Posay",
        "category": "Moisturizer",
        "skin_types": ["Dry", "Sensitive", "Damaged", "Irritated"],
        "targeted_concerns": ["Redness", "Barrier Repair", "Dryness", "Eczema", "Post-Acne Rawness"],
        "key_ingredients": ["Madecassoside (Centella)", "5% Panthenol (Vitamin B5)", "Shea Butter"],
        "price": 17.99,
        "currency": "USD",
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&q=80",
        "am_pm_routine": "PM",
        "description": "Multi-purpose soothing balm that heals irritated, dry, compromised skin barriers.",
        "how_to_use": "Apply twice daily to clean dry skin as final moisturizer step."
    },
    {
        "product_name": "Beauty of Joseon Relief Sun: Rice + Probiotics SPF50+ PA++++",
        "brand": "Beauty of Joseon",
        "category": "Sunscreen",
        "skin_types": ["Dry", "Combination", "Sensitive", "Normal"],
        "targeted_concerns": ["Sun Protection", "Hyperpigmentation", "Dullness", "Aging"],
        "key_ingredients": ["30% Rice Extract", "Grain Probiotics Complex", "Niacinamide"],
        "price": 18.00,
        "currency": "USD",
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=500&q=80",
        "am_pm_routine": "AM",
        "description": "Lightweight, non-greasy organic sunscreen with no white cast and glowing moisture finish.",
        "how_to_use": "Apply generously 30 minutes before sun exposure as final skincare step."
    },
    {
        "product_name": "La Roche-Posay Effaclar Mat Oil-Free Moisturizer",
        "brand": "La Roche-Posay",
        "category": "Moisturizer",
        "skin_types": ["Oily", "Combination", "Acne-Prone"],
        "targeted_concerns": ["Excess Oil", "Shine Control", "Enlarged Pores", "Acne"],
        "key_ingredients": ["Sebulyse Technology", "Micro-Spheres", "LHA (Lipohydroxy Acid)"],
        "price": 31.99,
        "currency": "USD",
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&q=80",
        "am_pm_routine": "Both",
        "description": "Sebum-regulating matte moisturizer that targets excess oil and tightens visible pores.",
        "how_to_use": "Apply morning and evening all over face after cleansing & serum steps."
    }
]


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
