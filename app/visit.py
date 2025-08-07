from database import execute_query

# 방문 등록
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

    try:
        execute_query(query, values)
        print(f"방문 등록 성공: 고객 ID {customer_id}")

        return True

    except Exception as e:
        print(f"방문 등록 실패: {e}")

        return False

# 전체 방문 기록 조회
def get_visits():
    query = """
    SELECT v.*, c.name as customer_name
    FROM visit v
    JOIN customer c ON v.customer_id = c.customer_id
    ORDER BY visit_date DESC
    """

    return execute_query(query, fetch_all=True)

# 고객별 방문 기록 조회
def get_visits_by_customer(customer_id):
    query = """
    SELECT v.*, c.name as customer_name 
    FROM visit v
    JOIN customer c ON v.customer_id = c.customer_id
    WHERE v.customer_id = %s 
    ORDER BY v.visit_date DESC
    """

    return execute_query(query, (customer_id,), fetch_all=True)

# 방문 기록 수정
def update_visit(visit_id, memo):
    query = """
    UPDATE visit SET memo = %s WHERE visit_id = %s
    """

    try:
        execute_query(query, (memo, visit_id))
        print(f"방문 기록 수정 성공")

        return True

    except Exception as e:
        print(f"방문 기록 수정 실패: {e}")
        
        return False

# 방문 기록 삭제
def delete_visit(visit_id):
    query = "DELETE FROM visit WHERE visit_id = %s"

    try:
        execute_query(query, (visit_id,))
        print("방문 기록 삭제 성공")
        
        return True

    except Exception as e:
        print("방문 기록 삭제 실패")

        return False
    
# 기간별 방문 기록 조회
def get_visits_by_date_range(start_date, end_date):
    query = """
    SELECT v.*, c.name as customer_name
    FROM visit v
    JOIN customer c ON v.customer_id = c.customer_id
    WHERE v.visit_date BETWEEN %s AND %s
    ORDER BY v.visit_date DESC
    """

    result = execute_query(query, fetch_all=True)



