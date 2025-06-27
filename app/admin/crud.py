from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.admin.models import AdminUser
from app.admin.schemas import AdminUserCreate
from app.auth.security import hash_password


async def create_admin_user(session: AsyncSession, admin_data: AdminUserCreate) -> AdminUser:
    hashed_pw = hash_password(admin_data.password)
    admin_user = AdminUser(
        email=admin_data.email,
        hashed_password=hashed_pw
    )
    session.add(admin_user)
    await session.commit()
    await session.refresh(admin_user)
    return admin_user


async def get_admin_user_by_id(admin_id: int, session: AsyncSession) -> AdminUser | None:
    result = await session.execute(select(AdminUser).where(AdminUser.id == admin_id))
    admin_user = result.scalars().first()
    return admin_user
