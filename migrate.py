#script needs to be run in terminal to drop all tables and run them again

from model import db, connect_to_db

if __name__ == "__main__":
	from app import app
	connect_to_db(app)

	db.drop_all()
	db.create_all()
