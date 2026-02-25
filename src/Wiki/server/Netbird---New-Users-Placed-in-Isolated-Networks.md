**Environment**: Self-hosted NetBird, single-account mode, external OIDC auth
**Symptom**: New OIDC sign-ups create separate networks; existing users unaffected but isolated from new users

## Root Cause

Changing netbird domain in the management web interface initial setup/owner account creation, doesn't update that information in the accounts table in store.db. New users match against stale domain entries, triggering new account creation instead of joining the existing network (non matching domain).

## Fix Procedure

1. Stop the management container completely

```Bash
docker compose stop netbird-management
```

2. Backup then edit store.db (should be at /var/lib/netbird/store.db which is in a docker volume/bind-mount).
3. Make sure that only one entry exists under accounts table with the domain name you specified in the --single-account-mode-domain
4. Head to users table and make sure that the user with the same account id as in accounts table has the "owner" role field
5. All other users entries role have the account_id equal to the "owner" user account_id field
6. Place the new store.db back in its location and restart the container.

## Source

Thanks to this comment/issue: https://github.com/netbirdio/netbird/issues/2773#issuecomment-2507115716