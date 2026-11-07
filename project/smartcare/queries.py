"""Stage 9 contracts for pure collection processing."""

from datetime import datetime
from smartcare.domain import Appointment, AppointmentStatus


def appointment_sort_key(appointment: Appointment) -> tuple[datetime, str]:
    """Return the date/time and appointment ID ordering key without side effects."""
    return (appointment.date_time, appointment.appointment_id)


def select_appointments(
    appointments: list[Appointment],
    practitioner_id: str,
    status: AppointmentStatus | None = None,
) -> list[Appointment]:
    """Return a new list for this practitioner, optionally filtered by status.

    Order by date/time then appointment ID using appointment_sort_key.
    Do not mutate the source list/objects or perform input/output.
    """
    # 1. Filter by practitioner ID and optional status
    filtered = [
        appt for appt in appointments
        if appt.practitioner.practitioner_id == practitioner_id
        and (status is None or appt.status == status)
    ]

    # 2. Return a new sorted list using the named key
    return sorted(filtered, key=appointment_sort_key)