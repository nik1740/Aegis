"""
Graph Queries — Cypher query templates for Neo4j policy traversal.

Provides deterministic graph traversal to retrieve exact policy subgraphs
for a given employee + category + location combination.
This is the core of the GraphRAG engine.
"""

import os
from typing import Any

import structlog
from neo4j import GraphDatabase

logger = structlog.get_logger()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "aegis_graph")


class GraphQueryEngine:
    """Executes Cypher queries against the Neo4j policy knowledge graph."""

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def get_policy_subgraph(self, employee_id: str, category: str, location: str) -> dict[str, Any]:
        """
        Retrieve the exact policy subgraph applicable to an employee.

        Performs deterministic graph traversal:
        Employee → Role → PolicyRule ← ExpenseCategory
        with optional Location modifiers and Exemptions.

        Args:
            employee_id: The employee's unique identifier.
            category: The expense category (e.g., "meals", "transport").
            location: The employee's location city.

        Returns:
            Dictionary containing the applicable rules, limits, and exemptions.
        """
        query = """
        MATCH (emp:Employee {id: $employee_id})-[:HAS_ROLE]->(role:Role)
        MATCH (emp)-[:LOCATED_IN]->(loc:Location {city: $location})
        MATCH (cat:ExpenseCategory {name: $category})
        MATCH (role)-[:SUBJECT_TO]->(rule:PolicyRule)<-[:ENFORCED_BY]-(cat)
        OPTIONAL MATCH (loc)-[:MODIFIES_LIMIT]->(rule)
        OPTIONAL MATCH (rule)-[:EXEMPTS]->(exempt:Exemption)
        WHERE rule.effective_date <= date() AND (rule.expiry_date IS NULL OR rule.expiry_date >= date())
        RETURN rule.rule_id AS rule_id,
               rule.description AS description,
               rule.limit_amount AS limit_amount,
               rule.limit_currency AS limit_currency,
               rule.limit_period AS limit_period,
               loc.cost_index AS cost_index,
               exempt AS exemption
        ORDER BY rule.effective_date DESC
        LIMIT 1
        """
        with self.driver.session() as session:
            result = session.run(
                query,
                employee_id=employee_id,
                category=category,
                location=location,
            )
            records = [record.data() for record in result]

        logger.info(
            "policy_subgraph_retrieved",
            employee_id=employee_id,
            category=category,
            location=location,
            rules_found=len(records),
        )

        return {
            "employee_id": employee_id,
            "category": category,
            "location": location,
            "applicable_rules": records,
            "traversal_path": f"Employee({employee_id}) → Role → PolicyRule ← ExpenseCategory({category})",
        }

    def get_employee_profile(self, employee_id: str) -> dict[str, Any]:
        """
        Retrieve the full employee profile from the graph.

        Returns employee details with role, department, and location.
        """
        query = """
        MATCH (emp:Employee {id: $employee_id})
        OPTIONAL MATCH (emp)-[:HAS_ROLE]->(role:Role)
        OPTIONAL MATCH (emp)-[:BELONGS_TO]->(dept:Department)
        OPTIONAL MATCH (emp)-[:LOCATED_IN]->(loc:Location)
        RETURN emp, role, dept, loc
        """
        with self.driver.session() as session:
            result = session.run(query, employee_id=employee_id)
            record = result.single()

        if record is None:
            return {}

        return {
            "employee": dict(record["emp"]) if record["emp"] else None,
            "role": dict(record["role"]) if record["role"] else None,
            "department": dict(record["dept"]) if record["dept"] else None,
            "location": dict(record["loc"]) if record["loc"] else None,
        }

    def get_all_rules_for_category(self, category: str) -> list[dict]:
        """Retrieve all active policy rules for a given expense category."""
        query = """
        MATCH (cat:ExpenseCategory {name: $category})-[:ENFORCED_BY]->(rule:PolicyRule)
        WHERE rule.effective_date <= date() AND (rule.expiry_date IS NULL OR rule.expiry_date >= date())
        RETURN rule
        ORDER BY rule.limit_amount ASC
        """
        with self.driver.session() as session:
            result = session.run(query, category=category)
            return [dict(record["rule"]) for record in result]
