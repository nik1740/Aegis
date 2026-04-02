"""
Generate Test Data — Creates synthetic expense records for development.

Usage:
    poetry run python scripts/generate_test_data.py

Generates realistic expense records with varying amounts, categories,
and statuses for testing the full pipeline.
"""

import json
import random
import uuid
from datetime import date, timedelta

# Sample merchants per category
MERCHANTS = {
    "meals": ["Pret A Manger", "Wagamama", "Dishoom", "Nando's", "Byron Burger", "Itsu"],
    "transport": ["Uber", "Bolt", "Addison Lee", "National Rail", "TfL", "Hertz"],
    "accommodation": ["Premier Inn", "Travelodge", "Holiday Inn", "Hilton", "Marriott"],
    "office_supplies": ["Staples", "Amazon Business", "Ryman", "WHSmith"],
    "client_entertainment": ["The Ivy", "Sketch", "Nobu", "Hakkasan", "Chiltern Firehouse"],
}

EMPLOYEES = [
    {"id": "E-1042", "name": "Alice Johnson", "location": "London", "role": "Senior Analyst"},
    {"id": "E-1043", "name": "Bob Smith", "location": "London", "role": "Junior Analyst"},
    {"id": "E-1044", "name": "Carol Davis", "location": "New York", "role": "Manager"},
    {"id": "E-1045", "name": "David Wilson", "location": "Berlin", "role": "Junior Analyst"},
    {"id": "E-1046", "name": "Eva Martinez", "location": "Singapore", "role": "Director"},
]

STATUSES = ["SUBMITTED", "PROCESSING", "APPROVED", "REJECTED", "NEEDS_REMEDIATION"]

JUSTIFICATIONS = [
    "Team lunch after sprint review",
    "Client meeting with prospective account",
    "Travel to office for workshop",
    "Quarterly team dinner",
    "Office supplies for home office setup",
    "Airport transfer for client visit",
    "Hotel for 2-day conference attendance",
    "Working lunch during deadline",
    "Entertaining visiting partners",
    "Train tickets for branch office visit",
]


def generate_expenses(n: int = 50) -> list[dict]:
    """Generate n synthetic expense records."""
    expenses = []

    for i in range(n):
        category = random.choice(list(MERCHANTS.keys()))
        merchant = random.choice(MERCHANTS[category])
        employee = random.choice(EMPLOYEES)

        # Generate realistic amounts per category
        amount_ranges = {
            "meals": (8.0, 90.0),
            "transport": (5.0, 150.0),
            "accommodation": (60.0, 300.0),
            "office_supplies": (5.0, 100.0),
            "client_entertainment": (50.0, 250.0),
        }
        min_amt, max_amt = amount_ranges[category]
        amount = round(random.uniform(min_amt, max_amt), 2)

        expense = {
            "expense_id": f"EXP-2026-{str(i + 1).zfill(5)}",
            "idempotency_key": str(uuid.uuid4()),
            "employee_id": employee["id"],
            "employee_name": employee["name"],
            "merchant_name": merchant,
            "category": category,
            "total_amount": amount,
            "currency": "GBP",
            "transaction_date": (date.today() - timedelta(days=random.randint(0, 30))).isoformat(),
            "justification": random.choice(JUSTIFICATIONS),
            "status": random.choice(STATUSES),
            "location": employee["location"],
        }
        expenses.append(expense)

    return expenses


def main() -> None:
    """Generate test data and save to JSON."""
    print("🔧 Generating synthetic expense data...")
    expenses = generate_expenses(50)

    output_path = "scripts/test_expenses.json"
    with open(output_path, "w") as f:
        json.dump(expenses, f, indent=2)

    print(f"✅ Generated {len(expenses)} test expenses → {output_path}")

    # Stats
    categories = {}
    for exp in expenses:
        cat = exp["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\n📊 Category distribution:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}")


if __name__ == "__main__":
    main()
