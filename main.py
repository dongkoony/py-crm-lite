from wsgiref.handlers import read_environ

from flask import Flask, request, jsonify, render_template, flash, url_for, redirect
from app.customer import create_customer, get_all_customers, search_customers, update_customer, delete_customer, get_customer_by_birth_month, get_customer_by_customer
from app.visit import create_visit, get_visits, get_visits_by_customer, update_visit, get_visits_by_date_range, \
    get_visit_by_visit_id, delete_visit
from app.payment import create_payment, get_all_payments, get_payments_by_customer, update_payment, delete_payment, get_payment_methods
from app.stats import get_customer_statistics, get_overall_statistics, get_monthly_statistics

from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def home():
    # 전체 통계
    overall_stats = get_overall_statistics()

    # 이번달 생일 고객
    current_month = datetime.now().month
    birth_day_customers = get_customer_by_birth_month(current_month)

    # 최근 방문 기록
    recent_visits = get_visits()[:5] if get_visits() else []

    return render_template("dashboard.html",
                           overall_stats = overall_stats,
                           birth_day_customers = birth_day_customers,
                           recent_visits = recent_visits)

@app.route("/customers")
def customer_list():
    search = request.args.get("search", "")
    birth_month = request.args.get("birth_month", "")

    if search:
        customers = search_customers(search)

    elif birth_month:
        customers = get_customer_by_birth_month(birth_month)

    else:
        customers = get_all_customers()

    return render_template("customers/list.html", customers = customers, search = search, birth_month = birth_month)

@app.route("/customer/new", methods=["GET", "POST"])
def customer_new():
    if request.method == "POST":
        customer_data = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "birth_date": request.form["birth_date"],
            "gender": request.form["gender"],
            "memo": request.form["memo"]
        }

        if create_customer(customer_data):
            flash("등록 성공", "success")
            return redirect(url_for("customer_list"))

        else:
            flash("등록 실패", "error")

    return render_template("customers/new.html")

@app.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    customer = get_customer_by_customer(customer_id)

    if not customer:
        flash("고객을 찾을 수 없습니다.", "error")
        return redirect(url_for("customer_list"))

    stats = get_customer_statistics(customer_id)
    visits = get_visits_by_customer(customer_id)
    payments = get_payments_by_customer(customer_id)

    return render_template("customers/detail.html", customer = customer, stats = stats, visits = visits, payments = payments)

@app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def customer_edit(customer_id):
    customer = get_customer_by_customer(customer_id)

    if not customer:
        flash("고객을 찾을 수 없습니다.", "error")
        return redirect(url_for("customer_list"))

    if request.method == "POST":
        customer_data = {
            "customer_id": customer_id,
            "name": request.form["name"],
            "phone": request.form["phone"],
            "birth_date": request.form["birth_date"],
            "gender": request.form["gender"],
            "memo": request.form["memo"]
        }


        if update_customer(customer_data):
            flash("고객 정보 수정 성공", "success")

        else:
            flash("고객 정보 수정 실패", "error")

    return render_template("customers/edit.html", customer = customer)

@app.route("/customers/<int:customer_id>/delete", methods=["POST"])
def customer_delete(customer_id):
    if delete_customer(customer_id):
        flash("고객 삭제 성공", "success")

    else:
        flash("고객 삭제 실패", "error")

    return redirect(url_for("customer_list"))

@app.route("/routes")
def visit_list():
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    if start_date and end_date:
        visits = get_visits_by_date_range(start_date, end_date)

    else:
        visits = get_visits()

    return render_template("visits/list.html", visits = visits, start_date = start_date, end_date = end_date)

@app.route("/visits/new", methods=["GET", "POST"])
def visit_new():
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        visit_data = {
            "visit_date": request.form["visit_date"],
            "memo": request.form["memo"]
        }

        if create_visit(customer_id, visit_data):
            flash("방문 기록 저장 성공", "success")

        else:
            flash("방문 기록 저장 실패", "error")

    customers = get_all_customers()
    return render_template("visits/new.html", customers = customers)

@app.route("/visits/<int:visit_id>/edit", medthods=["GET", "POST"])
def visit_edit(visit_id):
    visit = get_visit_by_visit_id(visit_id)

    if not visit:
        flash("방문 기록을 찾을 수 없습니다", "error")
        return redirect(url_for("visit_list"))

    if request.method == "POST":

        memo = request.form["memo"]
        if update_visit(visit_id, memo):
            flash("방문 기록 수정 성공", "success")
            return redirect(url_for("visit_list"))

        else:
            flash("방문 기록 수정 실패", "error")

    return render_template("visits/edit.html", visit = visit)

@app.route("/visits/<int:visit_id>/delete", methods=["POST"])
def visit_delete(visit_id):
    if delete_visit(visit_id):
        flash("방문 기록 삭제 성공", "success")

    else:
        flash("방문 기록 삭제 실패", "error")

    return redirect(url_for("visit_list"))

@app.route("/payments")
def payment_list():
    payments = get_all_payments()
    return render_template("payments/list.html", payments = payments)

@app.route("/payments/new", methods=["GET","POST"])
def payment_new():
    if request.method == "POST":
        visit_id = request.form["visit_id"]
        payment_data = {
            "amount": request.form["amount"],
            "payment_method_code": request.form["payment_method_code"],
            "payment_datetime": request.form["payment_datetime"]
        }

        if create_payment(visit_id, payment_data):
            flash("결제 정보 등록 성공", "success")
            redirect(url_for("payment_list"))

        else:
            flash("결제 정보 등록 실패", "error")

    visits = get_visits()
    payment_methods = get_payment_methods()
    return render_template("payments/new.html", visits = visits, payment_methods = payment_methods)

@app.route("/stats")
def stats_dashboard():
    overall_stats = get_overall_statistics()

    current_date = datetime.now()
    monthly_stats = get_monthly_statistics(current_date.year, current_date.month)

    # 월별 통계
    monthly_data = []
    for i in range(6):
        month_date = current_date.replace(day=1) - timedelta(days=i*30)
        month_stats = get_monthly_statistics(month_date.year, month_date.month)
        monthly_data.append({
            "year": month_date.year,
            "month": month_date.month,
            "stats": month_stats
        })

    return render_template("stats/dashboard.html", overall_stats = overall_stats, monthly_stats = monthly_stats, monthly_data = monthly_data)

@app.route("/stats/customers")
def stats_customers():
    customers = get_all_customers()
    customer_stats = []

    for customer in customers:
        stats = get_customer_statistics(customers["customer_id"])
        if stats:
            customer_stats.append({
                "customer": customer,
                "stats": stats
            })

    return render_template("stats/customers.html", customer_stats = customer_stats)