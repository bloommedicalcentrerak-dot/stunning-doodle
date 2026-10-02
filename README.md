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
3. Install **Bloom OS Custom** (`bloom_os`).

The module lives in the `bloom_os/` directory so the technical name is a valid Python identifier (the GitHub repo name `Bloom-OS` contains a hyphen and cannot be an Odoo module name).

## Development

```bash
# Lint (matches CI)
pylint --disable=C0103,C0114,C0115,C0116,C0301,R0903,W0104 $(git ls-files '*.py' ':(exclude)bloom_os/models/**')
pylint --disable=C0103,C0114,C0115,C0116,C0301,E0401,R0903,W0104 $(git ls-files 'bloom_os/models/*.py' ':(glob)bloom_os/models/**/*.py' | sort -u)
```

