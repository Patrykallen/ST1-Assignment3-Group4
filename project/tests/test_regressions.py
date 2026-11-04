"""Stage 8 regression tests for the two prepared defects (F8-01, F8-02)."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def make_services():
    # Return a fresh store and services with synthetic participants.
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)
    patient_service.register_patient('P001', 'Alex Example')
    patient_service.register_patient('P002', 'Sam Example')
    practitioner_service.register_practitioner('DR001', 'Dr Lee', 'General')
    practitioner_service.register_practitioner('DR002', 'Dr Kim', 'Cardiology')
    return store, appointment_service


def test_f8_01_same_practitioner_same_time_conflicts_other_allowed():
    #F8-01: FR-05 / AC-04.1 rejects a same-practitioner SCHEDULED
    # conflict without changing state; AC-04.2 allows another practitioner.
    store, appointment_service = make_services()
    when = datetime(2026, 11, 15, 10, 0)
    first = appointment_service.book_appointment('A001', 'P001', 'DR001', when)

    with pytest.raises(ValueError):
        appointment_service.book_appointment('A002', 'P002', 'DR001', when)
    assert store.list_appointments() == [first]
    assert store.find_appointment('A002') is None

    other = appointment_service.book_appointment('A003', 'P002', 'DR002', when)
    assert other.practitioner.practitioner_id == 'DR002'
    assert other.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment('A003') is other


def test_f8_02_cancelled_appointment_is_retained_and_found():
    # F8-02: FR-06/07, BR-07, AC-05.2 and FR-08 keep the same cancelled
    # appointment in the store, findable by store and service; AC-05.3
    # rejects repeated cancellation without changing it.
    
    store, appointment_service = make_services()
    appointment = appointment_service.book_appointment(
        'A001', 'P001', 'DR001', datetime(2026, 11, 10, 10, 0),
    )

    assert appointment_service.cancel_appointment('A001') is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment in store.list_appointments()
    assert store.find_appointment('A001') is appointment
    assert appointment_service.find_appointment('A001') is appointment

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A001')
    assert appointment.status is AppointmentStatus.CANCELLED
    assert store.list_appointments() == [appointment]


def test_cancelled_appointment_does_not_block_same_practitioner_slot():
    # FR-05 / BR-05: only a SCHEDULED appointment conflicts so the same
    # practitioner can be rebooked at the time of a cancelled appointment.
    
    store, appointment_service = make_services()
    when = datetime(2026, 11, 20, 9, 0)
    cancelled = appointment_service.book_appointment('A001', 'P001', 'DR001', when)
    appointment_service.cancel_appointment('A001')

    rebooked = appointment_service.book_appointment('A002', 'P002', 'DR001', when)

    assert rebooked.status is AppointmentStatus.SCHEDULED
    assert store.list_appointments() == [cancelled, rebooked]
    assert cancelled.status is AppointmentStatus.CANCELLED