# 리팩토링 테스트 가이드

## 개요

리팩토링된 Flask CRM 시스템의 테스트 방법과 검증 절차를 상세히 설명하는 문서입니다. 데이터베이스 유무에 관계없이 애플리케이션을 안전하게 테스트할 수 있는 방법들을 제시합니다.

## 테스트 환경 분류

### 1. 데모 모드 (MySQL 없음)
- **목적**: UI 확인, 구조 검증, 개발 환경 빠른 설정
- **상황**: MySQL 모듈 미설치 또는 데이터베이스 미설정
- **결과**: 모든 페이지가 빈 데이터로 정상 렌더링

### 2. 프로덕션 모드 (MySQL 있음)
- **목적**: 실제 데이터를 사용한 완전한 기능 테스트
- **상황**: MySQL 설치, 데이터베이스 설정, 테이블 생성 완료
- **결과**: 실제 CRUD 기능까지 모든 기능 동작

## 데모 모드 테스트

### 환경 설정

```bash
# 1. 가상환경 생성 및 활성화
python3 -m venv pycrm
source pycrm/bin/activate  # Linux/Mac
pycrm\Scripts\activate     # Windows

# 2. 기본 의존성만 설치 (MySQL 제외)
pip install Flask==2.3.3 Jinja2==3.1.2 python-dotenv==1.0.0 Werkzeug==2.3.7

# 3. 애플리케이션 실행
python main.py
```

### 예상 로그 출력

```
[WARNING] MySQL 모듈이 설치되지 않았습니다. 데모 모드로 실행됩니다.
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 데모 모드 테스트 체크리스트

#### 기본 페이지 접근성 테스트
- [ ] 홈페이지 (`http://localhost:5000/`)
  - 대시보드 로드 확인
  - 통계 카드가 모두 0으로 표시
  - "이번달 생일 고객이 없습니다" 메시지 표시
  - "최근 방문 기록이 없습니다" 메시지 표시

#### 내비게이션 테스트
- [ ] 고객 관리 링크 클릭
- [ ] 방문 기록 링크 클릭  
- [ ] 결제 관리 링크 클릭
- [ ] 통계 링크 클릭

#### 개별 페이지 테스트

**고객 관리 (`/customers`)**:
- [ ] 페이지 정상 로드
- [ ] "등록된 고객이 없습니다" 메시지 표시
- [ ] "고객 등록" 버튼 존재
- [ ] 검색 폼 정상 동작 (빈 결과 반환)

**고객 등록 (`/customer/new`)**:
- [ ] 폼 페이지 정상 로드
- [ ] 모든 입력 필드 표시
- [ ] "등록" 버튼 존재
- [ ] "목록으로" 버튼 동작

**방문 기록 (`/visits`)**:
- [ ] 페이지 정상 로드
- [ ] "방문 기록이 없습니다" 메시지 표시
- [ ] 기간별 필터 폼 존재
- [ ] "방문 등록" 버튼 존재

**방문 등록 (`/visits/new`)**:
- [ ] 폼 페이지 정상 로드
- [ ] 고객 선택 드롭다운 (빈 상태)
- [ ] 날짜 입력 필드 (오늘 날짜 기본값)

**결제 내역 (`/payments`)**:
- [ ] 페이지 정상 로드
- [ ] "결제 내역이 없습니다" 메시지 표시
- [ ] "결제 등록" 버튼 존재

**결제 등록 (`/payments/new`)**:
- [ ] 폼 페이지 정상 로드
- [ ] 방문 선택 드롭다운 (빈 상태)
- [ ] 결제 수단 드롭다운 (빈 상태)

**통계 대시보드 (`/stats`)**:
- [ ] 페이지 정상 로드
- [ ] 모든 통계가 0으로 표시
- [ ] 월별 통계 차트 영역 존재

**고객별 통계 (`/stats/customers`)**:
- [ ] 페이지 정상 로드
- [ ] "고객 통계 데이터가 없습니다" 메시지 표시

### 자동화된 데모 모드 테스트

