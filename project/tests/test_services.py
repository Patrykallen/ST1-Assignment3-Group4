import pytest
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)


def test_cancel_scheduled_appointment():
    store = SmartCareDataStore()

    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P001", "Test Patient")
    practitioner_service.register_practitioner(
        "DR001", "Test Doctor", "General Practice"
    )

    appointment = appointment_service.book_appointment(
        "A001",
        "P001",
        "DR001",
        datetime(2026, 11, 10, 10, 0),
    )

    result = appointment_service.cancel_appointment("A001")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment_service.find_appointment("A001") is appointment


def test_cancel_appointment_twice():
    store = SmartCareDataStore()

    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P001", "Test Patient")
    practitioner_service.register_practitioner(
        "DR001", "Test Doctor", "General Practice"
    )

    appointment = appointment_service.book_appointment(
        "A001",
        "P001",
        "DR001",
        datetime(2026, 11, 10, 10, 0),
    )

    appointment_service.cancel_appointment("A001")

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A001")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment_service.find_appointment("A001") is appointment


def test_cannot_cancel_completed_appointment():
    store = SmartCareDataStore()

    patient = PatientService(store).register_patient(
        "P001", "Test Patient"
    )
    practitioner = PractitionerService(store).register_practitioner(
        "DR001", "Test Doctor", "General Practice"
    )

    appointment = Appointment(
        "A001",
        patient,
        practitioner,
        datetime(2026, 11, 10, 10, 0),
        AppointmentStatus.COMPLETED,
    )
    store.add_appointment(appointment)

    appointment_service = AppointmentService(store)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A001")

    assert appointment.status is AppointmentStatus.COMPLETED
    assert appointment_service.find_appointment("A001") is appointment


def test_cancel_unknown_appointment():
    store = SmartCareDataStore()
    appointment_service = AppointmentService(store)

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment("A999")


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_cancel_invalid_appointment_id(invalid_id):
    store = SmartCareDataStore()
    appointment_service = AppointmentService(store)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(invalid_id)
