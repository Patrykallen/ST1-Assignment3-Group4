import pytest
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


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
