

def after_tool_callback(context):
    """
    Hook into ADK after any tool runs. If it's 'hotels_search', map hotel names to IDs.
    """
    if context.tool_name == "hotels_search":
        tool_result = context.tool_result
        hotel_map = {
            hotel["name"].lower(): hotel["hotel_id"]
            for hotel in tool_result.get("hotel_offers", [])
        }
        context.state["recent_hotels"] = hotel_map
    return None  # Continue normal flow
