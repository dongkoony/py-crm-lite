from flask import Blueprint, request, render_template, flash, url_for, redirect
from app.customer import (
    create_customer, get_all_customers, search_customers, 
    update_customer, delete_customer, get_customer_by_birth_month, 
    get_customer_by_customer
)
from app.visit import get_visits_by_customer
from app.payment import get_payments_by_customer
from app.stats import get_customer_statistics

customer_bp = Blueprint('customer', __name__)

@customer_bp.route("/customers")
def customer_list():
    search = request.args.get("search", "")
    birth_month = request.args.get("birth_month", "")

    if search:
        customers = search_customers(search)
    elif birth_month:
        customers = get_customer_by_birth_month(birth_month)
    else:
        customers = get_all_customers()

    return render_template("customers/list.html", 
                         customers=customers, 
                         search=search, 
                         birth_month=birth_month)

@customer_bp.route("/customer/new", methods=["GET", "POST"])
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
            return redirect(url_for("customer.customer_list"))
        else:
            flash("등록 실패", "error")

    return render_template("customers/new.html")

@customer_bp.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    customer = get_customer_by_customer(customer_id)

    if not customer:
        flash("고객을 찾을 수 없습니다.", "error")
        return redirect(url_for("customer.customer_list"))

    stats = get_customer_statistics(customer_id)
    visits = get_visits_by_customer(customer_id)
    payments = get_payments_by_customer(customer_id)

    return render_template("customers/detail.html", 
                         customer=customer, 
                         stats=stats, 
                         visits=visits, 
                         payments=payments)

@customer_bp.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def customer_edit(customer_id):
    customer = get_customer_by_customer(customer_id)

    if not customer:
        flash("고객을 찾을 수 없습니다.", "error")
        return redirect(url_for("customer.customer_list"))

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
            return redirect(url_for("customer.customer_detail", customer_id=customer_id))
        else:
            flash("고객 정보 수정 실패", "error")

    return render_template("customers/edit.html", customer=customer)

@customer_bp.route("/customers/<int:customer_id>/delete", methods=["POST"])
def customer_delete(customer_id):
    if delete_customer(customer_id):
        flash("고객 삭제 성공", "success")
    else:
        flash("고객 삭제 실패", "error")

    return redirect(url_for("customer.customer_list"))