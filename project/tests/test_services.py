
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


# FR-02: Patient Search Tests

def test_find_existing_patient():
    store = SmartCareDataStore()
    service = PatientService(store)

    patient = service.register_patient("P001", "Test Patient")

    result = service.find_patient("P001")

    assert result is patient


def test_find_unknown_patient():
    store = SmartCareDataStore()
    service = PatientService(store)

    with pytest.raises(LookupError):
        service.find_patient("P999")


def test_find_patient_with_whitespace():
    store = SmartCareDataStore()
    service = PatientService(store)

    patient = service.register_patient("P001", "Test Patient")

    result = service.find_patient("  P001  ")

    assert result is patient


def test_find_patient_case_sensitive():
    store = SmartCareDataStore()
    service = PatientService(store)

    service.register_patient("P001", "Test Patient")

    with pytest.raises(LookupError):
        service.find_patient("p001")


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_find_invalid_patient_id(invalid_id):
    store = SmartCareDataStore()
    service = PatientService(store)

    with pytest.raises(ValueError):
        service.find_patient(invalid_id)


# FR-03: Practitioner Lookup Tests

def test_find_existing_practitioner():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    practitioner = service.register_practitioner(
        "DR001",
        "Test Practitioner",
        "General Practice",
    )

    result = service.find_practitioner("DR001")

    assert result is practitioner


def test_find_unknown_practitioner():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    with pytest.raises(LookupError):
        service.find_practitioner("DR999")

    assert store.list_practitioners() == []


def test_find_practitioner_with_whitespace():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    practitioner = service.register_practitioner(
        "DR001",
        "Test Practitioner",
        "General Practice",
    )

    result = service.find_practitioner("  DR001  ")

    assert result is practitioner


def test_find_practitioner_case_sensitive():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    service.register_practitioner(
        "DR001",
        "Test Practitioner",
        "General Practice",
    )

    with pytest.raises(LookupError):
        service.find_practitioner("dr001")


@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])
def test_find_invalid_practitioner_id(invalid_id):
    store = SmartCareDataStore()
    service = PractitionerService(store)

    with pytest.raises(ValueError):
        service.find_practitioner(invalid_id)


# FR-06/FR-07: Appointment Cancellation Tests

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
    assert appointment in store.list_appointments()


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
