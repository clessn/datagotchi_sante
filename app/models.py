from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app import login

from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    user_id: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    interac: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    condition_id: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))                                   

    logs: so.WriteOnlyMapped['Log'] = so.relationship(
        back_populates='participant')

    def __repr__(self):
        return f'{self.email} - condition : {self.condition_id}'
    
    def get_id(self):
        return self.user_id

    def assign_condition(self, condition_id):
        """Assigns a condition ID to the user."""
        self.condition_id = condition_id
        db.session.commit()


class Question(db.Model):
    question_id: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    question_content: so.Mapped[str] = so.mapped_column(sa.String(1000),
                                             unique=True) 
    group_id: so.Mapped[str] = so.mapped_column(sa.String(64))
    form_id: so.Mapped[str] = so.mapped_column(sa.String(64))                              

    logs: so.WriteOnlyMapped['Log'] = so.relationship(
        back_populates='question')
    
    answers: so.WriteOnlyMapped['Answer'] = so.relationship(
        back_populates='question')

    def __repr__(self):
        return f'{self.question_id} ({self.group_id}) - {self.form_id}'


    def get_answer(self):
        query = self.answers.select()
        answers = db.session.scalars(query).all()
        return answers
    
    def get_form(self):
        form = []
        query = self.answers.select()
        answers = db.session.scalars(query).all()
        for answer in answers:
            form.append((answer.answer_id,answer.answer_content))
        return form

class Answer(db.Model):
    answer_id: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    answer_content: so.Mapped[str] = so.mapped_column(sa.String(1000)) 
    answer_weight: so.Mapped[int] = so.mapped_column(sa.Integer)

    question_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Question.question_id),index=True)                           
    question: so.Mapped['Question'] = so.relationship(back_populates='answers')

    logs: so.WriteOnlyMapped['Log'] = so.relationship(
        back_populates='answer')

    def __repr__(self):
        return f'{self.answer_id} - weight: {self.answer_weight}'



class Log(db.Model):
    log_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    user_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(User.user_id),index=True)
    participant: so.Mapped['User'] = so.relationship(back_populates='logs')

    question_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Question.question_id),index=True)
    question: so.Mapped['Question'] = so.relationship(back_populates='logs')

    answer_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Answer.answer_id),index=True)
    answer: so.Mapped['Answer'] = so.relationship(back_populates='logs')

    phase_id: so.Mapped[str] = so.mapped_column(sa.String(64))

    def __repr__(self):
        return f'{self.timestamp} - Q:{self.question_id} - A:{self.answer_id}'


