import json
from pathlib import Path
from typing import Dict, Any, List


# ==========================
# CONFIG
# ==========================
OUTPUT_PATH = Path("facultyfinderpart2\\data\\faculty.json")

REQUIRED_FIELDS = {
    "faculty_id",
    "name",
    "mail",
    "phd_field",
    "specialization",
    "bio",
    "research",
    "publications",
}


# ==========================
# SANITY CHECKS
# ==========================
def validate_api_response(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(api_response, dict):
        raise ValueError("API response must be a dictionary")

    if "results" not in api_response:
        raise ValueError("API response missing 'results' key")

    if not isinstance(api_response["results"], list):
        raise ValueError("'results' must be a list")

    for idx, record in enumerate(api_response["results"]):
        if not isinstance(record, dict):
            raise ValueError(f"Record at index {idx} is not a dictionary")

        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            raise ValueError(
                f"Record at index {idx} missing fields: {missing}"
            )

    return api_response["results"]


# ==========================
# FILE WRITE
# ==========================
def save_to_json(records: List[Dict[str, Any]]):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "results": records
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"[OK] Data saved to {OUTPUT_PATH}")


# ==========================
# PUBLIC API
# ==========================
def generate_json_from_api_response(api_response: Dict[str, Any]):
    records = validate_api_response(api_response)
    save_to_json(records)


# ==========================
# EXAMPLE USAGE
# ==========================
if __name__ == "__main__":
    import requests

    API_URL = "http://127.0.0.1:8000/faculty"
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    generate_json_from_api_response(response.json())
