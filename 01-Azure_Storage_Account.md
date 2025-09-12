# Azure Storage Account – Data Engineer Notes

## 📌 What is a Storage Account?
- A **Storage Account** is the **root namespace** in Azure for storing data objects.  
- Provides a **unique endpoint** for accessing Azure storage services.  
- All data in Azure Storage (blobs, files, queues, tables) lives inside a storage account.  

**Example Endpoint**:  
```
https://mystorageacct.blob.core.windows.net
```

---

## 📦 Storage Services in a Storage Account
A storage account can provide access to **four core services**:

1. **Blob Service**
   - Stores unstructured object data (files, logs, images, backups).
   - Equivalent to **AWS S3**.
   - Can be used as:
     - **Blob Storage** (flat namespace)  
     - **ADLS Gen2** (with hierarchical namespace enabled → HDFS-like)  

2. **File Service (Azure Files)**
   - Fully managed **file shares** in the cloud.
   - Supports SMB/NFS → can be mounted by VMs or on-prem servers.

3. **Queue Service**
   - Message queues for asynchronous communication.
   - Similar to **AWS SQS**.

4. **Table Service**
   - NoSQL key-value database.
   - Similar to **AWS DynamoDB (lite version)**.
   - Best for fast lookups, not analytics.

---

## 🔑 Authentication
- Each storage account has **two Access Keys (Key1, Key2)**.
- These keys act as **root credentials** → full access to all services.
- Best practice:
  - Don’t share keys directly.
  - Use **Azure AD / Managed Identity** where possible.
  - If needed, generate **SAS Tokens**:
    - Scoped (blob, container, service).
    - Limited permissions (read, write, list, delete).
    - Time-bound (start and expiry date).
    - Safer than handing out access keys.

---

## 🔄 Replication Options
Replication ensures **durability and availability** of data.

| Option | Copies | Location | Protects Against | Cost | Use Case |
|--------|--------|----------|------------------|------|----------|
| **LRS** (Locally Redundant Storage) | 3 | One datacenter | Disk/server failure | 💲 Low | Dev/test, non-critical |
| **ZRS** (Zone-Redundant Storage) | 3 | Across zones (same region) | Zone/datacenter outage | 💲💲 Medium | Prod workloads |
| **GRS** (Geo-Redundant Storage) | 6 | Primary region + paired region | Regional disaster | 💲💲💲 High | Mission-critical |
| **RA-GRS** (Read-Access GRS) | 6 | Primary + paired region (readable) | Regional disaster + read in secondary | 💲💲💲 High | Global read + DR |

---

## 📂 Structure
```
Storage Account (root)
│
├── Container (folder for blobs)
│   ├── Blob (object/file)
│   └── Blob (object/file)
│
├── File Share
├── Queue
└── Table
```

- **Blob storage** = flat namespace. Folders are virtual.  
- **ADLS Gen2 (HNS enabled)** = true directories + POSIX ACLs.  

---

## 🌡️ Access Tiers (Blob Storage)
Control cost vs. performance.

- **Hot** → Frequently accessed. High storage cost, low access cost.  
- **Cool** → Infrequently accessed (≥ 30 days). Lower storage cost, higher access cost.  
- **Archive** → Rarely accessed (≥ 180 days). Lowest storage cost, data must be rehydrated to access.  

---

## ✅ Blob vs ADLS
| Feature | Blob Storage | ADLS Gen2 |
|---------|--------------|-----------|
| Namespace | Flat | Hierarchical |
| Security | Container-level RBAC | POSIX ACLs + RBAC |
| Rename/Move | Copy + Delete | Atomic operations |
| Use Case | Backups, logs, app files | Data lakes, ETL, analytics |

---

## 🔎 Key Takeaways for Data Engineers
- **Storage Account = root container**, like AWS S3 bucket.  
- **Container = folder** for organizing blobs.  
- **Blob = actual file/object**.  
- Enable **Hierarchical Namespace (HNS)** if building a **Data Lake** → that makes it **ADLS Gen2**.  
- Use **SAS tokens** or **Azure AD** instead of access keys.  
- Pick replication based on **criticality** (LRS vs ZRS vs GRS).  
- Optimize costs with **Hot / Cool / Archive tiers**.  

---