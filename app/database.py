import mysql.connector
from .config import Config

def get_connection():
    try:
        db_config = Config.get_db_config()
        connection = mysql.connector.connect(**db_config)
        print("데이터베이스 연결 성공")
        
        return connection
    
    except mysql.connector.OperationalError as e:
        print(f"[ERROR] DB 연결 실패: {e}")
        return None

    except mysql.connector.Error as e:
        print(f"[ERROR] DB 오류: {e}")
        return None

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    SQL 쿼리 실행 함수

    Args:
        query (str): 실행할 SQL 쿼리
        params (tuple, optional): 쿼리 파라미터 (기본값: None)
        fetch_one (bool): 단건 결과 반환 여부 (기본값: False)
        fetch_all (bool): 여러건 결과 반환 여부 (기본값: False)
    
    Returns:
        dict or list or None: 쿼리 결과
    """
    conn = get_connection()

    if conn is None:
        print("[ERROR] DB 연결 객체 없음.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)  # 결과를 딕셔너리 형태로 반환
        cursor.execute(query, params or ())
        
        result = None

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        
        return result
    
    except mysql.connector.IntegrityError as e:
        print(f"[ERROR] 무결성 제약 조건 위반: {e}")

    except mysql.connector.Error as e:
        print(f"[ERROR] SQL 실행 중 오류: {e}")
    
    except mysql.connector.Exceptions as e:
        print(f"[ERROR] 알 수 없는 예외 발생: {e}")

    finally:
        cursor.close()
        conn.close()

def test_connection():
    """데이터 베이스 연결 테스트"""
    conn = get_connection()
    if conn:
        print("데이터베이스 연결 테스트 성공")
        conn.close()
        return True
    else:
        print("데이터베이스 연결 테스트 실패")
        return False


