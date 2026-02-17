from search import search, get_similar_by_id

def verify():
    print("Verifying search...")
    results = search("office")
    if not results:
        print("FAIL: No search results found for 'office'")
        return
    
    first_case = results[0]
    case_id = first_case.get("case_id")
    print(f"First result case_id: {case_id}")
    
    if not case_id:
        print("FAIL: No case_id in first search result")
        return

    print(f"Verifying similar search for {case_id}...")
    similar = get_similar_by_id(case_id)
    
    print(f"Found {len(similar)} similar cases.")
    if len(similar) > 0:
        print("SUCCESS: Similar search returned results.")
        for s in similar:
             print(f" - {s.get('project_name')} ({s.get('case_id')})")
    else:
        print("WARNING: Similar search returned 0 results (this might be expected if dataset is small, but check logic).")
        # In a small dataset, it might return 0 if filter removes the query itself and no others are close enough?
        # But get_similar_by_id usually returns neighbors.

if __name__ == "__main__":
    verify()
