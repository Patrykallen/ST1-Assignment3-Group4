"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Stage 9: implement the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit. main.py reports the incomplete menu
    without crashing.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    while True:
        print("\n=== SmartCare Clinic Menu ===")
        print("1. Register Patient")
        print("2. Find Patient")
        print("3. Register Practitioner")
        print("4. Find Practitioner")
        print("5. Book Appointment")
        print("6. Cancel Appointment")
        print("7. Find Appointment")
        print("8. List Practitioner Appointments")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == '1':
                pid = input("Patient ID: ").strip()
                name = input("Patient Name: ").strip()
                p = patients.register_patient(pid, name)
                print(f"Registered Patient: {p.patient_id} - {p.name}")

            elif choice == '2':
                pid = input("Patient ID to find: ").strip()
                p = patients.find_patient(pid)
                print(f"Found Patient: {p.patient_id} - {p.name}")

            elif choice == '3':
                drid = input("Practitioner ID: ").strip()
                name = input("Practitioner Name: ").strip()
                spec = input("Specialty: ").strip()
                d = practitioners.register_practitioner(drid, name, spec)
                print(f"Registered Practitioner: {d.practitioner_id} - {d.name} ({d.specialty})")

            elif choice == '4':
                drid = input("Practitioner ID to find: ").strip()
                d = practitioners.find_practitioner(drid)
                print(f"Found Practitioner: {d.practitioner_id} - {d.name} ({d.specialty})")

            elif choice == '5':
                aid = input("Appointment ID: ").strip()
                pid = input("Patient ID: ").strip()
                drid = input("Practitioner ID: ").strip()
                dt_str = input("Date & Time (YYYY-MM-DD HH:MM): ").strip()
                dt = parse_date_time(dt_str)
                appt = appointments.book_appointment(aid, pid, drid, dt)
                print(f"Booked: {format_appointment(appt)}")

            elif choice == '6':
                aid = input("Appointment ID to cancel: ").strip()
                appt = appointments.cancel_appointment(aid)
                print(f"Cancelled: {format_appointment(appt)}")

            elif choice == '7':
                aid = input("Appointment ID to find: ").strip()
                appt = appointments.find_appointment(aid)
                print(f"Found: {format_appointment(appt)}")

            elif choice == '8':
                drid = input("Practitioner ID: ").strip()
                status_str = input(
                    "Status filter (scheduled/cancelled/completed or blank for all): "
                ).strip().lower()

                status = None
                if status_str:
                    from smartcare.domain import AppointmentStatus
                    status = AppointmentStatus(status_str)

                list_appts = appointments.list_practitioner_appointments(drid, status)
                if not list_appts:
                    print("No appointments found.")
                else:
                    for appt in list_appts:
                        print(format_appointment(appt))

            elif choice == '0':
                print("Exiting session. All session data is discarded.")
                break
            else:
                print("Error: Invalid menu option.")

        except (ValueError, LookupError) as error:
            print(f"Error: {error}")