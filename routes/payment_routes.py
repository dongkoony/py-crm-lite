from flask import Blueprint, request, render_template, flash, url_for, redirect
from app.payment import (
    create_payment, delete_payment, get_all_payments, get_payment_methods
)
from app.visit import get_visits

payment_bp = Blueprint('payment', __name__)

@payment_bp.route("/payments")
def payment_list():
    payments = get_all_payments()
    return render_template("payments/list.html", payments=payments)

@payment_bp.route("/payments/new", methods=["GET", "POST"])
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
            return redirect(url_for("payment.payment_list"))
        else:
            flash("결제 정보 등록 실패", "error")

    visits = get_visits()
    payment_methods = get_payment_methods()
    return render_template("payments/new.html", 
                         visits=visits, 
                         payment_methods=payment_methods)

@payment_bp.route("/payments/<int:payment_id>/delete", methods=["POST"])
def payment_delete(payment_id):
    if delete_payment(payment_id):
        flash("결제 삭제 성공", "success")
    else:
        flash("결제 삭제 실패", "error")

    return redirect(url_for("payment.payment_list"))