import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:

    # 데이터베이스 설정
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
    DB_NAME = os.getenv("DB_NAME", "crm_db")

    @classmethod
    def get_db_config(cls):
        # 데이터베이스 연결 설정 반환
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_NAME,
            "autocommit": True  # 자동 커밋 활성화
        }