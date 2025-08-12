from flask import Blueprint, request, render_template, flash, url_for, redirect
from app.visit import (
    create_visit, get_visits, get_visits_by_date_range, 
    get_visit_by_visit_id, update_visit, delete_visit
)
from app.customer import get_all_customers
from datetime import datetime

visit_bp = Blueprint('visit', __name__)

@visit_bp.route("/visits")
# 기존 /routes 경로도 지원하기 위한 추가 라우트
@visit_bp.route("/routes")
def visit_list():
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    if start_date and end_date:
        visits = get_visits_by_date_range(start_date, end_date)
    else:
        visits = get_visits()

    return render_template("visits/list.html", 
                         visits=visits, 
                         start_date=start_date, 
                         end_date=end_date)

@visit_bp.route("/visits/new", methods=["GET", "POST"])
def visit_new():
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        visit_data = {
            "visit_date": request.form["visit_date"],
            "memo": request.form["memo"]
        }

        if create_visit(customer_id, visit_data):
            flash("방문 기록 저장 성공", "success")
            return redirect(url_for("visit.visit_list"))
        else:
            flash("방문 기록 저장 실패", "error")

    customers = get_all_customers()
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("visits/new.html", customers=customers, today=today)

@visit_bp.route("/visits/<int:visit_id>/edit", methods=["GET", "POST"])
def visit_edit(visit_id):
    visit = get_visit_by_visit_id(visit_id)

    if not visit:
        flash("방문 기록을 찾을 수 없습니다", "error")
        return redirect(url_for("visit.visit_list"))

    if request.method == "POST":
        memo = request.form["memo"]
        if update_visit(visit_id, memo):
            flash("방문 기록 수정 성공", "success")
            return redirect(url_for("visit.visit_list"))
        else:
            flash("방문 기록 수정 실패", "error")

    return render_template("visits/edit.html", visit=visit)

@visit_bp.route("/visits/<int:visit_id>/delete", methods=["POST"])
def visit_delete(visit_id):
    if delete_visit(visit_id):
        flash("방문 기록 삭제 성공", "success")
    else:
        flash("방문 기록 삭제 실패", "error")

    return redirect(url_for("visit.visit_list"))