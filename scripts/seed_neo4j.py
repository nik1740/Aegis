"""
Seed Neo4j — Initialize the policy knowledge graph with sample data.

Usage:
    poetry run python scripts/seed_neo4j.py

Loads the sample policy from knowledge_graph/seed_data/sample_policy.json
and builds the complete Neo4j graph (employees, roles, departments,
locations, categories, policy rules, and all relationships).
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_graph.graph_builder import GraphBuilder


def seed_neo4j() -> None:
    """Seed the Neo4j database with sample policy data."""
    print("🔵 Loading sample policy data...")
    policy_path = Path(__file__).parent.parent / "knowledge_graph" / "seed_data" / "sample_policy.json"

    with open(policy_path) as f:
        policy = json.load(f)

    print(f"   Company: {policy['company_name']}")
    print(f"   Version: {policy['policy_version']}")
    print(f"   Rules: {len(policy['rules'])}")
    print(f"   Employees: {len(policy['employees'])}")

    builder = GraphBuilder()

    try:
        # Clear existing graph
        print("\n🗑️  Clearing existing graph...")
        builder.clear_graph()

        # Create constraints
        print("🔒 Creating constraints...")
        builder.create_constraints()

        # Create roles
        print("\n📋 Creating roles...")
        for role in policy["roles"]:
            builder.create_role(role["id"], role["title"], role["tier"], role["seniority_level"])
            print(f"   ✅ {role['title']} (Tier {role['tier']})")

        # Create departments
        print("\n🏢 Creating departments...")
        for dept in policy["departments"]:
            builder.create_department(dept["id"], dept["name"], dept["cost_center"], dept["budget"])
            print(f"   ✅ {dept['name']} ({dept['cost_center']})")

        # Create locations
        print("\n📍 Creating locations...")
        for loc in policy["locations"]:
            builder.create_location(loc["id"], loc["city"], loc["country"], loc["region"], loc["cost_index"])
            print(f"   ✅ {loc['city']}, {loc['country']} (cost_index: {loc['cost_index']})")

        # Create categories
        print("\n📂 Creating expense categories...")
        for cat in policy["categories"]:
            builder.create_category(cat["name"], cat["requires_receipt"], cat["requires_preapproval"])
            print(f"   ✅ {cat['name']}")

        # Create policy rules and link to roles/categories/locations
        print("\n📜 Creating policy rules...")
        for rule in policy["rules"]:
            builder.create_policy_rule(
                rule["rule_id"], rule["description"],
                rule["limit_amount"], rule["limit_currency"],
                rule["limit_period"], rule["effective_date"],
                rule.get("expiry_date"),
            )
            print(f"   ✅ {rule['rule_id']}: {rule['description']}")

            # Link to applicable roles
            for role_id in rule.get("applicable_roles", []):
                builder.link_role_rule(role_id, rule["rule_id"])

            # Link to category
            builder.link_category_rule(rule["category"], rule["rule_id"])

            # Link to applicable locations
            for loc_id in rule.get("applicable_locations", []):
                builder.link_location_rule(loc_id, rule["rule_id"])

        # Create employees and link to roles/departments/locations
        print("\n👤 Creating employees...")
        for emp in policy["employees"]:
            builder.create_employee(emp["id"], emp["name"], emp["email"])
            builder.link_employee_role(emp["id"], emp["role_id"])
            builder.link_employee_department(emp["id"], emp["dept_id"])
            builder.link_employee_location(emp["id"], emp["loc_id"])
            print(f"   ✅ {emp['name']} ({emp['id']})")

        print("\n" + "=" * 50)
        print("✅ Neo4j graph seeded successfully!")
        print(f"   Roles: {len(policy['roles'])}")
        print(f"   Departments: {len(policy['departments'])}")
        print(f"   Locations: {len(policy['locations'])}")
        print(f"   Categories: {len(policy['categories'])}")
        print(f"   Rules: {len(policy['rules'])}")
        print(f"   Employees: {len(policy['employees'])}")
        print("=" * 50)

    finally:
        builder.close()


if __name__ == "__main__":
    seed_neo4j()
