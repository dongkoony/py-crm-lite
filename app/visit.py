from database import execute_query

def create_visit(customer_id, visit_data):
    query = """
    INSERT INTO visit (customer_id, visit_date, memo)
    VALUES (%s, %s, %s)
    """

    values = (
    customer_id,
    visit_data["visit_date"],
    visit_data["memo"]
    )

    execute_query(query, values)

def get_visits():
    query = "SELECT * FROM visit ORDER BY visit_date DESC"

    return execute_query(query, fetch_all=True)

def get_visits_by_customer(customer_id):
    query = """
    SELECT * FROM visit WHERE customer_id = %s ORDER BY visit_date DESC
    """

    return execute_query(query, (customer_id,), fetch_all=True)

def update_visit(visit_id, memo):
    query = """
    UPDATE visit SET memo = %s WHERE visit_id = %s
    """

    execute_query(query, (memo, visit_id))

def delete_visit(visit_id):
    query = "DELETE FROM visit WHERE visit_id = %s"

    execute_query(query, (visit_id,))



