from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID

from app.database import get_db
from app.models.document import Document, Contribution, SearchLog, DailyScan
from app.schemas.search import StatsResponse

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    total_docs = await db.execute(select(func.count(Document.id)))
    pending_contributions = await db.execute(
        select(func.count(Contribution.id)).where(Contribution.status == "pending")
    )
    total_searches = await db.execute(select(func.count(SearchLog.id)))
    recent_scans = await db.execute(
        select(DailyScan).order_by(DailyScan.created_at.desc()).limit(5)
    )

    return {
        "total_documents": total_docs.scalar() or 0,
        "pending_contributions": pending_contributions.scalar() or 0,
        "total_searches": total_searches.scalar() or 0,
        "recent_scans": [
            {
                "id": str(scan.id),
                "date": scan.scan_date.isoformat(),
                "new_found": scan.new_documents_found,
            }
            for scan in recent_scans.scalars().all()
        ],
    }


@router.get("/contributions")
async def list_contributions(
    status: str = "pending",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contribution).where(Contribution.status == status)
    )
    return [
        {
            "id": str(c.id),
            "title": c.title,
            "status": c.status,
            "created_at": c.created_at.isoformat(),
        }
        for c in result.scalars().all()
    ]


@router.put("/contributions/{contribution_id}")
async def review_contribution(
    contribution_id: UUID,
    action: str,
    db: AsyncSession = Depends(get_db),
):
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")

    result = await db.execute(
        select(Contribution).where(Contribution.id == contribution_id)
    )
    contribution = result.scalar_one_or_none()

    if not contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")

    contribution.status = "approved" if action == "approve" else "rejected"
    await db.commit()

    return {"status": contribution.status}
