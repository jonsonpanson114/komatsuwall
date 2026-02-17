import json
import re

ENRICHED_DATA_PATH = "data/enriched_data.json"

def filter_products(description, all_products):
    refined_products = []
    # Normalize description for better matching (optional)
    desc_normalized = description.lower()
    
    for product in all_products:
        # Simple inclusion check.
        if product in description:
            refined_products.append(product)
            continue
            
        # Try a slightly more flexible match (remove hyphens)
        prod_normalized = product.replace("-", "").replace(" ", "")
        if prod_normalized in desc_normalized.replace("-", "").replace(" ", ""):
             refined_products.append(product)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(refined_products))

def main():
    print(f"Loading {ENRICHED_DATA_PATH}...")
    try:
        with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
            cases = json.load(f)
    except FileNotFoundError:
        print("Error: enriched_data.json not found.")
        return

    processed_count = 0
    total_images = 0
    
    for case in cases:
        case_products = case.get("products", [])
        
        for desc_entry in case.get("descriptions", []):
            total_images += 1
            description = desc_entry.get("description", "")
            
            # Calculate refined products
            refined = filter_products(description, case_products)
            
            # Update the entry with new field
            desc_entry["refined_products"] = refined
            
    print(f"Processed {len(cases)} cases and {total_images} images.")
    
    # Backup existing file just in case (optional but good practice)
    # shutil.copy(ENRICHED_DATA_PATH, ENRICHED_DATA_PATH + ".bak")

    print(f"Saving updated data to {ENRICHED_DATA_PATH}...")
    with open(ENRICHED_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
        
    print("Migration complete.")

if __name__ == "__main__":
    main()
