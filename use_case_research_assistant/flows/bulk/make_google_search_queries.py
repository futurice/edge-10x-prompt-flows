from typing import List, Dict
import json
from promptflow import tool

@tool
def make_google_search_queries(reformulated_questions: str, company_name: str, website_filters: List[str]) -> List[str]:
    """
    Takes reformulated questions as JSON string and creates multiple search queries with website filters
    
    Args:
        reformulated_questions: JSON string containing reformulated questions from the LLM
        company_name: Company name to focus the search on
        website_filters: List of website domains to restrict search to
    
    Returns:
        List of search queries with different variations and site filters
    """
    # Parse JSON string to get queries
    try:
        questions_dict = json.loads(reformulated_questions)
        queries = questions_dict.get('queries', [])
    except json.JSONDecodeError:
        print(f"Warning: Could not parse JSON: {reformulated_questions}")
        return []
    
    # Create site-specific queries for each domain and query
    site_queries = []
    for domain in website_filters:
        for base_query in queries:
            # Skip empty or invalid queries
            if not base_query or not isinstance(base_query, str):
                continue
                
            # Clean the query and ensure company name is included
            base_query = base_query.strip()
            if company_name.lower() not in base_query.lower():
                base_query = f"{company_name} {base_query}"
            
            # Basic site-restricted query
            site_queries.append(f'site:{domain} {base_query}')
            
            # Add variations with common search modifiers, always including company name
            site_queries.extend([
                f'site:{domain} {base_query} news',
                f'site:{domain} {base_query} blog',
                f'site:{domain} {base_query} press release',
                f'site:{domain} {base_query} report',
                f'site:{domain} {base_query} whitepaper',
                f'site:{domain} {base_query} case study',
                f'site:{domain} {base_query} webinar',
                f'site:{domain} {base_query} podcast',
                f'site:{domain} {base_query} video',
                f'site:{domain} {base_query} infographic'
            ])
    
    # Add some non-site-restricted queries for broader context
    general_queries = []
    for base_query in queries:
        if not base_query or not isinstance(base_query, str):
            continue
        base_query = base_query.strip()
        if company_name.lower() not in base_query.lower():
            base_query = f"{company_name} {base_query}"
            
        general_queries.extend([
            f'{base_query} announcement',
            f'{base_query} blog',
            f'{base_query} documentation'
        ])
    
    # Combine all queries and remove duplicates while preserving order
    all_queries = []
    seen = set()
    for query in site_queries + general_queries:
        if query not in seen:
            all_queries.append(query)
            seen.add(query)
            
    return all_queries 