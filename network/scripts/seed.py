from backend.graph import driver


def seed_data():
    with driver.session() as session:

        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")

        query = """
        CREATE
        (a1:Alumni {id:1, name:'Priya Sharma', title:'Software Engineer', location:'Hyderabad'}),
        (a2:Alumni {id:2, name:'Rahul Verma', title:'Backend Developer', location:'Bangalore'}),
        (a3:Alumni {id:3, name:'Ananya Rao', title:'Data Analyst', location:'Pune'}),
        (a4:Alumni {id:4, name:'Kiran Patel', title:'ML Engineer', location:'Hyderabad'}),

        (s1:Skill {name:'Python'}),
        (s2:Skill {name:'Django'}),
        (s3:Skill {name:'SQL'}),
        (s4:Skill {name:'Machine Learning'}),
        (s5:Skill {name:'React'}),

        (c1:Company {name:'Infosys'}),
        (c2:Company {name:'TCS'}),
        (c3:Company {name:'Wipro'}),

        (a1)-[:HAS_SKILL]->(s1),
        (a1)-[:HAS_SKILL]->(s2),
        (a1)-[:WORKS_AT]->(c1),

        (a2)-[:HAS_SKILL]->(s1),
        (a2)-[:HAS_SKILL]->(s3),
        (a2)-[:WORKS_AT]->(c2),

        (a3)-[:HAS_SKILL]->(s3),
        (a3)-[:HAS_SKILL]->(s4),
        (a3)-[:WORKS_AT]->(c1),

        (a4)-[:HAS_SKILL]->(s1),
        (a4)-[:HAS_SKILL]->(s4),
        (a4)-[:WORKS_AT]->(c3),

        (a1)-[:MENTORS]->(a2),
        (a2)-[:MENTORS]->(a3),
        (a1)-[:MENTORS]->(a4)
        """

        session.run(query)

    print("Seed data inserted successfully!")


if __name__ == "__main__":
    seed_data()

