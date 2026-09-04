from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.models.document import Contributor, Contribution
from app.schemas.search import ContributorCreate, ContributionCreate, ContributionResponse

router = APIRouter()


@router.post("", response_model=ContributionResponse)
async def create_contribution(
    contribution: ContributionCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(
        __import__("sqlalchemy").select(Contributor).where(
            Contributor.email == contribution.contributor.email
        )
    )
    contributor = existing.scalar_one_or_none()

    if not contributor:
        contributor = Contributor(
            name=contribution.contributor.name,
            email=contribution.contributor.email,
            phone=contribution.contributor.phone,
            organization=contribution.contributor.organization,
        )
        db.add(contributor)
        await db.flush()

    new_contribution = Contribution(
        contributor_id=contributor.id,
        document_type=contribution.document_type,
        title=contribution.title,
        content=contribution.content,
    )
    db.add(new_contribution)
    await db.commit()
    await db.refresh(new_contribution)

    return new_contribution


@router.get("/status/{contribution_id}")
async def get_contribution_status(
    contribution_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        __import__("sqlalchemy").select(Contribution).where(
            Contribution.id == contribution_id
        )
    )
    contribution = result.scalar_one_or_none()

    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")

    return {
        "id": str(contribution.id),
        "status": contribution.status,
        "created_at": contribution.created_at.isoformat(),
    }
