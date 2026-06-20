# Backup Restoration Guidelines
This article details point-in-time recovery (PITR), retention policies, and backup validation in CloudSync Pro.

## Automated Backups
* **Frequency**: Daily full snapshot with continuous write-ahead log (WAL) archiving.
* **Retention Period**:
  * Developer Tier: 7 days.
  * Pro Tier: 30 days.
  * Enterprise Tier: 90 days.

## Point-in-Time Recovery (PITR)
PITR allows restoring your database to any millisecond within the retention period.

**Steps to Restore**:
1. Open the Admin Console > Clusters > select cluster.
2. Under "Backups", select "Point-in-Time Recovery".
3. Specify the target date and time down to the second.
4. Click "Validate & Restore".
5. A temporary staging cluster will be provisioned first. Once validation passes, you can redirect production traffic to the restored instance.

*Note*: Backup restoration time depends on the database size, averaging 10 minutes per 100 GB.
