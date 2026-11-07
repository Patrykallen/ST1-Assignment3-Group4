"""Tests for Stage 9 pure queries (sorting and filtering)."""

from datetime import datetime
from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key, select_appointments


def test_appointment_sort_key():
    p = Patient('P1', 'Alice')
    d = Practitioner('D1', 'Dr. Smith', 'GP')
    dt1 = datetime(2026, 10, 1, 9, 0)
    dt2 = datetime(2026, 10, 1, 10, 0)

    app1 = Appointment('A2', p, d, dt1)
    app2 = Appointment('A1', p, d, dt1)

    # Same datetime, should tie-break by appointment_id ('A1' before 'A2')
    key1 = appointment_sort_key(app1)
    key2 = appointment_sort_key(app2)
    assert key2 < key1


def test_select_appointments_filtering_and_sorting():
    p = Patient('P1', 'Alice')
    d1 = Practitioner('D1', 'Dr. Smith', 'GP')
    d2 = Practitioner('D2', 'Dr. Jones', 'GP')

    dt1 = datetime(2026, 10, 1, 10, 0)
    dt2 = datetime(2026, 10, 1, 9, 0)

    app1 = Appointment('A1', p, d1, dt1, AppointmentStatus.SCHEDULED)
    app2 = Appointment('A2', p, d1, dt2, AppointmentStatus.SCHEDULED)
    app3 = Appointment('A3', p, d2, dt1, AppointmentStatus.SCHEDULED)

    appointments = [app1, app2, app3]

    # Select for D1, should be ordered by time ascending (dt2 comes before dt1)
    result = select_appointments(appointments, 'D1')
    assert len(result) == 2
    assert result[0].appointment_id == 'A2'
    assert result[1].appointment_id == 'A1'