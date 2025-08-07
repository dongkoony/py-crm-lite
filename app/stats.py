from database import execute_query

def get_total_visits_by_customer(customer_id):
    query = "SELECT COUNT(*) total_visits FROM visit WHERE customer_id = %s"

    result = execute_query(query, (customer_id,), fetch_one=True)
    
    return result["total_visits"] if result else 0

def get_total_payment_by_customer(customer_id):
    query = """
    SELECT SUM(p.amount) total_amount
    FROM payment p
    JOIN visit v ON p.visit_id = v.visit_id
    WHERE v.customer_id = %s
    """

    result = execute_query(query, (customer_id, ), fetch_one=True)

    return result["total_amount"] if result and result["total_amount"] else 0