
import requests
import json

def login_for_token(username, password, base_url="http://localhost:8000"):
    """
    Logs in a user to get a JWT token.

    Args:
        username (str): The username to login with.
        password (str): The password for the user.
        base_url (str): The base URL of the API.

    Returns:
        str: The access token, or None if an error occurs.
    """
    login_url = f"{base_url}/login"
    login_data = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(login_url, data=login_data, headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    
    return None

def cast_vote(poll_id: int, option_id: int, token: str, base_url: str = "http://localhost:8000"):
    """
    Casts a vote on a specific poll option.

    Args:
        poll_id (int): The ID of the poll to vote on.
        option_id (int): The ID of the option to vote for.
        token (str): The JWT access token for authentication.
        base_url (str): The base URL of the API.

    Returns:
        dict: The JSON response from the API, or None if an error occurs.
    """
    vote_url = f"{base_url}/polls/{poll_id}/vote"
    vote_data = {"option_id": option_id}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(vote_url, data=json.dumps(vote_data), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

    return None

def get_poll_results(poll_id: int, base_url: str = "http://localhost:8000"):
    """
    Retrieves the results for a specific poll.

    Args:
        poll_id (int): The ID of the poll to get results for.
        base_url (str): The base URL of the API.

    Returns:
        dict: The poll results from the API, or None if an error occurs.
    """
    results_url = f"{base_url}/polls/{poll_id}/results"

    try:
        response = requests.get(results_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

    return None

if __name__ == '__main__':
    # --- Example Usage ---
    
    # 1. Log in to get a token
    # Replace with a user that you have already registered
    test_username = "testuser"
    test_password = "testpassword"
    print(f"Attempting to log in as user: {test_username}")
    access_token = login_for_token(test_username, test_password)

    if access_token:
        print("Login successful!")
        
        # 2. Cast a vote (assuming poll with ID 1 and option with ID 1 exist)
        poll_to_vote_on = 1
        option_to_choose = 1
        print(f"\nAttempting to vote on poll {poll_to_vote_on} for option {option_to_choose}...")
        vote_response = cast_vote(poll_to_vote_on, option_to_choose, access_token)
        
        if vote_response:
            print("Vote cast successfully!")
            print(vote_response)
        else:
            print("Failed to cast vote.")

    else:
        print("Login failed. Cannot proceed to vote.")

    # 3. Get poll results (this can be done without a token)
    # Assuming a poll with ID 1 exists
    poll_to_get_results = 1
    print(f"\nAttempting to get results for poll {poll_to_get_results}...")
    results = get_poll_results(poll_to_get_results)

    if results:
        print("Successfully fetched poll results!")
        print(f"Question: {results.get('question')}")
        for result in results.get('results', []):
            print(f"- {result.get('text')}: {result.get('vote_count')} votes")
    else:
        print("Failed to get poll results.")
