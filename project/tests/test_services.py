
import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService, PractitionerService


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
