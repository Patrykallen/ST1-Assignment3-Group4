"""Tests for Stage 9 service workflows and listing integration."""

from datetime import datetime
import pytest
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService


def test_list_practitioner_appointments_workflow():
    store = SmartCareDataStore()
    p_service = PatientService(store)
    d_service = PractitionerService(store)
    a_service = AppointmentService(store)

    p_service.register_patient('P1', 'Alice')
    d_service.register_practitioner('D1', 'Dr. Smith', 'GP')

    dt1 = datetime(2026, 10, 1, 9, 0)
    dt2 = datetime(2026, 10, 1, 10, 0)

    a_service.book_appointment('A1', 'P1', 'D1', dt1)
    a_service.book_appointment('A2', 'P1', 'D1', dt2)

    # Cancel A1 to test history retention and status filtering
    a_service.cancel_appointment('A1')

    # List all statuses (default should include both A1 and A2)
    all_appts = a_service.list_practitioner_appointments('D1', None)
    assert len(all_appts) == 2

    # List scheduled only (should only include A2)
    scheduled_appts = a_service.list_practitioner_appointments('D1', AppointmentStatus.SCHEDULED)
    assert len(scheduled_appts) == 1
    assert scheduled_appts[0].appointment_id == 'A2'

    # Unknown practitioner should raise LookupError
    with pytest.raises(LookupError):
        a_service.list_practitioner_appointments('UNKNOWN', None)