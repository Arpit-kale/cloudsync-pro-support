# Storage Quotas & Database Scaling
This document explains database storage limits, quota alerts, and database resizing steps.

## Storage Quotas by Plan
- **Developer**: 5 GB storage limit.
- **Pro Plan**: 500 GB storage limit.
- **Enterprise Plan**: Up to 10 TB (Scalable).

## High Disk Usage Alerts
When storage reaches 85%, CloudSync Pro raises a warning notification.
At 95% disk usage, the database replication pipeline is temporarily paused to prevent disk corruption, and the system returns the error:
`ERR_STORAGE_QUOTA_EXCEEDED` ("Storage quota exceeded. Writes are disabled.")

## Mitigation and Cleanup Steps
1. **Analyze storage usage**: Review large tables and indices via the Admin Dashboard.
2. **Vacuum and Clean**: Execute a DB vacuum/cleanup to free unused blocks.
3. **Upgrade storage volume**:
   * Navigate to console > Clusters > Storage.
   * Adjust the storage slider to add more capacity.
   * Storage scaling is dynamic and completes within 5 minutes without downtime.
