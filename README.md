# Bloom OS

Odoo clinic management app for Bloom Medical Center.

## Module

Installable addon technical name: **`bloom_os`**

Features:

- Patients
- Appointments (draft → confirmed → done)
- Laser sessions
- Slimming sessions
- Live dashboard totals

## Odoo.sh / local install

1. Add this repository to your Odoo addons path (Odoo.sh: connect the GitHub repo).
2. Update the apps list.
3. Install **Bloom OS Custom** (`bloom_os`). Tick **"Load demonstration data"** (or pass `--demo=all` on the CLI) to seed a sample department, room, doctor and patient with a first draft appointment, so you can log in and confirm a booking immediately.

The module lives in the `bloom_os/` directory so the technical name is a valid Python identifier (the GitHub repo name `Bloom-OS` contains a hyphen and cannot be an Odoo module name).

## Module structure

```
bloom_os/
├── __init__.py
├── __manifest__.py       # Module metadata, dependencies and data files
├── models/               # Python models (business logic)
├── security/             # Access control rules
└── views/                # Form/tree/kanban views and menus
```

The module depends only on Odoo's `base` module.

## Models

| Model | Description | Key fields |
| --- | --- | --- |
| `bloom.patient` | Clinic patient record | `name`, `phone`, `emirates_id`, `notes`, `active`; reverse `One2many` links to appointments, laser and slimming sessions |
| `bloom.department` | Clinic department | `name`, `code`, `active` |
| `bloom.room` | Physical treatment room | `name`, `department_id` (`Many2one` to `bloom.department`), `active` |
| `bloom.doctor` | Doctor record | `name`, `specialty`, `department_id` (`Many2one` to `bloom.department`), `phone`, `active` |
| `bloom.appointment` | Appointment booking | `patient_id` (required, cascade delete), `date`, `doctor_id`, `room_id`, `service_type` (`laser`/`slimming`/`consultation`), `notes`, `state` (`draft` → `confirmed` → `done`, or `cancelled`) |
| `bloom.laser` | Laser treatment session | `patient_id` (required, cascade delete), `session_date`, `area`, `machine`, `notes` |
| `bloom.slimming` | Slimming program session | `patient_id` (required, cascade delete), `session_date`, `program`, `weight`, `notes` |
| `bloom.dashboard` | Transient model backing the live dashboard | Computed totals: `total_patients`, `total_appointments`, `total_laser_sessions`, `total_slimming_sessions` |

### Appointment workflow

`bloom.appointment.state` moves through `draft` → `confirmed` → `done`, with `cancelled` available at any point via the following methods:

- `action_confirm()` — sets state to `confirmed`
- `action_done()` — sets state to `done`
- `action_cancel()` — sets state to `cancelled`
- `action_draft()` — resets state to `draft`

### Dashboard

`bloom.dashboard` is a `TransientModel`. Calling `action_open_dashboard()` creates a transient record and opens it in a form view, with totals computed on the fly from `bloom.patient`, `bloom.appointment`, `bloom.laser` and `bloom.slimming` record counts.

## Security

Access rights are defined in `bloom_os/security/ir.model.access.csv`. Every model (`bloom.patient`, `bloom.department`, `bloom.room`, `bloom.doctor`, `bloom.appointment`, `bloom.laser`, `bloom.slimming`, `bloom.dashboard`) grants full read/write/create/unlink permissions to `base.group_user` (any internal/logged-in user). There are no restricted groups or record rules beyond this.

## Views

Each model has a corresponding view file under `bloom_os/views/`:

- `patient_view.xml` — patient form/list views and the `menu_bloom_root` top-level menu
- `department_view.xml`, `room_view.xml`, `doctor_view.xml` — supporting master data
- `appointment_view.xml` — appointment form/list views and menu
- `laser_view.xml`, `slimming_view.xml` — treatment session views and menus
- `dashboard_view.xml` — dashboard form view and menu entry

All other menus attach under `menu_bloom_root` (declared in `patient_view.xml`), and the manifest's `data` list controls load order.

## Demo data

`bloom_os/data/demo_data.xml` (loaded only when demo data is enabled) seeds:

- Department: **General Medicine**
- Room: **Room 1** (in General Medicine)
- Doctor: **Dr. Sarah Ahmed** (General Practitioner, in General Medicine)
- Patient: **First Client**
- A **draft** appointment tomorrow linking the patient, doctor and room, ready to be confirmed via **Bloom OS → Appointments**.

## Development

```bash
# Lint (matches CI)
mapfile -d '' NON_MODELS < <(git ls-files -z -- '*.py' ':(exclude)bloom_os/models/**')
mapfile -d '' MODELS < <(git ls-files -z -- 'bloom_os/models/*.py' ':(glob)bloom_os/models/**/*.py' | sort -zu)
pylint --disable=C0103,C0114,C0115,C0116,C0301,R0903,W0104 "${NON_MODELS[@]}"
pylint --disable=C0103,C0114,C0115,C0116,C0301,E0401,R0801,R0903,W0104 "${MODELS[@]}"
```
