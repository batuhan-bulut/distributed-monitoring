# httpx_client.py
import httpx
import json
import logging

logger = logging.getLogger(__name__)

async def async_get_request(url: str, params: dict = None, headers: dict = None, timeout: int = 10):
    """
    Makes an asynchronous GET request to the specified URL using httpx.

    Args:
        url (str): The URL to send the GET request to.
        params (dict, optional): A dictionary of query parameters. Defaults to None.
        headers (dict, optional): A dictionary of HTTP headers. Defaults to None.
        timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10.

    Returns:
        dict or None: The JSON response if successful, otherwise None.
                      Prints an error message if the request fails.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            logger.info(f"GET Request to {url} successful!")
            logger.info(f"Status Code: {response.status_code}")

            # Try to parse JSON, if not, return text
            try:
                return response.json()
            except json.JSONDecodeError:
                logger.info("Response is not valid JSON. Returning raw text.")
                return response.text

        except httpx.HTTPStatusError as errh:
            logger.info(f"HTTP Error for GET {url}: {errh} - Response: {errh.response.text}")
        except httpx.RequestError as errc:
            logger.info(f"Request Error (e.g., ConnectionError, Timeout) for GET {url}: {errc}")
        except Exception as err:
            logger.info(f"An unexpected error occurred for GET {url}: {err}")
    return None

async def async_post_request(url: str, data: dict = None, json_data: dict = None, headers: dict = None, timeout: int = 10):
    """
    Makes an asynchronous POST request to the specified URL using httpx.

    Args:
        url (str): The URL to send the POST request to.
        data (dict, optional): A dictionary of form-encoded data. Defaults to None.
        json_data (dict, optional): A dictionary of JSON data. Use either 'data' or 'json_data', not both. Defaults to None.
        headers (dict, optional): A dictionary of HTTP headers. Defaults to None.
        timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10.

    Returns:
        dict or None: The JSON response if successful, otherwise None.
                      Prints an error message if the request fails.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            if json_data:
                response = await client.post(url, json=json_data, headers=headers)
            else:
                response = await client.post(url, data=data, headers=headers)

            response.raise_for_status()  # Raises for 4xx/5xx

            logger.info(f"POST Request to {url} successful!")
            logger.info(f"Status Code: {response.status_code}")

            try:
                return {
                    "status_code": response.status_code,
                    "body": response.json()
                }
            except json.JSONDecodeError:
                logger.info("Response is not valid JSON. Returning raw text.")
                return {
                    "status_code": response.status_code,
                    "body": response.text
                }

        except httpx.HTTPStatusError as errh:
            logger.error(f"HTTP Error for POST {url}: {errh} - Response: {errh.response.text}")
            try:
                return {
                    "status_code": errh.response.status_code,
                    "body": errh.response.json()
                }
            except json.JSONDecodeError:
                return {
                    "status_code": errh.response.status_code,
                    "body": errh.response.text
                }
        except httpx.RequestError as errc:
            logger.error(f"Request Error (e.g., ConnectionError, Timeout) for POST {url}: {errc}")
            return {
                "status_code": 503,
                "body": f"Connection error: {errc}"
            }
        except Exception as err:
            logger.error(f"An unexpected error occurred for POST {url}: {err}")
            return {
                "status_code": 500,
                "body": f"Unexpected error: {err}"
            }
