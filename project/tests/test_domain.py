from datetime import datetime
import pytest

from smartcare.domain import (
    Patient,
    Practitioner,
    Appointment,
    AppointmentStatus,
)


# --- 1. Patient Domain Tests ---

def test_patient_valid_construction_and_trimming():
    # IDs should trim whitespace and retain valid attributes
    patient = Patient("  P001  ", "Jane Doe")
    assert patient.patient_id == "P001"
    assert patient.name == "Jane Doe"


def test_patient_blank_id_rejected():
    # Reference intention: blank patient ID rejected
    with pytest.raises(ValueError):
        Patient("", "Jane Doe")
    with pytest.raises(ValueError):
        Patient("   ", "Jane Doe")


# --- 2. Practitioner Domain Tests ---

def test_practitioner_valid_construction():
    practitioner = Practitioner("DR001", "Dr. Smith", "General Practice")
    assert practitioner.practitioner_id == "DR001"
    assert practitioner.name == "Dr. Smith"
    assert practitioner.specialty == "General Practice"


def test_practitioner_blank_id_rejected():
    with pytest.raises(ValueError):
        Practitioner("", "Dr. Smith", "General Practice")


# --- 3. Appointment Domain Tests ---

def test_appointment_initial_status_scheduled():
    # Reference intention: a new appointment starts SCHEDULED
    patient = Patient("P001", "Jane Doe")
    practitioner = Practitioner("DR001", "Dr. Smith", "General Practice")
    apt_time = datetime(2026, 11, 15, 10, 0)

    appointment = Appointment("A001", patient, practitioner, apt_time)
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_appointment_cancellation_changes_status():
    # Reference intention: cancellation changes status
    patient = Patient("P001", "Jane Doe")
    practitioner = Practitioner("DR001", "Dr. Smith", "General Practice")
    appointment = Appointment("A001", patient, practitioner, datetime(2026, 11, 15, 10, 0))

    appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_appointment_repeated_cancellation_rejected():
    # Reference intention: repeated cancellation is rejected
    patient = Patient("P001", "Jane Doe")
    practitioner = Practitioner("DR001", "Dr. Smith", "General Practice")
    appointment = Appointment("A001", patient, practitioner, datetime(2026, 11, 15, 10, 0))

    appointment.cancel()
    with pytest.raises(ValueError):
        appointment.cancel()


def test_appointment_completed_cancellation_guard():
    # COMPLETED supplied at construction to test a cancellation guard
    patient = Patient("P001", "Jane Doe")
    practitioner = Practitioner("DR001", "Dr. Smith", "General Practice")
    
    appointment = Appointment(
        "A001",
        patient,
        practitioner,
        datetime(2026, 11, 15, 10, 0),
        status=AppointmentStatus.COMPLETED
    )
    
    with pytest.raises(ValueError):
        appointment.cancel()