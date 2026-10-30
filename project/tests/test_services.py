
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

# FR-01: Patient Registration

def test_register_valid_patient():
    store = SmartCareDataStore()
    service = PatientService(store)
    patient = service.register_patient("P001", "Jane Doe")
    assert service.find_patient("P001") is patient
    assert patient.name == "Jane Doe"

def test_register_duplicate_patient_id():
    store = SmartCareDataStore()
    service = PatientService(store)
    service.register_patient("P001", "Jane Doe")
    with pytest.raises(ValueError):
        service.register_patient("P001", "John Doe")

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


# FR-05: Practitioner conflict and boundary tests

def test_book_appointment_practitoner_conflict():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P001", "Jane Doe")
    patient_service.register_patient("P002", "John Doe")
    practitioner_service.register_practitioner("DR001", "Dr. Smith", "General Practice")
    appointment_time = datetime(2026, 11, 15, 10, 0)

    #book first appointment 
    appointment_service.book_appointment("A001", "P001", "DR001", appointment_time)

    #Attempting to book the same practioner at same time must fail
    with pytest.raises(ValueError):
        appointment_service.book_appointment("A001", "P002", "DR001", appointment_time)


def test_book_different_practitoner_same_time_allowed():
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P001", "Jane Doe")
    practitioner_service.register_practitioner("DR001", "Dr. Smith", "General Practice")
    practitioner_service.register_practitioner("DR002", "Dr. Adams", "Cardiology")
    appointment_time = datetime(2026, 11, 15, 10, 0)

    #Booking two different doctors at the same time is allowed
    apt1 = appointment_service.book_appointment("A001", "P001", "DR001", appointment_time)
    apt2 = appointment_service.book_appointment("A002", "P001", "DR002", appointment_time)

    assert apt1 in store.list_appointments()
    assert apt2 in store.list_appointments()


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


def test_unknown_participants_leave_state_unchanged():
    store = SmartCareDataStore()
    appointment_service = AppointmentService(store)
    appointment_time = datetime(2026, 11, 15, 10, 0)

    initial_count = len(store.list_appointments())

    # Booking with a non-existent patient should raise LookupError and not add an appointment
    with pytest.raises(LookupError):
        appointment_service.book_appointment("A001", "NON_EXISTENT", "DR001", appointment_time)

    assert len(store.list_appointments()) == initial_count


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
