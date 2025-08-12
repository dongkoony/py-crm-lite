# main.py

from flask import Flask, render_template
from datetime import datetime
import secrets

# Blueprint 임포트
from routes.customer_routes import customer_bp
from routes.visit_routes import visit_bp
from routes.payment_routes import payment_bp
from routes.stats_routes import stats_bp

# 비즈니스 로직 임포트 (홈페이지용)
from app.customer import get_customer_by_birth_month
from app.visit import get_visits
from app.stats import get_overall_statistics

def create_app():
    """Flask 애플리케이션 팩토리 함수"""
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
    
    # Blueprint 등록
    app.register_blueprint(customer_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(stats_bp)
    
    # 홈페이지 라우트
    @app.route("/")
    def home():
        # 전체 통계
        overall_stats = get_overall_statistics()
        
        # 이번달 생일 고객 조회
        current_month = datetime.now().month
        birth_day_customers = get_customer_by_birth_month(current_month)
        
        # 최근 방문 기록
        all_visits = get_visits()
        recent_visits = all_visits[:5] if all_visits else []
        
        return render_template("dashboard.html",
                             overall_stats=overall_stats or {},
                             birth_day_customers=birth_day_customers or [],
                             recent_visits=recent_visits)
    
    return app

# 애플리케이션 생성
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)