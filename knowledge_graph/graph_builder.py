"""
Graph Builder — Constructs the Neo4j policy knowledge graph.

Creates nodes and edges in Neo4j from parsed policy data:
- Employee nodes
- Role nodes (with seniority tiers)
- Department nodes
- Location nodes (with cost indices)
- ExpenseCategory nodes
- PolicyRule nodes (with limits, periods, dates)
- Exemption nodes

Relationships:
- HAS_ROLE, BELONGS_TO, LOCATED_IN
- SUBJECT_TO, ENFORCED_BY, MODIFIES_LIMIT
- EXEMPTS, OVERRIDES, REQUIRES_APPROVAL_FROM
"""

import os

import structlog
from neo4j import GraphDatabase

logger = structlog.get_logger()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "aegis_graph")


class GraphBuilder:
    """Builds and manages the Neo4j policy knowledge graph."""

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        logger.info("graph_builder_initialized", uri=NEO4J_URI)

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def clear_graph(self) -> None:
        """Clear all nodes and relationships (use with caution)."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.warning("graph_cleared")

    def create_constraints(self) -> None:
        """Create uniqueness constraints on node IDs."""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Employee) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (r:Role) REQUIRE r.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Department) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:ExpenseCategory) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:PolicyRule) REQUIRE p.rule_id IS UNIQUE",
        ]
        with self.driver.session() as session:
            for constraint in constraints:
                session.run(constraint)
        logger.info("graph_constraints_created", count=len(constraints))

    def create_employee(self, employee_id: str, name: str, email: str) -> None:
        """Create an Employee node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (e:Employee {id: $id}) SET e.name = $name, e.email = $email",
                id=employee_id, name=name, email=email,
            )

    def create_role(self, role_id: str, title: str, tier: int, seniority_level: str) -> None:
        """Create a Role node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (r:Role {id: $id}) SET r.title = $title, r.tier = $tier, r.seniority_level = $seniority_level",
                id=role_id, title=title, tier=tier, seniority_level=seniority_level,
            )

    def create_department(self, dept_id: str, name: str, cost_center: str, budget: float) -> None:
        """Create a Department node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (d:Department {id: $id}) SET d.name = $name, d.cost_center = $cost_center, d.budget = $budget",
                id=dept_id, name=name, cost_center=cost_center, budget=budget,
            )

    def create_location(self, loc_id: str, city: str, country: str, region: str, cost_index: float) -> None:
        """Create a Location node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (l:Location {id: $id}) SET l.city = $city, l.country = $country, "
                "l.region = $region, l.cost_index = $cost_index",
                id=loc_id, city=city, country=country, region=region, cost_index=cost_index,
            )

    def create_category(self, name: str, requires_receipt: bool = True, requires_preapproval: bool = False) -> None:
        """Create an ExpenseCategory node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (c:ExpenseCategory {name: $name}) "
                "SET c.requires_receipt = $requires_receipt, c.requires_preapproval = $requires_preapproval",
                name=name, requires_receipt=requires_receipt, requires_preapproval=requires_preapproval,
            )

    def create_policy_rule(self, rule_id: str, description: str, limit_amount: float,
                           limit_currency: str, limit_period: str,
                           effective_date: str, expiry_date: str | None = None) -> None:
        """Create a PolicyRule node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (p:PolicyRule {rule_id: $rule_id}) "
                "SET p.description = $description, p.limit_amount = $limit_amount, "
                "p.limit_currency = $limit_currency, p.limit_period = $limit_period, "
                "p.effective_date = date($effective_date), "
                "p.expiry_date = CASE WHEN $expiry_date IS NOT NULL THEN date($expiry_date) ELSE NULL END",
                rule_id=rule_id, description=description, limit_amount=limit_amount,
                limit_currency=limit_currency, limit_period=limit_period,
                effective_date=effective_date, expiry_date=expiry_date,
            )

    def link_employee_role(self, employee_id: str, role_id: str) -> None:
        """Create HAS_ROLE relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (e:Employee {id: $eid}), (r:Role {id: $rid}) MERGE (e)-[:HAS_ROLE]->(r)",
                eid=employee_id, rid=role_id,
            )

    def link_employee_department(self, employee_id: str, dept_id: str) -> None:
        """Create BELONGS_TO relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (e:Employee {id: $eid}), (d:Department {id: $did}) MERGE (e)-[:BELONGS_TO]->(d)",
                eid=employee_id, did=dept_id,
            )

    def link_employee_location(self, employee_id: str, loc_id: str) -> None:
        """Create LOCATED_IN relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (e:Employee {id: $eid}), (l:Location {id: $lid}) MERGE (e)-[:LOCATED_IN]->(l)",
                eid=employee_id, lid=loc_id,
            )

    def link_role_rule(self, role_id: str, rule_id: str) -> None:
        """Create SUBJECT_TO relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (r:Role {id: $rid}), (p:PolicyRule {rule_id: $pid}) MERGE (r)-[:SUBJECT_TO]->(p)",
                rid=role_id, pid=rule_id,
            )

    def link_category_rule(self, category_name: str, rule_id: str) -> None:
        """Create ENFORCED_BY relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (c:ExpenseCategory {name: $cname}), (p:PolicyRule {rule_id: $pid}) "
                "MERGE (c)-[:ENFORCED_BY]->(p)",
                cname=category_name, pid=rule_id,
            )

    def link_location_rule(self, loc_id: str, rule_id: str) -> None:
        """Create MODIFIES_LIMIT relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (l:Location {id: $lid}), (p:PolicyRule {rule_id: $pid}) "
                "MERGE (l)-[:MODIFIES_LIMIT]->(p)",
                lid=loc_id, pid=rule_id,
            )

    def build_from_policy(self, policy_data: dict) -> None:
        """Build the complete graph from a parsed policy dictionary."""
        # TODO: Full implementation using PolicyParser output
        logger.info("graph_build_started")
        self.create_constraints()
        logger.info("graph_build_complete")
