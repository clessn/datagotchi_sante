from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    user_id: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    interac: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    condition_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))                                   

    logs: so.WriteOnlyMapped['Log'] = so.relationship(
        back_populates='participant')

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Log(db.Model):
    log_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.user_id),index=True)
    participant: so.Mapped['User'] = so.relationship(back_populates='logs')

    phase_id: so.Mapped[str] = so.mapped_column(sa.String(64))

    def __repr__(self):
        return '<Log {}>'.format(self.timestamp)
