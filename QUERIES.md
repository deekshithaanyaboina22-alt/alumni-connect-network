# Main Cypher Queries

## 1. List all alumni with company

```cypher id="hww94u"
MATCH (a:Alumni)-[:WORKS_AT]->(c:Company)
RETURN a.name, a.title, c.name
ORDER BY a.name
```

**Purpose:** Displays the alumni directory with company information.

---

## 2. Search alumni by skill

```cypher id="mq0wz1"
MATCH (a:Alumni)-[:HAS_SKILL]->(s:Skill),
      (a)-[:WORKS_AT]->(c:Company)
WHERE toLower(s.name) = toLower($skill)
RETURN DISTINCT a.name, a.title, c.name
ORDER BY a.name
```

**Purpose:** Finds alumni connected to a specific skill node.

---

## 3. Two-hop mentorship traversal

```cypher id="4s85lo"
MATCH (a:Alumni {id:$id})-[:MENTORS*1..2]->(m:Alumni)
RETURN DISTINCT m.name, m.title
```

**Purpose:** Finds alumni reachable within one or two mentorship relationships.

**Why it is graph-friendly:** Multi-hop relationship traversal is much simpler in a graph database than writing recursive joins in a relational database.
