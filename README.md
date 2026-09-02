# Leeway International — Attendance Master Portal

Corporate attendance portal for Employee Master, BIO biometric attendance and TOS data processing.

## Live

GitHub Pages: https://srp8046-del.github.io/Attendance/

## Current release

The portal is a single-page GitHub Pages application in `index.html`.

### Features
- Corporate responsive dashboard
- Light / dark theme
- Employer/Admin and Employee entry model
- Employee Master directory
- Browser-side CSV uploads for Employee Master, BIO and TOS
- Employee Master mapping between BIO Employee Code and TOS Agent ID
- BIO attendance rules
- TOS calculation for Tele Sales Executive
- Final status severity: ABSENT > HALFDAY > LATE > PRESENT
- Search and filters
- Attendance register
- CSV report export
- No raw employee attendance files committed to the public repository

## Attendance rules

BIO:
- Missing IN or OUT: NOT PUNCHED
- < 04:00: ABSENT
- 04:00–06:59: HALFDAY
- 07:00–07:59: LATE
- >= 08:00: PRESENT

TOS applies only to `Tele Sales Executive`:

`TOS = LOGIN TIME - LUNCH TIME - TEA TIME - TRAINING TIME`

Final Tele Sales status uses the worse of BIO and TOS.

## Security note

GitHub Pages is static hosting. The current sign-in is a UI/demo gate, not production authentication. Do not place employee passwords, confidential attendance records, or other secrets in this public repository. For production authentication, centralized storage, audit logs, and office-network-only access, connect the frontend to a secure backend/identity provider and enforce network controls server-side.

## Data format

Employee Master columns supported by the current build include:

`Employee Code, NAME, DESIGNATION, SUPERVISOR, CAMPAIGN / PROCESS, DOJ, SHIFT, SHIFT IN, SHIFT OUT, AGENT ID`

TOS columns include:

`DATE, AGENT ID, AGENT NAME, LOGIN TIME, LUNCH TIME, TEA TIME, TRAINING TIME`

BIO CSV exports should provide employee/date/in/out fields. The mapping engine intentionally preserves the two ID systems and links them through Employee Master.
