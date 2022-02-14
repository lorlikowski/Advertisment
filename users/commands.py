from user_factory import UserFactory, User
from sqlalchemy.exc import IntegrityError

def create_users(
    NUM_USERS=500
):
    from user_factory import session

    cnt = session.query(User).count()
    print(f"Users before: {cnt}. Creating up to {NUM_USERS}.")

    while cnt < NUM_USERS:
        try:
            UserFactory.create()
            cnt += 1
            if (cnt % 10 == 0):
                print(f"Added {cnt}th user")
        except IntegrityError:
            print("Skipping error")

    session.commit()
    print(f"Users after: {session.query(User).count()}")
