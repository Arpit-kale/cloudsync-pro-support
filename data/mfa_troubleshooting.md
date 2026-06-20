# Multi-Factor Authentication (MFA) Setup & Recovery
This document provides steps for troubleshooting issues with Authenticator apps, backup codes, and MFA reset procedures.

## MFA Configuration
All CloudSync Pro accounts must configure MFA. Supported methods:
* Authenticator Apps (Google Authenticator, Authy).
* Hardware Security Keys (YubiKey).

## Lost Authenticator App or Device
If you lose your MFA device:
1. Locate the **Backup Recovery Codes** provided during initial MFA setup.
2. Enter a backup recovery code in the verification prompt. (Each backup code is single-use only).

## MFA Reset Procedure
If backup codes are also lost, an administrator of your organization can reset your MFA:
1. Admin Console > Users & Security > Locate user.
2. Click "Reset MFA" for that user.
3. The user will receive an email to reconfigure MFA at their next login.

If you are the sole Account Owner, you must submit a signed verification form and valid company ID to support.
