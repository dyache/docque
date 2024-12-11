import psycopg2
from src.config import Config

settings = Config()

conn = psycopg2.connect(dbname=settings.db_name, user=settings.db_user, password=settings.db_password,
                        host=settings.db_host, port=settings.db_port)

cur = conn.cursor()
create_student_table = """
CREATE TABLE IF NOT EXISTS Student (
    student_id VARCHAR(255) PRIMARY KEY,  
    notify BOOLEAN NOT NULL               
);
"""

create_staff_table = """
CREATE TABLE IF NOT EXISTS Staff (
    staff_id UUID PRIMARY KEY,             
    staff_name VARCHAR(255) NOT NULL,            
    hashed_password TEXT NOT NULL,         
    current_queue_number INT
);
"""

create_queue_table = """
CREATE TABLE IF NOT EXISTS Queue (
    queue_id UUID PRIMARY KEY,            
    position SERIAL NOT NULL,                
    student_id VARCHAR(255) REFERENCES student (student_id),
    created_at TIMESTAMP NOT NULL,        
    status VARCHAR(255) NOT NULL
);
"""

create_queue_history_table = """
CREATE TABLE IF NOT EXISTS QueueHistory (
    queue_id UUID PRIMARY KEY,              
    position INT NULL,                
    student_id VARCHAR(255) REFERENCES student (student_id),
    created_at TIMESTAMP NOT NULL,        
    status VARCHAR(255) NOT NULL          
);
"""

create_settings_table = """
CREATE TABLE IF NOT EXISTS Setting (
    setting_id UUID PRIMARY KEY,
    queue_reset_enabled NOT NULL DEFAULT FALSE,
    queue_reset_day VARCHAR(50) NOT NULL DEFAULT 'Everyday'
    queue_reset_at TIME NOT NULL 
)
"""

cur.execute(create_student_table)
cur.execute(create_staff_table)
cur.execute(create_queue_table)
cur.execute(create_queue_history_table)
try:
    conn.commit()
    print("Таблицы успешно созданы.")
except Exception as e:
    print(f"Ошибка: {e}")
