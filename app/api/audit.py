from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
