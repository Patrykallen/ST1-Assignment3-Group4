"""Simple workflows using a shared SmartCareDataStore object."""


from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


class PatientService:
    """Coordinate patient registration and lookup through the shared store."""

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate patient operations."""
        self.data_store = data_store

    def register_patient(self, patient_id: str, name: str) -> Patient:
        """Validate and register a patient, returning the stored object.

        Raise ValueError for invalid fields or an existing patient ID.
        """
        patient = Patient(patient_id, name)
        self.data_store.add_patient(patient)
        return patient

    
    def find_patient(self, patient_id: str) -> Patient:
        """Return the original stored patient for a valid patient ID.

        Raise ValueError for invalid IDs and LookupError if not found.
        """
    
        patient = self.data_store.find_patient(patient_id)

        if patient is None:
            raise LookupError('Patient not found')

        return patient


class PractitionerService:
    """Coordinate practitioner registration and lookup through the shared
    store.
    """

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate practitioner operations."""
        self.data_store = data_store

    def register_practitioner(
        self,
        practitioner_id: str,
        name: str,
        specialty: str,
    ) -> Practitioner:
        """Validate and register a practitioner, returning the stored
        object.

        Raise ValueError for invalid fields or an existing practitioner
        ID.
        """
        practitioner = Practitioner(practitioner_id, name, specialty)
        self.data_store.add_practitioner(practitioner)
        return practitioner

    
    def find_practitioner(self, practitioner_id: str) -> Practitioner:
        """Return the original stored practitioner for a valid ID.

        Raise ValueError for invalid IDs and LookupError if not found.
        Do not create or replace practitioner records.
        """
        practitioner = self.data_store.find_practitioner(practitioner_id)

        if practitioner is None:
            raise LookupError('Practitioner not found')

        return practitioner


class AppointmentService:
    """Coordinate booking, lookup and cancellation using the shared store."""

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate appointment operations."""
        self.data_store = data_store

    def book_appointment(
        self,
        appointment_id: str,
        patient_id: str,
        practitioner_id: str,
        date_time: datetime,
    ) -> Appointment:
        """Book registered participant IDs and return the stored
        appointment.

        Raise LookupError for absent participants. Raise ValueError for
        invalid values, duplicate appointment IDs or a practitioner
        conflict.
        """
        patient = self.data_store.find_patient(patient_id)
        practitioner = self.data_store.find_practitioner(practitioner_id)
        if patient is None:
            raise LookupError('Patient not found')
        if practitioner is None:
            raise LookupError('Practitioner not found')
        appointment = Appointment(
            appointment_id,
            patient,
            practitioner,
            date_time,
        )
        if self.data_store.find_appointment(
            appointment.appointment_id,
        ) is not None:
            raise ValueError('Appointment ID already exists')
        if self.data_store.has_practitioner_conflict(
            practitioner.practitioner_id,
            date_time,
        ):
            raise ValueError(
                'Practitioner already has a SCHEDULED appointment at this time',
            )
        self.data_store.add_appointment(appointment)
        return appointment

    def find_appointment(self, appointment_id: str) -> Appointment:
        """Return the stored appointment; raise LookupError when absent.

        Reject a blank or invalid ID with ValueError; do not create
        records.
        """
        appointment = self.data_store.find_appointment(appointment_id)
        if appointment is None:
            raise LookupError('Appointment not found')
        return appointment

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        """Cancel a scheduled appointment and return the stored object.

        Raise ValueError for invalid IDs or illegal state transitions.
        Raise LookupError if the appointment does not exist.
        Retain cancelled appointments in the shared data store.
        """
        appointment = self.data_store.find_appointment(appointment_id)

        if appointment is None:
            raise LookupError('Appointment not found')

        appointment.cancel()

        return appointment



    def list_practitioner_appointments(
        self,
        practitioner_id: str,
        status: AppointmentStatus | None = None,
    ) -> list[Appointment]:
        """Stage 9: new ordered list; default includes every status.

        Unknown practitioner raises LookupError, invalid status
        ValueError; a known practitioner with no matches returns an
        empty list.
        """
        # 1. Validate practitioner existence using the store contract (raises LookupError if missing/unknown)
        practitioner = self.data_store.find_practitioner(practitioner_id)
        if practitioner is None:
            raise LookupError('Practitioner not found')

        # 2. Validate status if provided (must be an AppointmentStatus enum or None)
        if status is not None and not isinstance(status, AppointmentStatus):
            raise ValueError('Invalid appointment status')

        # 3. Retrieve all appointments from the shared store
        all_appointments = self.data_store.list_appointments()

        # 4. Use our pure query from queries.py to select and sort them
        from smartcare.queries import select_appointments
        return select_appointments(all_appointments, practitioner.practitioner_id, status)
