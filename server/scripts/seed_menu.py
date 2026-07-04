from database import SessionLocal
from models.menu_item import MenuItem
from repositories.interfaces.menu_repository import MenuRepository
from repositories.sqlalchemy.menu_repository import SqlAlchemyMenuRepository


def seed_menu_items(menu_repository: MenuRepository):

    if menu_repository.get_all():
        print("Menu already seeded.")
        return

    menu_items = [
        MenuItem(
            name="Margherita Pizza",
            price=299,
            is_available=True,
        ),
        MenuItem(
            name="Veg Burger",
            price=199,
            is_available=True,
        ),
        MenuItem(
            name="Coke",
            price=60,
            is_available=True,
        ),
    ]

    for menu_item in menu_items:
        menu_repository.create(menu_item)


def main():

    session = SessionLocal()

    try:
        menu_repository = SqlAlchemyMenuRepository(session)
        seed_menu_items(menu_repository)
        session.commit()
        print("Menu seeded successfully.")

    finally:
        session.close()


if __name__ == "__main__":
    main()
