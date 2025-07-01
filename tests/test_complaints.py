import pytest
from sqlalchemy import select


@pytest.mark.anyio
async def test_get_complaints_page(async_client, db_session):
    response = await async_client.get("/complaints")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_complaint(async_client, db_session):
    form_data = {
        "name_surname": "John Doe",
        "email": "",
        "message": "how are u bro how are u bro"
    }

    response = await async_client.post("/complaints", data=form_data)
    assert response.status_code == 303
    assert response.headers["location"] == "/complaints"

    from app.complaints.models import Complaint  # noqa: E402
    complaint = await db_session.execute(select(Complaint).where(Complaint.email == ""))
    complaint = complaint.scalar_one_or_none()

    assert complaint is not None
    assert complaint.name_surname == "John Doe"
    assert complaint.message == "how are u bro how are u bro"


@pytest.mark.anyio
async def test_delete_complaint_by_id(async_client, db_session):
    from app.complaints.models import Complaint  # noqa: E402
    complaint = Complaint(
        name_surname="Jane Doe",
        email="test@gmail.com",
        message="Test delete complaint"
    )
    db_session.add(complaint)
    await db_session.commit()
    await db_session.refresh(complaint)

    response = await async_client.post(f"/complaints/{complaint.id}/delete")
    assert response.status_code == 303
    assert response.headers["location"] == "/complaints"

    deleted_complaint = await db_session.get(Complaint, complaint.id)
    assert deleted_complaint is None
