import json
import re

def filter_products(description, all_products):
    refined_products = []
    # Normalize description for better matching (optional, depends on data)
    desc_normalized = description.lower()
    
    for product in all_products:
        # Simple inclusion check. 
        # Could be improved with regex to avoid partial matches if needed, 
        # but Japanese product names are often specific enough.
        # We might need to handle variations like "マイティ-70" vs "マイティ70" if they exist in text.
        # For now, let's try direct matching and see.
        
        # Remove whitespace and hyphens for flexible matching? 
        # Or stick to exact match first. Enriched data has "マイティ-70".
        # Let's try exact match first.
        if product in description:
            refined_products.append(product)
            continue
            
        # Try a slightly more flexible match (remove hyphens)
        prod_normalized = product.replace("-", "").replace(" ", "")
        if prod_normalized in desc_normalized.replace("-", "").replace(" ", ""):
             refined_products.append(product)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(refined_products))

def verify():
    # Load actual data
    with open("data/enriched_data.json", "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    # Test with Case 3483 (index 0 usually, but let's find it)
    target_case = next((c for c in cases if c["case_id"] == "3483"), None)
    if not target_case:
        print("Case 3483 not found")
        return

    case_products = target_case["products"]
    print(f"Case Products ({len(case_products)}): {case_products}")
    
    for i, desc_entry in enumerate(target_case.get("descriptions", [])[:5]): # Check first 5 images
        desc = desc_entry.get("description", "")
        print(f"\n--- Image {i} ---")
        filtered = filter_products(desc, case_products)
        print(f"Filtered ({len(filtered)}): {filtered}")
        # print(f"Description snippet: {desc[:100]}...")

if __name__ == "__main__":
    verify()
