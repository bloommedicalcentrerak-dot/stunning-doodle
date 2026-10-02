# Bloom OS

Odoo clinic management app for Bloom Medical Center.

## Module

Installable addon technical name: **`bloom_os`**

Features:

- Patients
- Team management
- Appointments (draft → confirmed → done)
- Laser sessions
- Slimming sessions
- Live dashboard totals
- Departments
- Purchase tracking with delivery dates, status, stock alerts, and document uploads
- Upcoming appointments on the dashboard
- Patient history with linked clinic records

## Odoo.sh install

1. Open your Odoo.sh project and connect this GitHub repository.
2. Make sure the repository is available in the build so Odoo can read the `bloom_os/` addon directory.
3. Open the Odoo instance for the branch you want to use.
4. Go to **Apps**.
5. Click **Update Apps List**.
6. Search for **Bloom OS Custom** or the technical name **`bloom_os`**.
7. Click **Install**.

## Odoo local install

1. Add the repository root directory (the directory that contains `bloom_os/`) to your Odoo addons path.
2. Restart the Odoo server.
3. Open **Apps** in Odoo.
4. Click **Update Apps List**.
5. Search for **Bloom OS Custom** or **`bloom_os`**.
6. Click **Install**.

## Where the app is

- Installable addon folder: `bloom_os/`
- Technical module name: `bloom_os`
- Display name in Odoo: **Bloom OS Custom**

## Purchases

The app now includes a simple clinic purchases section for:

- Items, devices, and materials
- Departments
- Suppliers
- Ordered quantity and received quantity
- Order date, expected delivery date, and received date
- Statuses: Draft, Ordered, Partially Received, Received, Cancelled
- Low-stock and overdue-delivery alerts
- Invoice, quotation, receipt, and other document uploads

The module lives in the `bloom_os/` directory so the technical name is a valid Python identifier (the GitHub repo name `Bloom-OS` contains a hyphen and cannot be an Odoo module name).

## Quick usage

1. Open **Dashboard** to see clinic totals and the next appointments.
2. Add a patient from **Patients**.
3. Add your clinic team from **Team** and assign staff members to work records.
4. Create an appointment and move it through Draft, Confirmed, Done, or Cancelled.
5. Add **Laser Sessions** or **Slimming Sessions** for the patient.
6. Open the patient or team form to review the full record history in one place.

## Development

```bash
# Lint (matches CI)
mapfile -d '' -t non_models < <(git ls-files -z '*.py' ':!:models/**' ':!:*/models/**')
mapfile -d '' -t models < <(git ls-files -z 'models/*.py' ':(glob)models/**/*.py' '*/models/*.py' ':(glob)*/models/**/*.py' | sort -zu)

if [ "${#non_models[@]}" -gt 0 ]; then
  pylint --disable=C0103,C0114,C0115,C0116,C0301,R0903,W0104 "${non_models[@]}"
fi

if [ "${#models[@]}" -gt 0 ]; then
  pylint --disable=C0103,C0114,C0115,C0116,C0301,E0401,R0801,R0903,W0104 "${models[@]}"
fi
```
