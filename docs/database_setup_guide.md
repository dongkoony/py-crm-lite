# 데이터베이스 설정 가이드

## 개요

이 문서는 Flask CRM 시스템에 MySQL 데이터베이스를 연결하는 방법을 단계별로 설명합니다. 초보자도 쉽게 따라할 수 있도록 상세한 설명과 함께 제공됩니다.

## 지원 환경

- **Linux (Ubuntu/Debian)**: 완벽 지원
- **Windows (WSL)**: WSL2 환경에서 완벽 지원
- **macOS**: 기본 지원 (Homebrew 사용)
- **Windows (네이티브)**: MySQL for Windows 사용

## 1단계: MySQL 설치

### Ubuntu/WSL 환경

```bash
# 패키지 목록 업데이트
sudo apt update

# MySQL 서버 설치
sudo apt install mysql-server -y

# 설치 확인
mysql --version
```

### macOS 환경

```bash
# Homebrew로 MySQL 설치
brew install mysql

# MySQL 서비스 시작
brew services start mysql
```

### Windows 환경

1. [MySQL 공식 사이트](https://dev.mysql.com/downloads/installer/)에서 MySQL Installer 다운로드
2. 설치 프로그램 실행 후 "Server only" 선택
3. 기본 설정으로 설치 진행

## 2단계: MySQL 서비스 시작

### Ubuntu/WSL

```bash
# 서비스 시작 (systemd가 있는 경우)
sudo systemctl start mysql
sudo systemctl enable mysql

# WSL 환경에서 systemd가 없는 경우
sudo service mysql start

# 서비스 상태 확인
sudo service mysql status
```

정상적으로 실행되면 다음과 같은 메시지가 출력됩니다:
```
Server version          8.0.42-0ubuntu0.22.04.2
Protocol version        10
Connection              Localhost via UNIX socket
UNIX socket             /var/run/mysqld/mysqld.sock
Uptime:                 5 min 0 sec
```

### macOS

```bash
# 서비스 확인
brew services list | grep mysql

# 서비스가 실행 중이지 않다면 시작
brew services start mysql
```

## 3단계: MySQL 접속 및 초기 설정

### Root 계정으로 접속

```bash
# Ubuntu/WSL에서 sudo 권한으로 접속
sudo mysql

# 또는 직접 접속 시도
mysql -u root -p
```

접속되면 다음과 같은 프롬프트가 나타납니다:
```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 22
Server version: 8.0.42-0ubuntu0.22.04.2 (Ubuntu)

mysql>
```

### 보안 설정 (선택사항)

보다 안전한 설정을 원한다면 다음 명령어 실행:

```bash
sudo mysql_secure_installation
```

설정 옵션:
- **VALIDATE PASSWORD PLUGIN**: `N` (개발환경이므로 비활성화)
- **root 비밀번호 설정**: 원하는 비밀번호 입력 (예: `1234`)
- **익명 사용자 제거**: `Y`
- **원격 root 로그인 금지**: `Y` 
- **test 데이터베이스 제거**: `Y`
- **권한 테이블 다시 로드**: `Y`

## 4단계: CRM 데이터베이스 생성

MySQL에 접속한 상태에서 다음 SQL 명령어들을 순서대로 실행:

```sql
-- CRM 전용 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS crm_db
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- CRM 전용 사용자 계정 생성
CREATE USER IF NOT EXISTS 'crm_user'@'localhost' 
IDENTIFIED BY '1234';

-- CRM 데이터베이스에 대한 모든 권한 부여
GRANT ALL PRIVILEGES ON crm_db.* TO 'crm_user'@'localhost';

-- 권한 변경사항 적용
FLUSH PRIVILEGES;

-- 생성 확인
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'crm_user';

-- MySQL 종료
EXIT;
```

성공하면 다음과 같은 출력을 확인할 수 있습니다:
```
+--------------------+
| Database           |
+--------------------+
| crm_db             |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

## 5단계: 애플리케이션 환경 설정

### .env 파일 생성

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력:

```bash
# 프로젝트 루트에서 실행
cat > .env << EOF
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=crm_user
DB_PASSWORD=1234
DB_NAME=crm_db
EOF
```

### 설정 파일 확인

`.env` 파일이 올바르게 생성되었는지 확인:

```bash
cat .env
```

출력 결과:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=crm_user
DB_PASSWORD=1234
DB_NAME=crm_db
```

## 6단계: 데이터베이스 연결 테스트

### 명령줄에서 연결 테스트

```bash
# CRM 사용자로 데이터베이스 연결 테스트
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db -e "SELECT 'Connection successful!' as status;"
```

성공하면 다음과 같은 출력이 나타납니다:
```
mysql: [Warning] Using a password on the command line interface can be insecure.
+---------------------+
| status              |
+---------------------+
| Connection successful! |
+---------------------+
```

**참고**: `[Warning] Using a password on the command line interface can be insecure.` 메시지는 보안 경고이며 정상 동작입니다.

## 7단계: 데이터베이스 테이블 생성

### SQL 스크립트로 테이블 생성

```bash
# 테이블 구조 생성
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db < scripts/sql/crm_ddl.sql

# 결제 수단 초기 데이터 입력
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db < scripts/sql/init_payment_method.sql
```

### 테이블 생성 확인

```bash
# 생성된 테이블 목록 확인
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db -e "SHOW TABLES;"
```

정상적으로 생성되면 다음과 같은 테이블 목록이 출력됩니다:
```
+------------------+
| Tables_in_crm_db |
+------------------+
| customer         |
| payment          |
| payment_method   |
| visit            |
+------------------+
```

### 초기 데이터 확인

```bash
# 결제 수단 초기 데이터 확인
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db -e "SELECT * FROM payment_method;"
```

출력 결과:
```
+-------------+-------------+
| method_code | method_name |
+-------------+-------------+
| CASH        | 현금        |
| CARD        | 카드        |
| POINT       | 포인트      |
| TRANSFER    | 계좌이체    |
+-------------+-------------+
```

## 8단계: 애플리케이션 실행 및 연결 확인

### Python 의존성 설치

```bash
# 가상환경 활성화 (이미 생성한 경우)
source pycrm/bin/activate  # Linux/Mac
pycrm\Scripts\activate     # Windows

# MySQL 커넥터 설치 확인
pip install mysql-connector-python
```

### 애플리케이션 실행

```bash
python main.py
```

**성공적인 연결 시 출력:**
```
데이터베이스 연결 성공
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**실패 시 출력:**
```
[ERROR] DB 연결 실패: 2003 (HY000): Can't connect to MySQL server on '127.0.0.1:3306' (111)
[ERROR] DB 연결 객체 없음.
```

## 문제 해결

### 일반적인 문제들

#### 1. MySQL 서비스가 실행되지 않음

**증상**: `Can't connect to MySQL server`

**해결방법**:
```bash
# 서비스 상태 확인
sudo service mysql status

# 서비스 시작
sudo service mysql start

# 포트 확인
sudo netstat -tlnp | grep 3306
```

#### 2. 권한 거부 오류

**증상**: `Access denied for user 'crm_user'@'localhost'`

**해결방법**:
```bash
# Root로 MySQL 접속
sudo mysql

# 사용자 다시 생성
DROP USER IF EXISTS 'crm_user'@'localhost';
CREATE USER 'crm_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON crm_db.* TO 'crm_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3. 소켓 연결 오류 (WSL 환경)

**증상**: `Can't connect to local MySQL server through socket`

**해결방법**:
- `.env` 파일에서 `DB_HOST=localhost`를 `DB_HOST=127.0.0.1`로 변경
- TCP 연결 강제 사용

#### 4. 테이블이 존재하지 않음

**증상**: `Table 'crm_db.customer' doesn't exist`

**해결방법**:
```bash
# 테이블 생성 스크립트 재실행
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db < scripts/sql/crm_ddl.sql
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db < scripts/sql/init_payment_method.sql

# 테이블 존재 확인
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db -e "SHOW TABLES;"
```

### 고급 문제 해결

#### MySQL 에러 로그 확인

```bash
# 에러 로그 실시간 확인
sudo tail -f /var/log/mysql/error.log

# 최근 에러 확인
sudo tail -20 /var/log/mysql/error.log
```

#### 연결 프로세스 확인

```bash
# MySQL 프로세스 확인
ps aux | grep mysql

# 포트 사용 확인
sudo netstat -tlnp | grep 3306

# MySQL 변수 확인
mysql -u root -p -e "SHOW VARIABLES LIKE 'port';"
mysql -u root -p -e "SHOW VARIABLES LIKE 'socket';"
```

## 자동화 스크립트

전체 설정 과정을 자동화하는 스크립트:

```bash
#!/bin/bash
# setup_database.sh

echo "🚀 CRM 데이터베이스 설정 시작"

# MySQL 서비스 시작
echo "📊 MySQL 서비스 시작..."
sudo service mysql start

# 데이터베이스 및 사용자 생성
echo "🗄️ 데이터베이스 및 사용자 생성..."
sudo mysql << EOF
CREATE DATABASE IF NOT EXISTS crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'crm_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON crm_db.* TO 'crm_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# .env 파일 생성
echo "⚙️ 환경 설정 파일 생성..."
cat > .env << EOF
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=crm_user
DB_PASSWORD=1234
DB_NAME=crm_db
EOF

# 테이블 생성
echo "📋 테이블 생성..."
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db < scripts/sql/crm_ddl.sql
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db < scripts/sql/init_payment_method.sql

# 연결 테스트
echo "🔍 연결 테스트..."
mysql -u crm_user -p1234 -h 127.0.0.1 crm_db -e "SELECT 'Database setup completed!' as status;"

echo "✅ 데이터베이스 설정 완료!"
echo "애플리케이션을 실행하려면: python main.py"
```

사용 방법:
```bash
chmod +x setup_database.sh
./setup_database.sh
```

## 보안 권장사항

### 프로덕션 환경 설정

1. **강력한 비밀번호 사용**:
```sql
ALTER USER 'crm_user'@'localhost' IDENTIFIED BY 'your_strong_password_here';
```

2. **네트워크 액세스 제한**:
```bash
# /etc/mysql/mysql.conf.d/mysqld.cnf
bind-address = 127.0.0.1
```

3. **불필요한 권한 제거**:
```sql
# 최소 권한 부여
GRANT SELECT, INSERT, UPDATE, DELETE ON crm_db.* TO 'crm_user'@'localhost';
```

4. **정기적인 백업**:
```bash
# 자동 백업 스크립트
mysqldump -u crm_user -p1234 crm_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

## 마무리

이 가이드를 따라하면 Flask CRM 시스템에 MySQL 데이터베이스를 성공적으로 연결할 수 있습니다. 

**완료 후 확인사항:**
- [ ] MySQL 서비스 정상 실행
- [ ] crm_db 데이터베이스 생성 완료
- [ ] crm_user 계정 생성 및 권한 부여 완료
- [ ] .env 파일 정상 생성
- [ ] 모든 테이블 생성 완료
- [ ] 애플리케이션에서 "데이터베이스 연결 성공" 메시지 확인

문제가 발생하면 문제 해결 섹션을 참조하거나, 에러 로그를 확인하여 구체적인 원인을 파악하시기 바랍니다.