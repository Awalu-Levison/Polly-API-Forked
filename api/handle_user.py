import requests
import json

def register_user(username, password, base_url="http://localhost:8000"):
    """
    Registers a new user with the Polly-API.

    Args:
        username (str): The username to register.
        password (str): The password for the user.
        base_url (str): The base URL of the API.

    Returns:
        dict: The JSON response from the API, or None if an error occurs.
    """
    register_url = f"{base_url}/register"
    user_data = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(register_url, data=json.dumps(user_data), headers=headers)
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
    new_username = "testuser"
    new_password = "testpassword"

    print(f"Attempting to register user: {new_username}")
    registration_response = register_user(new_username, new_password)

    if registration_response:
        print("User registered successfully!")
        print("Response:")
        print(registration_response)
    else:
        print("User registration failed.")