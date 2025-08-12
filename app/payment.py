from .database import execute_query

# 결제 등록
def create_payment(visit_id, payment_data):
    query = """
    INSERT INTO payment (visit_id, amount, payment_method_code, payment_datetime)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        visit_id,
        payment_data["amount"],
        payment_data["payment_method_code"],
        payment_data["payment_datetime"]
    )

    try:
        execute_query(query, values)
        print(f"결제 기록 등록 성공: 방문 ID {visit_id}, 금액 {payment_data['amount']}")
        return True
    
    except Exception as e:
        print(f"결제 기록 등록 실패: {e}")
        return False
    
# 전체 결제 기록 조회
def get_all_payments():
    query = """
    SELECT p.*, v.customer_id, c.name as customer_name, pm.method_name
    FROM payment p
    JOIN visit v ON p.visit_id = v.visit_id
    JOIN customer c ON v.customer_id = c.customer_id
    JOIN payment_method pm ON p.payment_method_code = pm.method_code
    ORDER BY p.payment_datetime DESC
    """

    return execute_query(query, fetch_all=True)

# 고객별 결제 기록 조회
def get_payments_by_customer(customer_id):
    query = """
    SELECT p.*, v.visit_date, pm.method_name
    FROM payment p
    JOIN visit v ON p.visit_id = v.visit_id
    JOIN payment_method pm ON p.payment_method_code = pm.method_code
    WHERE v.customer_id = %s
    ORDER BY p.payment_datetime DESC
    """

    result = execute_query(query, (customer_id,), fetch_all=True)
    return result if result else []
    # return execute_query(query, fetch_all=True)

# 결제 수정
def update_payment(payment_data):
    query = """
    UPDATE payment
    SET amount = %s, payment_method_code = %s, payment_datetime = %s
    WHERE payment_id = %s
    """

    values = (
        payment_data["amount"],
        payment_data["payment_method_code"],
        payment_data["payment_datetime"],
        payment_data["payment_id"]
    )

    try:
        execute_query(query, values)
        print(f"결제 기록 수정 성공: 결제 ID {payment_data['payment_id']}")

        return True

    except Exception as e:
        print(f"결제 기록 수정 실패: {e}")

        return False

# 결제 삭제
def delete_payment(payment_id):
    query = "DELETE FROM payment WHERE payment_id = %s"

    try:
        execute_query(query, (payment_id,))
        print(f"결제 기록 삭제 성공: 결제 ID {payment_id}")

        return True
    
    except Exception as e:
        print(f"결제 기록 삭제 실패: {e}")
        
        return False

# 결제 수단 조회
def get_payment_methods():
    query = "SELECT * FROM payment_method"

    return execute_query(query, fetch_all=True)