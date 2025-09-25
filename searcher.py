# searcher.py
import requests
import time
import json
from urllib.parse import urlparse
from tqdm import tqdm
import rate_limiter

SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

def perform_search(api_key, search_engine_id, queries, num_results, output_file, save_full_url, force):
    """Executes the search against the Google API."""
    results = set()
    requests_per_query = (num_results + 9) // 10  # 1-10 needs 1 req, 11-20 needs 2, etc.

    print(f"🔍 Starting search for {len(queries)} queries...")
    
    # Pre-flight check for API limits
    if not force:
        required = len(queries) * requests_per_query
        remaining = rate_limiter.get_remaining_requests()
        if remaining < required:
             print(f"⚠️ Warning: Not enough API requests remaining for a full run.")
             print(f"   - Required: ~{required}, Remaining: {remaining}")
             if input("   Continue anyway? (y/n): ").lower() != 'y':
                 print("Aborting search.")
                 return

    for query in queries:
        print(f"\n▶ Running query: '{query}'")
        with tqdm(total=num_results, desc="Results", unit="item", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            for i in range(requests_per_query):
                if not force and not rate_limiter.check_and_update_limit():
                    break  # Stop this query if limit is reached
                
                params = {"q": query, "key": api_key, "cx": search_engine_id, "num": 10, "start": i * 10 + 1}
                
                try:
                    response = requests.get(SEARCH_URL, params=params)
                    response.raise_for_status()
                    rate_limiter.increment_usage()
                    response_data = response.json()

                    if "items" in response_data:
                        for item in response_data["items"]:
                            link = item.get("link")
                            if not link: continue
                            
                            result = link if save_full_url else urlparse(link).netloc
                            if result not in results:
                                results.add(result)
                            pbar.update(1)
                    else:
                        break # No more results for this query
                except requests.exceptions.RequestException as e:
                    print(f"\n❌ Network Error: {e}")
                    break
                    
                time.sleep(1) # Be a good internet citizen
            
        if not force and not rate_limiter.check_and_update_limit():
            print("Stopping all searches due to API limit.")
            break # Stop all queries

    sorted_results = sorted(list(results))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_results, f, indent=2, ensure_ascii=False)

    print(f"\n✨ Done! Found {len(sorted_results)} unique results.")
    print(f"   Results saved to '{output_file}'")
