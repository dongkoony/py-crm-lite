from database import execute_query

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

    execute_query(query, values)


def update_payment(payment_data):
    query = """
    UPDATE payment
    SET amount = %s, payment_method_code = %s, payment_datetime = %s
    WHERE payment_id = %s
    """

    values = (
        payment_data["amount"],
        payment_data["payment_method_code"],
        payment_data["payment_datetime"]
    )

    execute_query(query, values)

def delete_payment(payment_id):
    query = "DELETE FROM payment WHERE payment_id = %s"

    execute_query(query, (payment_id,))