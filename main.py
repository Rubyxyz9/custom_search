# main.py
import argparse
import sys
import config_manager
import query_manager
import searcher

def main():
    # An awesome banner for your tool
    banner = r"""
   ______                      __           __   ______                 __
  / ____/___  ____ ___  ____  / /____  ____/ /  / ____/___  ____  _____/ /_
 / /   / __ \/ __ `__ \/ __ \/ __/ _ \/ __  /  / /   / __ \/ __ \/ ___/ __/
/ /___/ /_/ / / / / / / /_/ / /_/  __/ /_/ /  / /___/ /_/ / / / (__  ) /_
\____/\____/_/ /_/ /_/ .___/\__/\___/\__,_/   \____/\____/_/ /_/____/\__/
                    /_/          | Google Custom Search CLI |
    """
    print(banner)

    parser = argparse.ArgumentParser(
        description="A powerful CLI tool to leverage the Google Custom Search API.",
        epilog="Example: python3 main.py run -n 25 -o my_results.json",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Config Command ---
    parser_config = subparsers.add_parser("config", help="Configure API credentials for one or more profiles.")
    parser_config.set_defaults(func=lambda args: config_manager.configure_profile())

    # --- Query Command ---
    parser_query = subparsers.add_parser("query", help="Manage your list of search queries.")
    query_subparsers = parser_query.add_subparsers(dest="query_action", required=True)

    query_subparsers.add_parser("add", help="Add a new search query.").add_argument("query_string", type=str)
    query_subparsers.add_parser("list", help="List all saved queries.")
    query_subparsers.add_parser("remove", help="Remove a query by its index.").add_argument("index", type=int)

    # --- Run Command ---
    parser_run = subparsers.add_parser("run", help="Run a search with your saved queries.")
    parser_run.add_argument("-p", "--profile", type=str, default="default", help="Credentials profile to use (default: default).")
    parser_run.add_argument("-o", "--output", type=str, default="results.json", help="Output file for results (default: results.json).")
    parser_run.add_argument("-n", "--num", type=int, default=10, choices=range(1, 101), metavar="[1-100]", help="Results per query (default: 10, max: 100).")
    parser_run.add_argument("--full-url", action="store_true", help="Save full URLs instead of just the domain names.")
    parser_run.add_argument("--force", action="store_true", help="Bypass the API daily limit check (use with caution).")

    args = parser.parse_args()
    
    # --- Function Dispatch ---
    if args.command == "config":
        args.func(args)
    elif args.command == "query":
        if args.query_action == "add":
            query_manager.add_query(args.query_string)
        elif args.query_action == "list":
            query_manager.list_queries()
        elif args.query_action == "remove":
            query_manager.remove_query(args.index)
    elif args.command == "run":
        run_search_operation(args)

def run_search_operation(args):
    """Wrapper function to handle the logic for the 'run' command."""
    api_key, search_engine_id = config_manager.load_credentials(args.profile)
    if not api_key: return

    queries = query_manager.load_queries()
    if not queries:
        print("🤷 No queries to run. Use 'python3 main.py query add \"<your_query>\"' to add one.")
        return

    searcher.perform_search(api_key, search_engine_id, queries, args.num, args.output, args.full_url, args.force)

if __name__ == "__main__":
    main()
