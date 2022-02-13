from datetime import datetime, timedelta
from advertisement_factory import CategoryFactory, AdvertisementFactory
from models import Category, Advertisement


def create_categories(NUM_CATEGORIES: int = 100):
    from advertisement_factory import session

    cnt = session.query(Category).count()
    if cnt < NUM_CATEGORIES:
        print(f"Categories before: {cnt}. Creating {NUM_CATEGORIES}.")

        categories = CategoryFactory.create_batch(NUM_CATEGORIES)
        session.commit()
        print(categories)


def create_advertisements(
    NUM_ADVERTISEMENTS: int = 4000,
    available_users: int = 500,
    available_categories: int = 100,
):
    from advertisement_factory import session

    cnt = session.query(Advertisement).count()
    if cnt < NUM_ADVERTISEMENTS:
        print(f"Advertisements before: {cnt}. Creating {NUM_ADVERTISEMENTS}.")

        dt = datetime.now()

        AdvertisementFactory.create_batch(
            NUM_ADVERTISEMENTS,
            available_user_ids=list(range(1, available_users)),
            available_category_ids=list(range(1, available_categories)),
            date_min=dt - timedelta(days=5),
            date_max=dt + timedelta(days=10),
        )
        session.commit()
