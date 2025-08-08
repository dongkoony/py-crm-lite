from .database import execute_query
from datetime import datetime, timedelta

# 고객별 총 방문 횟수 조회
def get_total_visits_by_customer(customer_id):
    query = "SELECT COUNT(*) total_visits FROM visit WHERE customer_id = %s"

    result = execute_query(query, (customer_id,), fetch_one=True)
    
    return result["total_visits"] if result else 0

# 고객별 총 결제 금액 조회
def get_total_payment_by_customer(customer_id):
    query = """
    SELECT SUM(p.amount) total_amount
    FROM payment p
    JOIN visit v ON p.visit_id = v.visit_id
    WHERE v.customer_id = %s
    """

    result = execute_query(query, (customer_id, ), fetch_one=True)

    return result["total_amount"] if result and result["total_amount"] else 0

# 고객별 통계 정보 조회
def get_customer_statistics(customer_id):
    query = """
    SELECT 
        c.name,
        COUNT(v.visit_id) as total_visits,
        SUM(p.amount) as total_payment,
        AVG(p.amount) as avg_payment,
        MAX(v.visit_date) as last_visit_date,
        MIN(v.visit_date) as first_visit_date
    FROM customer c
    LEFT JOIN visit v ON c.customer_id = v.customer_id
    LEFT JOIN payment p ON v.visit_id = p.visit_id
    WHERE c.customer_id = %s
    GROUP BY c.customer_id, c.name
    """

    result = execute_query(query, (customer_id, ), fetch_one=True)
    
    if result:
        result["total_payment"] = result["total_payment"] or 0
        result["avg_payment"] = result["avg_payment"] or 0
    
    return result

# 전체 통계 조회
def get_overall_statistics():
    query = """
    SELECT 
        COUNT(DISTINCT c.customer_id) as total_customers,
        COUNT(v.visit_id) as total_visits,
        SUM(p.amount) as total_revenue,
        AVG(p.amount) as avg_revenue_per_visit,
        COUNT(DISTINCT DATE(v.visit_date)) as total_visit_days
    FROM customer c
    LEFT JOIN visit v ON c.customer_id = v.customer_id
    LEFT JOIN payment p ON v.visit_id = p.visit_id
    """

    result = execute_query(query, fetch_one=True)
    if result:
        result["total_revenue"] = result["total_revenue"] or 0
        result["avg_revenue_per_visit"] = result["avg_revenue_per_visit"] or 0

    return result

# 월별 통계 조회
def get_monthly_statistics(year, month):
    query = """
    SELECT 
        COUNT(DISTINCT v.customer_id) as unique_customers,
        COUNT(v.visit_id) as total_visits,
        SUM(p.amount) as total_revenue,
        AVG(p.amount) as avg_revenue_per_visit
    FROM visit v
    LEFT JOIN payment p ON v.visit_id = p.visit_id
    WHERE YEAR(v.visit_date) = %s AND MONTH(v.visit_date) = %s
    """

    result = execute_query(query, (year, month), fetch_one=True)

    if result:
        result["total_revenue"] = result["total_revenue"] or 0
        result["avg_revenue_per_visit"] = result["avg_revenue_per_visit"] or 0

    return result