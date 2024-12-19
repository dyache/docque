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
    staff_name VARCHAR(255) NOT NULL UNIQUE,            
    hashed_password TEXT NOT NULL,         
    current_queue_number INT DEFAULT -1
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
CREATE TABLE IF NOT EXISTS Queue_History (
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
    queue_reset_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    queue_reset_day VARCHAR(50) NOT NULL DEFAULT 'Everyday',
    queue_reset_at TIME NOT NULL 
)
"""

cur.execute(create_student_table)
cur.execute(create_staff_table)
cur.execute(create_queue_table)
cur.execute(create_queue_history_table)
cur.execute(create_settings_table)

create_position_index = """
CREATE INDEX IF NOT EXISTS idx_queue_position ON Queue (position);
"""
cur.execute(create_position_index)

create_trigger_function = """
CREATE OR REPLACE FUNCTION log_queue_updates()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO Queue_History (queue_id, position, student_id, created_at, status)
        VALUES (NEW.queue_id, NEW.position, NEW.student_id, NEW.created_at, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
cur.execute(create_trigger_function)

# create_trigger = """
# CREATE OR REPLACE TRIGGER after_queue_update
# AFTER UPDATE ON Queue
# FOR EACH ROW
# EXECUTE FUNCTION log_queue_updates();
# """
# cur.execute(create_trigger)

create_view_inner_join = """
CREATE OR REPLACE VIEW staff_with_queue AS
SELECT s.staff_id, s.staff_name, q.queue_id, q.position, q.status
FROM Staff s
INNER JOIN Queue q ON s.current_queue_number = q.position;
"""
cur.execute(create_view_inner_join)

create_view_left_join = """
CREATE OR REPLACE VIEW queue_with_staff_info AS
SELECT q.queue_id, q.position, q.status, s.staff_name, s.staff_id
FROM Queue q
LEFT JOIN Staff s ON q.position = s.current_queue_number;
"""
cur.execute(create_view_left_join)

try:
    conn.commit()
    print("Таблицы успешно созданы.")
except Exception as e:
    print(f"Ошибка: {e}")
