-- 고객 테이블
CREATE TABLE customer (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  phone VARCHAR(20),
  birth_date DATE,
  gender CHAR(1),
  memo TEXT
);

-- 방문 테이블
CREATE TABLE visit (
  visit_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  visit_date DATETIME NOT NULL,
  memo TEXT,
  CONSTRAINT fk_visit_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE CASCADE
);

-- 결제 수단 코드 테이블
CREATE TABLE payment_method (
  method_code VARCHAR(20) PRIMARY KEY,
  method_name VARCHAR(20) NOT NULL
);

-- 결제 테이블  
CREATE TABLE payment (
  payment_id INT PRIMARY KEY AUTO_INCREMENT,
  visit_id INT NOT NULL,
  amount INT NOT NULL CHECK (amount >= 0),
  payment_method_code VARCHAR(20) NOT NULL,
  payment_datetime DATETIME NOT NULL,
  CONSTRAINT fk_payment_visit FOREIGN KEY (visit_id) REFERENCES visit (visit_id) ON DELETE CASCADE,
  CONSTRAINT fk_payment_payment_method FOREIGN KEY (payment_method_code) REFERENCES payment_method (method_code) ON DELETE CASCADE
);
