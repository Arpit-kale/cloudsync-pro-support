# Data Sync Delay & Replica Lag
This article covers diagnosing and resolving synchronization delays and replica lag between source and destination databases in CloudSync Pro.

## Understanding Replication Lag
Replication lag is the delay in seconds between a transaction being committed on the primary cluster and it appearing on the read replica.
* **Metric name**: `cloudsync_replica_lag_seconds`
* **Normal range**: < 2.0 seconds
* **Critical range**: > 10.0 seconds

## Root Causes of Delays
1. **Network Latency**: High packet loss or latency (> 150ms) between primary and replica regions.
2. **Cluster Sync Timeouts**: Large bulk writes saturating the sync buffer, causing connection timeouts (`ERR_SYNC_TIMEOUT`).
3. **Write Congestion**: Destination replica unable to write quickly enough due to lower tier performance.

## Conflict Resolution & Recovery Steps
When primary and replica systems drift, conflict resolution strategies must be applied:
* **Last-Write-Wins (LWW)**: Default policy using system timestamps.
* **Manual Merge**: Handled via custom conflict webhooks.

**Resolution Steps**:
1. Check the replication health dashboard to monitor `cloudsync_replica_lag_seconds`.
2. Temporarily pause secondary batch workloads if lag exceeds 30 seconds.
3. Scale up replica write throughput (IOPS) via Admin Console > Clusters > Scale.
4. Verify if sync resumes automatically.