```python
# demo_test.py
import sys
sys.path.append('.')

def test_demo_mode():
    from main import app
    
    test_urls = [
        '/',
        '/customers',
        '/customer/new', 
        '/visits',
        '/visits/new',
        '/payments',
        '/payments/new',
        '/stats',
        '/stats/customers'
    ]
    
    with app.test_client() as client:
        for url in test_urls:
            response = client.get(url)
            assert response.status_code == 200, f"Failed: {url}"
            print(f"✅ {url}: OK")
    
    print("🎉 모든 데모 모드 테스트 통과!")

if __name__ == "__main__":
    test_demo_mode()
```

실행:
```bash
python demo_test.py
```

## 프로덕션 모드 테스트

### 환경 설정

```bash
# 1. 가상환경에서 MySQL 의존성 설치
pip install -r requirements.txt

# 2. .env 파일 생성
cat > .env << EOF
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=crm_db
EOF

# 3. 데이터베이스 초기화
mysql -u root -p crm_db < scripts/sql/crm_ddl.sql
mysql -u root -p crm_db < scripts/sql/init_payment_method.sql

# 4. 애플리케이션 실행
python main.py
```

### 예상 로그 출력

```
데이터베이스 연결 성공
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 프로덕션 모드 테스트 체크리스트

#### CRUD 기능 테스트

**고객 관리**:
- [ ] 고객 등록 기능
  - 필수 필드 검증
  - 성공 시 목록 페이지로 리다이렉트
  - 플래시 메시지 표시
- [ ] 고객 목록 조회
  - 등록된 고객 표시
  - 검색 기능 동작
  - 생일월 필터 동작
- [ ] 고객 상세 보기
  - 고객 정보 표시
  - 방문 기록 표시
  - 결제 내역 표시
- [ ] 고객 정보 수정
  - 기존 정보 로드
  - 수정 후 상세 페이지로 리다이렉트
- [ ] 고객 삭제
  - 삭제 확인 팝업
  - 관련 데이터 정리

**방문 기록 관리**:
- [ ] 방문 등록
  - 고객 선택 드롭다운에 실제 고객 표시
  - 날짜 및 메모 입력
- [ ] 방문 목록 조회
  - 등록된 방문 기록 표시
  - 기간별 필터링 동작
- [ ] 방문 기록 수정
  - 메모 수정 기능
- [ ] 방문 기록 삭제
  - 관련 결제 내역 처리

**결제 관리**:
- [ ] 결제 등록
  - 방문 선택 드롭다운에 실제 방문 표시
  - 결제 수단 선택
  - 금액 입력
- [ ] 결제 목록 조회
  - 등록된 결제 표시
  - 고객별 필터링
- [ ] 결제 삭제
  - 삭제 확인 및 처리

#### 통계 기능 테스트
- [ ] 전체 통계 계산
  - 총 고객수
  - 총 방문수  
  - 총 매출
  - 평균 결제금액
- [ ] 월별 통계
  - 해당 월 데이터 집계
  - 차트 데이터 정확성
- [ ] 고객별 통계
  - 개별 고객 통계 계산
  - 정렬 및 표시

### 통합 테스트 시나리오

#### 시나리오 1: 신규 고객 전체 플로우
1. 고객 등록 → 고객 A 생성
2. 방문 등록 → 고객 A의 방문 기록 생성
3. 결제 등록 → 해당 방문의 결제 기록 생성
4. 통계 확인 → 모든 수치가 올바르게 반영

#### 시나리오 2: 데이터 수정 플로우
1. 기존 고객 정보 수정
2. 방문 메모 수정
3. 결제 금액 확인 (수정 기능이 있다면)
4. 통계 업데이트 확인

#### 시나리오 3: 삭제 플로우
1. 결제 기록 삭제
2. 방문 기록 삭제
3. 고객 삭제
4. 통계가 올바르게 업데이트되는지 확인

## 에러 처리 테스트

### 데이터베이스 연결 중단 테스트

```bash
# MySQL 서버 중지 후 애플리케이션 동작 확인
sudo systemctl stop mysql  # Linux
brew services stop mysql   # Mac

# 애플리케이션 실행 후 페이지 접근
python main.py
```

예상 동작:
- 연결 실패 메시지 표시
- 모든 페이지가 데모 모드처럼 동작
- TypeError 발생하지 않음

### 잘못된 설정 테스트

**.env 파일에 잘못된 정보 설정**:
```
DB_HOST=nonexistent_host
DB_USER=wrong_user
DB_PASSWORD=wrong_password
```

예상 동작:
- 연결 실패 로그 출력
- 애플리케이션은 정상 실행
- 데모 모드로 동작

## 성능 테스트

### 응답 시간 측정

```python
# performance_test.py
import time
import sys
sys.path.append('.')

