from database import Base, engine

# Import every model
from models.menu_item import MenuItem

Base.metadata.create_all(engine)

print("Tables created successfully!")