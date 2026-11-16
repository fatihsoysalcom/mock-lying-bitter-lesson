import sys

# --- Simulate the Real Supplier API ---
# In a real scenario, this would be an actual HTTP call to an external service.
# We simulate its behavior changing over time.
_REAL_API_VERSION = 1

def real_supplier_api_call():
    """Simulates calling the actual supplier API."""
    if _REAL_API_VERSION == 1:
        # Initial API response structure
        print("  [Real API] Fetching data (Version 1)...")
        return {"product_id": "P123", "status": "available", "price": 100}
    elif _REAL_API_VERSION == 2:
        # API has changed: 'product_id' became 'item_id', 'status' became 'availability'
        print("  [Real API] Fetching data (Version 2 - BREAKING CHANGE)...")
        return {"item_id": "P123", "availability": "in_stock", "cost": 105}
    else:
        raise ValueError("Unknown real API version")

# --- Simulate the Mock Supplier API ---
# This mock is initially accurate but will not be updated when the real API changes.
def mock_supplier_api_call():
    """Simulates calling a mock of the supplier API."""
    print("  [Mock API] Fetching data...")
    # This mock always returns the structure of API Version 1
    return {"product_id": "P123", "status": "available", "price": 100}

# --- Client Code (our application) ---
def get_product_details(api_caller_func):
    """
    Our application's function that interacts with the supplier API
    and expects specific fields.
    """
    print(f"Attempting to get product details using {api_caller_func.__name__}...")
    try:
        response = api_caller_func()
        # This is where our application code relies on the API's contract
        product_id = response["product_id"] # <-- This field is crucial for our app
        status = response["status"]         # <-- This field is crucial for our app
        price = response.get("price", "N/A")
        return f"Product ID: {product_id}, Status: {status}, Price: {price}"
    except KeyError as e:
        return f"ERROR: Missing expected field in API response: {e}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred: {e}"

# --- Test / CI Simulation ---
def run_test(test_name, api_caller_func, expected_substring):
    """Simulates a CI test run."""
    print(f"\n--- Running Test: {test_name} ---")
    result = get_product_details(api_caller_func)
    if expected_substring in result:
        print(f"TEST PASSED: '{result}' contains '{expected_substring}'")
        return True
    else:
        print(f"TEST FAILED: '{result}' does NOT contain '{expected_substring}'")
        return False

# --- Main Demonstration Logic ---
if __name__ == "__main__":
    print("--- Scenario 1: Mock is accurate and matches the Real API (Version 1) ---")
    print("  (Both the real API and the mock provide 'product_id' and 'status')")

    # Test with mock (should pass)
    mock_test_passed_v1 = run_test(
        "Client functionality with MOCK (API V1)",
        mock_supplier_api_call,
        "Product ID: P123, Status: available"
    )

    # Test with real API (should pass)
    real_test_passed_v1 = run_test(
        "Client functionality with REAL API (API V1)",
        real_supplier_api_call,
        "Product ID: P123, Status: available"
    )

    print("\n" + "="*80)
    print("--- Scenario 2: Real API changes (to Version 2), but Mock remains outdated ---")
    print("  (Real API now returns 'item_id' and 'availability', breaking our client code)")
    print("  (Mock still returns 'product_id' and 'status')")

    # Simulate the real API changing its contract
    _REAL_API_VERSION = 2 # <-- This represents a breaking change on the supplier's side

    # Test with mock (!!! THIS TEST WILL STILL PASS, DEMONSTRATING THE 'LIE' !!!)
    mock_test_passed_v2 = run_test(
        "Client functionality with MOCK (API V2 - MOCK IS OUTDATED)",
        mock_supplier_api_call,
        "Product ID: P123, Status: available"
    )
    if mock_test_passed_v2:
        print("\n!!! IMPORTANT: The mock test PASSED, but the mock is now lying! "
              "Our CI would report success, giving a false sense of security. !!!")
        print("!!! This is the 'Acı Bir Ders' (Bitter Lesson) from the article. !!!")

    # Test with real API (!!! THIS TEST WILL NOW FAIL, REVEALING THE REAL PROBLEM !!!)
    real_test_passed_v2 = run_test(
        "Client functionality with REAL API (API V2 - REAL API HAS CHANGED)",
        real_supplier_api_call,
        "Product ID: P123, Status: available" # This substring will no longer be found
    )
    if not real_test_passed_v2:
        print("\n!!! The real API test FAILED, correctly identifying the breaking change. !!!")
        print("!!! This shows why relying solely on outdated mocks is dangerous. !!!")

    print("\n" + "="*80)
    print("--- Summary ---")
    print(f"Scenario 1 (Mock accurate): Mock Test Passed: {mock_test_passed_v1}, Real API Test Passed: {real_test_passed_v1}")
    print(f"Scenario 2 (Mock outdated): Mock Test Passed: {mock_test_passed_v2}, Real API Test Failed: {not real_test_passed_v2}")
    print("The mock test in Scenario 2 passed, even though the real API changed and would break the application.")
    print("This highlights the danger of mocks that 'lie' because they are not kept in sync with the actual API.")
