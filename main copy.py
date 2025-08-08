from app import customer, visit, payment, stats
import datetime

if __name__ == "__main__":
    # 고객 등록
    customer.create_customer("홍길동", "010-1234-5678", "1990-01-01", "M", "VIP 고객")

    # 고객 목록 조회
    customers = customer.get_all_customers()
    print("고객 목록:", customers)

    # 방문 기록 등록
    first_customer_id = customers[0]['customer_id']
    visit.create_visit(first_customer_id, datetime.datetime.now(), "첫 방문")

    # 방문 내역 조회
    visits = visit.get_visits_by_customer(first_customer_id)
    print("방문 내역:", visits)

    # 결제 등록
    first_visit_id = visits[0]['visit_id']
    payment.create_payment(first_visit_id, 50000, "CASH", datetime.datetime.now())

    # 결제 내역 조회
    payments = payment.get_payments_by_visit(first_visit_id)
    print("결제 내역:", payments)

    # 통계 조회
    total_visits = stats.get_total_visits_by_customer(first_customer_id)
    total_payment = stats.get_total_payment_by_customer(first_customer_id)
    print(f"총 방문 횟수: {total_visits}, 총 결제 금액: {total_payment}")
