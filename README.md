# Bloom OS

Odoo clinic management app for Bloom Medical Center.

## Module

Installable addon technical name: **`bloom_os`**

Features:

- **Patients** — auto code (`PAT/`), contact details, Emirates ID, medical
  history, allergies, emergency contacts and chatter
- **Appointments** — calendar view, doctor / room / service, draft → confirmed
  → done
- **Laser & slimming sessions** — package link, pricing, BMI tracking,
  done / cancel
- **Treatment packages** — total / used / remaining sessions
- **Doctors & staff, rooms and services** — seeded with the Bloom Medical
  Center setup
- **Payments** — cash / card / bank transfer
- **Dashboard** — patients, today's appointments, sessions, packages and
  collected payments
- **Security** — Clinic User / Clinic Manager groups with access rights

## Odoo.sh / local install

1. Add this repository to your Odoo addons path (Odoo.sh: connect the GitHub repo).
2. Update the apps list (Apps → Update Apps List).
3. Install **Bloom OS Custom** (`bloom_os`).
4. Assign users to the **Clinic User** or **Clinic Manager** group
   (Settings → Users & Companies → Users → *Bloom OS*).

The module lives in the `bloom_os/` directory so the technical name is a valid Python identifier (the GitHub repo name `Bloom-OS` contains a hyphen and cannot be an Odoo module name).

```
bloom_os/
  models/   patient, doctor, room, service, package, appointment, laser, slimming, payment, dashboard
  views/    forms, lists, calendar, menus
  data/     sequences + staff/rooms/services seed
  security/ groups + ir.model.access.csv
```

## HID ID card reader

The Patient form has a **Scan ID** field, focused automatically when the form
opens. Most USB ID/card readers (e.g. Emirates ID readers) work in
keyboard-emulation ("HID wedge") mode: no driver is needed, the reader just
"types" the card data followed by Enter/Tab wherever the cursor is.

1. Open a patient record (or click **New**) — the **Scan ID** field is
   focused by default.
2. Insert/swipe the card in the reader.
3. When the field loses focus, Odoo parses the scanned text and fills in
   **Patient Name** and **Emirates ID** automatically (an Emirates ID number
   is detected as `784-XXXX-XXXXXXX-X`; any remaining alphabetic text is used
   as the name if it is still empty). The **Scan ID** field is cleared so it
   is ready for the next card.

If your reader's output format differs (e.g. a smart-card SDK instead of
keyboard emulation), the parsing logic in
`bloom_os/models/patient.py::_onchange_id_scan_raw` should be adjusted to
match its actual output.

## Development

```bash
# Lint (matches CI)
mapfile -d '' NON_MODELS < <(git ls-files -z -- '*.py' ':(exclude)bloom_os/models/**')
mapfile -d '' MODELS < <(git ls-files -z -- 'bloom_os/models/*.py' ':(glob)bloom_os/models/**/*.py' | sort -zu)
pylint --disable=C0103,C0114,C0115,C0116,C0301,R0903,W0104 "${NON_MODELS[@]}"
pylint --disable=C0103,C0114,C0115,C0116,C0301,E0401,R0903,W0104 "${MODELS[@]}"
```
