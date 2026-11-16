# mock-lying-bitter-lesson
This example demonstrates the danger of outdated API mocks. It simulates a client interacting with a supplier API, where a mock initially matches the real API. When the real API changes its contract, the outdated mock continues to pass tests, giving a false sense of security in CI, while the actual integration would fail.
