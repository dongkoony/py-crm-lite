-- 결제 수단 등록 쿼리
INSERT INTO payment_method (method_code, method_name)
VALUES ('CASH', '현금'),
       ('CARD', '카드'),
       ('POINT', '포인트'),
       ('TRANSFER', '계좌이체');