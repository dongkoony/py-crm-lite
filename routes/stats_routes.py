from flask import Blueprint, render_template
from app.stats import get_overall_statistics, get_monthly_statistics, get_customer_statistics
from app.customer import get_all_customers
from datetime import datetime, timedelta

stats_bp = Blueprint('stats', __name__)

@stats_bp.route("/stats")
def stats_dashboard():
    overall_stats = get_overall_statistics()
    current_date = datetime.now()
    monthly_stats = get_monthly_statistics(current_date.year, current_date.month)

    # 월별 통계 (최근 6개월)
    monthly_data = []
    for i in range(6):
        month_date = current_date.replace(day=1) - timedelta(days=i*30)
        month_stats = get_monthly_statistics(month_date.year, month_date.month)
        monthly_data.append({
            "year": month_date.year,
            "month": month_date.month,
            "stats": month_stats
        })

    return render_template("stats/dashboard.html", 
                         overall_stats=overall_stats, 
                         monthly_stats=monthly_stats, 
                         monthly_data=monthly_data)

@stats_bp.route("/stats/customers")
def stats_customers():
    customers = get_all_customers()
    customer_stats = []

    for customer in customers:
        # 버그 수정: customers -> customer
        stats = get_customer_statistics(customer["customer_id"])
        if stats:
            customer_stats.append({
                "customer": customer,
                "stats": stats
            })

    return render_template("stats/customers.html", customer_stats=customer_stats)