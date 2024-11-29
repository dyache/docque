import psycopg2
from passlib.context import CryptContext

from src.config import Config
from src.staff.repository import StaffRepository
from src.staff.routes import StaffRoutes
from src.staff.service import StaffService
from src.glob import app

# TODO: protect all other routes with auth

settings = Config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = psycopg2.connect(dbname=settings.db_name, user=settings.db_user, password=settings.db_password,
                        host=settings.db_host, port=settings.db_port)

cur = conn.cursor()

# TODO: init all routes
staff_repository = StaffRepository(conn, cur)
staff_serv = StaffService(staff_repository, pwd_context, settings)
staff_routes = StaffRoutes(staff_serv)

cur.close()
conn.close()
