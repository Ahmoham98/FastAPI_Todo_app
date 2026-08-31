import random
from fastapi import Depends
from core.database import get_db
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import UserModel, UserRole
from tasks.models import TaskModel

fake = Faker()

async def seed_data(
    db: AsyncSession, 
    user_count: int = 5, 
    tasks_per_user: int = 3
):
    """Generate random tasks and users using Faker

    Args:
        user_count (int, optional): number of users you want to be added to database. Defaults to 5.
        task_per_user (int, optional): nubmer of tasks you want to be added per user in database. Defaults to 3.
    """

    created_users = []

    # 1.Creates new user
    for _ in range(user_count):
        user_obj = UserModel(
            email=fake.unique.email(), 
            role = random.choice([UserRole.USER, UserRole.ADMIN]), 
            is_active=True
        )
        user_obj.hash_password("123456789")

        db.add(user_obj)
        await db.flush()

        created_users.append(user_obj)

        # 2.For every user creates tasks
        for _ in range(tasks_per_user):
            db_task = TaskModel(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=100),
                is_done=random.choice([True, False]),
                user_id=user_obj.id
            )
            db.add(db_task)

    await db.commit()

    for user in created_users:
        await db.refresh(user)

    return {
        "message": f"Successfully seeded {user_count} users and {user_count * tasks_per_user} tasks.",
        "sample_password": "123456789",
        "sample_emails": [u.email for u in created_users],
    }
