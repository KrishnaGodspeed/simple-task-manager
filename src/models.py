from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # SAARTHI-202506031552: MEDIUM | CORRECTNESS
    # ISSUE: The `due_date` column should be nullable as per PRD FR-001.
    # POLICY: PRD FR-001 states that the due date is optional.
    # FIX: Set `nullable=True` for the `due_date` column.
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    ALLOWED_STATUSES = {"pending", "in progress", "completed"}

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

    def to_dict(self, detailed=True):
        """
        Serializes the Task object to a dictionary.

        Args:
            detailed (bool): If True, returns all task details. If False, returns only ID, title, and status (for list view as per PRD FR-002).

        Returns:
            dict: A dictionary representation of the Task object.
        """
        if detailed:
            data = {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'due_date': self.due_date.isoformat() if self.due_date else None,
                'status': self.status,
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
        else: # For list view as per PRD FR-002
            data = {
                'id': self.id,
                'title': self.title,
                'status': self.status
           }
        return data

    # SAARTHI-202506031552: LOW | LINTING
    # ISSUE: Method name `check_and_update_status` does not follow snake_case naming convention.
    # POLICY: OrgPolicy_compliance.md: Policy 3.1 - Python: `snake_case` for functions, variables, and modules.
    # FIX: Rename the method to `check_and_update_status`.
    def check_and_update_status(self, new_status):
        if new_status not in self.ALLOWED_STATUSES:
            # SAARTHI-202506031552: MEDIUM | CODE QUALITY
            # ISSUE: The method should raise a ValueError instead of returning False to provide more informative error handling.
            # POLICY: N/A
            # FIX: Raise a ValueError if the new_status is invalid.
            return False  # Or raise ValueError
        self.status = new_status
        return True

    # SAARTHI-202506031552: MEDIUM | COMPLIANCE
    # ISSUE: Task descriptions are not currently encrypted at rest, which could be a compliance issue if descriptions contain PII.
    # POLICY: OrgPolicy_compliance.md: Policy 1.4 - Data Security in Transit & At Rest.
    # FIX: Implement encryption for task descriptions at rest if they are deemed sensitive.


