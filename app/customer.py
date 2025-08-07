from database import execute_query

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
    
    execute_query(query, values)

def get_customers():
    query = "SELECT * FROM customer"
    return execute_query(query, fetch_all=True)

def search_customers(search_term):
    query = """
    SELECT * FROM customer
    WHERE name LIKE %s OR phone LIKE %s OR birth_date LIKE %s
    """

    keywords = f"%{search_term}%"

    return execute_query(query, (keywords, keywords, keywords), fetch_all=True)
    
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

    execute_query(query, values)

def delete_customer(customer_id):
    query = "DELETE FROM customer WHERE customer_id = %s"
    
    execute_query(query, (customer_id,))