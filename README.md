# Mock Lying Bitter Lesson

This example demonstrates the danger of outdated API mocks. It simulates a client interacting with a supplier API, where a mock initially matches the real API. When the real API changes its contract, the outdated mock continues to pass tests, giving a false sense of security in CI, while the actual integration would fail.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [Tedarikçi API'sını Mock'larken CI'ı Kurtarmak ve Mock'un Bize Yalan Söylemesi: Acı Bir Ders](https://fatihsoysal.com/blog/tedarikci-apisini-mocklarken-cii-kurtarmak-ve-mockun-bize-yalan-soylemesi-aci-bir-ders/).

## License

MIT — see [LICENSE](LICENSE).
