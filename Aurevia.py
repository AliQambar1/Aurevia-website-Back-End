# seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.user import UserModel
from models.listing import ListingModel  # تأكد من وجود الملف
from config.environment import db_URI

engine = create_engine(db_URI)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("Recreating database...")
# حذف الجداول القديمة وإنشاء الجديدة (بما فيها listings)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Seeding data...")


admin_user = UserModel(username="admin", email="admin@aurevia.com", role="admin")
admin_user.set_password("admin123")


normal_user = UserModel(username="aliqa", email="ali@aurevia.com", role="user")
normal_user.set_password("user123")

db.add(admin_user)
db.add(normal_user)
db.commit()

print("Database seeded! Admin: admin/admin123")