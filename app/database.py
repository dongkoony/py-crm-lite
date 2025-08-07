import mysql.connector

dbconfig = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "mydb",
    "raise_on_warnings": True,
    "autocommit": True
}

def get_connection():
    try:
        return mysql.connector.connect(**dbconfig)
    
    except mysql.connector.OperationalError as e:
        print(f"[ERROR] DB 연결 실패: {e}")
        return None

    except mysql.connector.Error as e:
        print(f"[ERROR] DB 오류: {e}")
        return None

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    conn = get_connection()

    if conn is None:
        print("[ERROR] DB 연결 객체 없음.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
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


