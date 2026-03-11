from duckduckgo_search import DDGS

def tool_signal_harvester(company: str) -> dict:
    """
    Captures live buyer signals for a target company.
    Tracks triggers like Funding rounds, Leadership changes, Hiring trends, Website visits & page-level activity, etc.
    """
    query = f"{company} (funding OR hiring OR leadership OR acquisition OR \"new product\" OR growth)"
    try:
        results = DDGS().text(query, max_results=5)
        signals = [res['title'] + " - " + res['body'] for res in results]
        return {
            "company": company,
            "signals": signals
        }
    except Exception as e:
        return {
            "company": company,
            "signals": [f"Error fetching live signals: {str(e)}"]
        }