from app.database import SessionLocal, Base, engine
from app.models import Admin
from app.auth import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# List of admins to add/update
admins = [
    {"username": "admin", "password": "password123"},      # default admin
    {"username": "admin2", "password": "mypassword456"}    # example additional admin
]

db = SessionLocal()

for a in admins:
    existing_admin = db.query(Admin).filter(Admin.username == a["username"]).first()
    if existing_admin:
        # Update password if admin already exists
        existing_admin.hashed_password = get_password_hash(a["password"])
        print(f"Updated password for admin '{a['username']}'")
    else:
        # Create new admin
        new_admin = Admin(username=a["username"], hashed_password=get_password_hash(a["password"]))
        db.add(new_admin)
        print(f"Created new admin '{a['username']}'")

db.commit()
db.close()
print("Admin seeding completed!")

