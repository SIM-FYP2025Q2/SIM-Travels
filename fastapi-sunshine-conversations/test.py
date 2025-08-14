def extract_adk_response_text(data):
    """
    Extracts the conversational response text from either an ADK or A2A data structure.

    This function attempts to parse the input 'data' in two ways:
    1. As a standard ADK response, where the text is directly available.
    2. As an A2A response, where the relevant text is often nested within
       an errorMessage and customMetadata structure.

    Args:
        data (list): A list containing dictionary objects representing the
                     agent's response data.

    Returns:
        str: The extracted response text as a single string, or None if
             no text could be found in either expected format.
    """
    if not isinstance(data, list) or not data:
        return None

    # --- Attempt 1: Extract as a standard ADK response ---
    # This is the most direct and common format. The text is usually in the
    # first element of the list.
    try:
        # Navigate the dictionary: data[0] -> 'content' -> 'parts' -> [0] -> 'text'
        text = data[0].get('content', {}).get('parts', [{}])[0].get('text')
        if text:
            return text.strip()
    except (IndexError, AttributeError):
        # This structure doesn't match the standard ADK format.
        # We'll proceed to the next attempt.
        pass

    # --- Attempt 2: Extract as an A2A error/transfer response ---
    # This format nests the original conversation inside an error message
    # when an agent-to-agent transfer occurs.
    try:
        for item in data:
            # The key indicator is the 'errorMessage' and 'customMetadata' keys.
            if 'errorMessage' in item and 'customMetadata' in item:
                # Navigate the complex nested structure to find the text parts.
                # Path: item -> 'customMetadata' -> 'a2a:request' -> 'params' -> 'message' -> 'parts'
                parts = item.get('customMetadata', {}).get('a2a:request', {}).get('params', {}).get('message', {}).get('parts', [])
                if parts:
                    # Join the 'text' value from each dictionary in the 'parts' list.
                    response_texts = [part.get('text', '') for part in parts]
                    full_text = '\n'.join(response_texts)
                    return full_text.strip()
    except (IndexError, AttributeError):
        # This structure also doesn't match.
        return None

    # Return None if no text could be extracted from any known format.
    return None


# --- Example Usage ---

# 1. Example of an A2A (Agent2Agent) response
a2a_data = [{'content': {'parts': [{'functionCall': {'id': 'adk-b6f0e666-a375-4a59-ab7c-7683004337bb', 'args': {'agent_name': 'flight_offers_agent'}, 'name': 'transfer_to_agent'}}], 'role': 'model'}, 'usageMetadata': {'candidatesTokenCount': 13, 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 13}], 'promptTokenCount': 1956, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 1956}], 'totalTokenCount': 1969}, 'invocationId': 'e-7c105910-f35a-413a-896e-ed6fabf54255', 'author': 'flight_query_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'longRunningToolIds': [], 'id': 'dd132cf8-82d7-4205-92b8-90624f1be862', 'timestamp': 1754507627.766713}, {'content': {'parts': [{'functionResponse': {'id': 'adk-b6f0e666-a375-4a59-ab7c-7683004337bb', 'name': 'transfer_to_agent', 'response': {'result': None}}}], 'role': 'user'}, 'invocationId': 'e-7c105910-f35a-413a-896e-ed6fabf54255', 'author': 'flight_query_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'transferToAgent': 'flight_offers_agent', 'requestedAuthConfigs': {}}, 'id': 'bc80bbc7-4cda-45f9-ab1e-7688c1250838', 'timestamp': 1754507630.568199}, {'errorMessage': 'A2A request failed: HTTP Error 503: Network communication error: All connection attempts failed', 'customMetadata': {'a2a:request': {'id': '94ec4c85-5b85-430a-ba18-94b8dc426dc7', 'jsonrpc': '2.0', 'method': 'message/send', 'params': {'message': {'kind': 'message', 'messageId': '4861c619-f639-4cfd-870a-8ac840ce2391', 'parts': [{'kind': 'text', 'text': 'i want flights from new york to london on 10 august 2025 for 1 pax'}, {'kind': 'text', 'text': '[flight_query_agent] said: Okay, I have all the required information! Just to confirm, you want to fly from New York to London on August 10, 2025, for one adult traveler.\n\nDo you have any additional preferences, such as:\n\n* Return date (for a round-trip flight)\n* Number of child travelers\n* Number of infant travelers\n* Preferred travel class (e.g., Economy, Business)\n* If they prefer non-stop flights\n'}, {'kind': 'text', 'text': 'For context:'}, {'kind': 'text', 'text': 'yes'}, {'kind': 'text', 'text': '[flight_query_agent] said: Okay great! What are the additional preferences you have for your flight? For example, do you have a return date, or preferred travel class?\n'}, {'kind': 'text', 'text': 'For context:'}, {'kind': 'text', 'text': 'my bad i meant i have no preferences, continue search'}, {'kind': 'text', 'text': "[flight_query_agent] called tool `transfer_to_agent` with parameters: {'agent_name': 'flight_offers_agent'}"}, {'kind': 'text', 'text': 'For context:'}, {'kind': 'text', 'text': "[flight_query_agent] `transfer_to_agent` tool returned result: {'result': None}"}, {'kind': 'text', 'text': 'For context:'}], 'role': 'user'}}}, 'a2a:error': 'A2A request failed: HTTP Error 503: Network communication error: All connection attempts failed'}, 'invocationId': 'e-7c105910-f35a-413a-896e-ed6fabf54255', 'author': 'flight_offers_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'id': 'b363daab-48dd-4c54-9265-863bab501866', 'timestamp': 1754507632.869317}]

# 2. Example of an ADK (Agent Development Kit) response
adk_data = [{'content': {'parts': [{'text': 'Okay, I have all the required information! Just to confirm, you want to fly from New York to London on August 10, 2025, for one adult traveler.\n\nDo you have any additional preferences, such as:\n\n* Return date (for a round-trip flight)\n* Number of child travelers\n* Number of infant travelers\n* Preferred travel class (e.g., Economy, Business)\n* If they prefer non-stop flights\n'}], 'role': 'model'}, 'usageMetadata': {'candidatesTokenCount': 103, 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 103}], 'promptTokenCount': 1811, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 1811}], 'totalTokenCount': 1914}, 'invocationId': 'e-e81fb449-4585-469c-944c-c24afb0e5cf5', 'author': 'flight_query_agent', 'actions': {'stateDelta': {}, 'artifactDelta': {}, 'requestedAuthConfigs': {}}, 'id': 'b3a3808f-16b9-4b58-9355-c1db6294fc6f', 'timestamp': 1754507570.438984}]


# Extract and print the text from both examples
a2a_response_text = extract_adk_response_text(a2a_data)
adk_response_text = extract_adk_response_text(adk_data)

print("--- A2A Extracted Text ---")
print(a2a_response_text)
print("\n" + "="*30 + "\n")
print("--- ADK Extracted Text ---")
print(adk_response_text)

