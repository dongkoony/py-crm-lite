from database import execute_query

"""
고객 관리 모듈
"""

# 고객 등록
def create_customer(customer_data):
    query = """
    INSERT INTO customer (name, phone, birth_date, gender, memo)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        customer_data["name"],
        customer_data["phone"],
        customer_data["birth_date"],
        customer_data["gender"],
        customer_data["memo"]
    )

    try:
        execute_query(query, values)
        print(f"고객 등록 성공: {customer_data["name"]}")
       
        return True
    
    except Exception as e:
        print(f"고객 등록 실패: {e}")
        
        return False

# 전체 고객 조회
def get_all_customers():
    query = "SELECT * FROM customer ORDER BY name"

    return execute_query(query, fetch_all=True)

# 고객 검색
def search_customers(search_term):
    query = """
    SELECT * FROM customer
    WHERE name LIKE %s OR phone LIKE %s OR birth_date LIKE %s
    """

    keywords = f"%{search_term}%"

    return execute_query(query, (keywords, keywords, keywords), fetch_all=True)
    
# 고객 정보 수정
def update_customer(customer_data):
    query = """
    UPDATE customer
    set name = %s, phone = %s, birth_date = %s, gender = %s, memo= %s
    WHERE customer_id = %s
    """
    values = (
        customer_data["name"],
        customer_data["phone"],
        customer_data["birth_date"],
        customer_data["gender"],
        customer_data["memo"],
        customer_data["customer_id"]
    )

    try:
        execute_query(query, values)
        print(f"고객 정보 수정 성공: {customer_data["name"]}")
    
        return True
    
    except Exception as e:
        print(f"고객 정보 수정 실패: {e}")
        
        return False

# 고객 삭제
def delete_customer(customer_id):
    query = "DELETE FROM customer WHERE customer_id = %s"
    
    try:
        execute_query(query, (customer_id,))
        print("고객 삭제 성공: {customer_id}")

        return True
    
    except Exception as e:
        print("고객 삭제 실패: {e}")
        
        return False
    
# 특정 월에 생일인 고객 조회
def get_customer_by_birth_month(month):
    query = """
    SELECT * FROM customer
    WHERE MONTH(birth_date) = %s
    ORDER BY DAY(birth_date), name
    """

    return execute_query(query, (month,), fetch_all=True)