def measure_response_time():
    from main import app
    
    test_urls = ['/', '/customers', '/visits', '/payments', '/stats']
    
    with app.test_client() as client:
        for url in test_urls:
            start_time = time.time()
            response = client.get(url)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # ms
            print(f"{url}: {response_time:.2f}ms")

if __name__ == "__main__":
    measure_response_time()
```

### 메모리 사용량 모니터링

```python
# memory_test.py
import psutil
import os
import sys
sys.path.append('.')

def monitor_memory():
    process = psutil.Process(os.getpid())
    
    print("메모리 사용량 모니터링 시작")
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"초기 메모리: {initial_memory:.2f} MB")
    
    # 애플리케이션 로드
    from main import app
    
    load_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"앱 로드 후: {load_memory:.2f} MB")
    
    # 여러 페이지 요청
    with app.test_client() as client:
        for i in range(100):
            client.get('/')
            client.get('/customers')
            client.get('/visits')
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"100회 요청 후: {final_memory:.2f} MB")

if __name__ == "__main__":
    monitor_memory()
```

## 브라우저 테스트

### 수동 테스트 체크리스트

#### UI/UX 테스트
- [ ] 모든 버튼이 올바르게 동작
- [ ] 링크가 정확한 페이지로 이동
- [ ] 폼 제출이 예상대로 동작
- [ ] 플래시 메시지가 적절히 표시
- [ ] 반응형 디자인 동작 (모바일, 태블릿)

#### 브라우저 호환성
- [ ] Chrome 최신 버전
- [ ] Firefox 최신 버전
- [ ] Safari (Mac)
- [ ] Edge (Windows)

#### JavaScript 기능
- [ ] 삭제 확인 팝업
- [ ] 폼 유효성 검사
- [ ] 날짜 선택기
- [ ] 동적 UI 요소

## 자동화된 테스트 스크립트

### 통합 테스트 스크립트

```bash
#!/bin/bash
# test_all.sh

echo "🚀 CRM 시스템 전체 테스트 시작"

# 1. 데모 모드 테스트
echo "📝 데모 모드 테스트..."
python demo_test.py

# 2. 성능 테스트
echo "⚡ 성능 테스트..."
python performance_test.py

# 3. 메모리 테스트
echo "💾 메모리 테스트..."
python memory_test.py

# 4. URL 검증
echo "🔗 URL 검증..."
python -c "
import sys
sys.path.append('.')
from main import app

print('Available routes:')
for rule in app.url_map.iter_rules():
    print(f'  {rule.endpoint}: {rule.rule}')
"

echo "✅ 모든 테스트 완료!"
```

실행:
```bash
chmod +x test_all.sh
./test_all.sh
```

## 테스트 문서화

### 테스트 결과 기록

```markdown
# 테스트 실행 결과

## 환경 정보
- OS: Ubuntu 20.04
- Python: 3.8.10
- 테스트 일시: 2024-01-15 14:30:00

## 데모 모드 테스트
✅ 모든 페이지 200 응답
✅ 에러 메시지 없음
✅ UI 정상 렌더링

## 성능 테스트
- 홈페이지: 15.23ms
- 고객 목록: 12.45ms
- 통계 페이지: 18.67ms

## 메모리 사용량
- 초기: 25.4 MB
- 앱 로드 후: 28.7 MB
- 100회 요청 후: 29.1 MB

## 발견된 이슈
없음

## 권장사항
- 모든 테스트 통과
- 프로덕션 배포 가능
```

## 결론

이 테스트 가이드를 통해:

1. **개발 환경**: 데모 모드로 빠른 개발과 UI 확인
2. **품질 보증**: 자동화된 테스트로 안정성 확보
3. **성능 검증**: 응답 시간과 메모리 사용량 모니터링
4. **사용자 경험**: 브라우저 테스트로 실제 사용성 확인

리팩토링된 시스템이 모든 상황에서 안정적으로 동작함을 검증할 수 있으며, 지속적인 개발과 유지보수를 위한 테스트 기반을 구축했습니다.