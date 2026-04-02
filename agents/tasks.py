"""
Celery Tasks — Async background job definitions.

Defines Celery tasks for:
- VLM extraction (heavy, GPU-optional)
- Remediation timeout checks (scheduled)
- Fraud model retraining (weekly)
- Batch expense ingestion
- Notification delivery
"""

import os

from celery import Celery
from celery.schedules import crontab

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")

app = Celery("aegis", broker=CELERY_BROKER_URL)

# Celery configuration
app.conf.update(
    result_backend=CELERY_BROKER_URL,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Periodic task schedule
app.conf.beat_schedule = {
    "check-remediation-timeouts": {
        "task": "tasks.check_remediation_timeouts",
        "schedule": crontab(minute=0),  # Every hour
    },
    "retrain-fraud-model": {
        "task": "tasks.retrain_fraud_model",
        "schedule": crontab(hour=2, minute=0, day_of_week="sunday"),  # Sunday 2AM UTC
    },
}


@app.task(name="tasks.process_expense_extraction", queue="extraction", max_retries=3)
def process_expense_extraction(expense_id: str, s3_key: str) -> dict:
    """
    Extract structured data from a receipt via VLM.

    Heavy task — runs on dedicated extraction workers.
    """
    # TODO: Download file, call VLM, store results
    return {"expense_id": expense_id, "status": "not_implemented"}


@app.task(name="tasks.check_remediation_timeouts", queue="remediation")
def check_remediation_timeouts() -> dict:
    """
    Check for expired remediation sessions (48h timeout).

    Runs every hour via Celery Beat.
    """
    # TODO: Query remediation_sessions for expired sessions
    # TODO: Auto-escalate expired sessions
    return {"checked": 0, "escalated": 0}


@app.task(name="tasks.retrain_fraud_model", queue="ml")
def retrain_fraud_model() -> dict:
    """
    Retrain the Isolation Forest fraud model on latest data.

    Runs weekly (Sunday 2AM UTC) via Celery Beat.
    """
    # TODO: Load last 90 days of approved expenses
    # TODO: Train new Isolation Forest model
    # TODO: Save model artifact to disk
    return {"status": "not_implemented"}


@app.task(name="tasks.send_notification", queue="notify", max_retries=3)
def send_notification(channel: str, message: str, expense_id: str) -> dict:
    """Send a notification via Slack/email."""
    # TODO: Route to appropriate notification channel
    return {"delivered": False, "reason": "not_implemented"}
