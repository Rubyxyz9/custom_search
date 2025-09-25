# query_manager.py
import json
import os

QUERIES_FILE = "queries.json"

def load_queries():
    """Loads queries from the JSON file."""
    if not os.path.exists(QUERIES_FILE):
        return []
    try:
        with open(QUERIES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_queries(queries):
    """Saves the list of queries to the JSON file."""
    with open(QUERIES_FILE, "w") as f:
        json.dump(queries, f, indent=4)

def add_query(query_string):
    """Adds a new query to the list, avoiding duplicates."""
    queries = load_queries()
    if query_string in queries:
        print(f"ℹ️  Query '{query_string}' already exists.")
        return
    queries.append(query_string)
    save_queries(queries)
    print(f"✅ Query added: '{query_string}'")

def list_queries():
    """Displays all saved queries with their index numbers."""
    queries = load_queries()
    if not queries:
        print("🤷 No queries found. Add one with the 'query add' command.")
        return
    print("📋 Current Queries:")
    for i, query in enumerate(queries):
        print(f"  [{i}] {query}")

def remove_query(index):
    """Removes a query by its index."""
    queries = load_queries()
    try:
        index = int(index)
        if 0 <= index < len(queries):
            removed_query = queries.pop(index)
            save_queries(queries)
            print(f"✅ Query removed: '{removed_query}'")
        else:
            print(f"❌ Error: Index {index} is out of bounds.")
    except ValueError:
        print("❌ Error: Please provide a valid number for the index.")
