import pytest
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PractitionerService


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
