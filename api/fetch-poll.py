
from unittest import skip
import requests

def get_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000"):        
    """
    Fetches a paginated list of polls from the Polly-API.

    Args:
        skip (int): The number of polls to skip for pagination.
        limit (int): The maximum number of polls to return.
        base_url (str): The base URL of the API.

    Returns:
        list: A list of poll objects from the API, or None if an error occurs.
    """
    polls_url = f"{base_url}/polls"
    params = {
        "skip": skip,
        "limit": limit
    }

    try:
        response = requests.get(polls_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

    return None

if __name__ == '__main__':
    # Example usage:
    print("Attempting to fetch polls (skip=0, limit=10)...")
    polls_data = get_polls(skip=0, limit=10)

    if polls_data:
        print("Successfully fetched polls!")
        print("Response:")
        for poll in polls_data:
            print(f"- Poll ID: {poll.get('id')}, Question: {poll.get('question')}")
    else:
        print("Failed to fetch polls.")

