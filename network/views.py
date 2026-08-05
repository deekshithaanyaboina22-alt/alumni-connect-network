from django.http import JsonResponse
from django.shortcuts import render
from backend.graph import driver
from neo4j.exceptions import ServiceUnavailable



# Homepage - Alumni Directory with Skill Search
def alumni_list(request):

    skill = request.GET.get("skill", "").strip()

    try:
        with driver.session() as session:

            if skill:

                query = """
                MATCH (a:Alumni)-[:HAS_SKILL]->(s:Skill),
                      (a)-[:WORKS_AT]->(c:Company)
                WHERE toLower(s.name) = toLower($skill)
                RETURN DISTINCT a.id AS id,
                                a.name AS name,
                                a.title AS title,
                                a.location AS location,
                                c.name AS company
                ORDER BY a.name
                """

                result = session.run(query, skill=skill)

            else:

                query = """
                MATCH (a:Alumni)-[:WORKS_AT]->(c:Company)
                RETURN a.id AS id,
                       a.name AS name,
                       a.title AS title,
                       a.location AS location,
                       c.name AS company
                ORDER BY a.name
                """

                result = session.run(query)

            alumni = [dict(record) for record in result]

        return render(request, "network/alumni_list.html", {
            "alumni_list": alumni,
            "selected_skill": skill
        })

    except ServiceUnavailable:

        return render(request, "network/alumni_list.html", {
            "alumni_list": [],
            "selected_skill": skill,
            "db_error": "Database is temporarily unavailable. Please try again later."
        })



# API Endpoint - JSON response
def alumni_api(request):

    with driver.session() as session:

        query = """
        MATCH (a:Alumni)-[:WORKS_AT]->(c:Company)
        RETURN a.id AS id,
               a.name AS name,
               a.title AS title,
               a.location AS location,
               c.name AS company
        ORDER BY a.name
        """

        result = session.run(query)

        alumni = [dict(record) for record in result]

    return JsonResponse(alumni, safe=False)

    return JsonResponse(alumni, safe=False)


# Alumni Detail Page with 2-Hop Mentorship Traversal
def alumni_detail(request, alumni_id):

    with driver.session() as session:

        # Alumni details
        detail_query = """
        MATCH (a:Alumni {id:$id})-[:WORKS_AT]->(c:Company)
        OPTIONAL MATCH (a)-[:HAS_SKILL]->(s:Skill)
        RETURN a.id AS id,
               a.name AS name,
               a.title AS title,
               a.location AS location,
               c.name AS company,
               collect(s.name) AS skills
        """

        detail_result = session.run(detail_query, id=alumni_id).single()

        if not detail_result:
            return render(request, "network/alumni_not_found.html")

        alumni = dict(detail_result)

        # 2-hop mentorship traversal
        recommendation_query = """
        MATCH (a:Alumni {id:$id})-[:MENTORS*1..2]->(m:Alumni)
        RETURN DISTINCT m.id AS id,
                        m.name AS name,
                        m.title AS title
        """

        recommendation_result = session.run(recommendation_query, id=alumni_id)

        recommendations = [dict(record) for record in recommendation_result]

    return render(request, "network/alumni_detail.html", {
        "alumni": alumni,
        "recommendations": recommendations
    })


