# TagMap Usage Examples

This document provides practical examples of using TagMap in real-world scenarios.

## Basic Setup

```python
import tagmap

# Create an empty TagMap
m = tagmap.TagMap()

# Add entries with tags
m["alice"] = {"dev", "python"}
m["bob"] = {"dev", "cpp"}
m["carol"] = {"design", "python"}
m["dave"] = {"ops", "devops"}
```

---

## Example 1: Team Member Skills

Manage team members and their skills:

```python
team = tagmap.TagMap({
    "alice": ["python", "typescript", "backend"],
    "bob": ["cpp", "rust", "backend"],
    "carol": ["ux", "ui", "design"],
    "dave": ["devops", "kubernetes", "aws"],
})

# Find all Python developers
python_devs = team.query("python")
print(python_devs)  # ['alice']

# Find all backend developers
backend_devs = team.query("backend")
print(backend_devs)  # ['alice', 'bob']

# Find people with either Python or TypeScript skills
frontend_or_python = team.query_any("typescript", "python")
print(frontend_or_python)  # ['alice']

# Count backend developers
num_backend = team.count(["backend"])
print(num_backend)  # 2

# Find someone who knows both Python and backend
python_backend = team.query("python", "backend")
print(python_backend)  # ['alice']
```

---

## Example 2: Content Tagging System

Organize blog posts with multiple tags:

```python
posts = tagmap.TagMap()

# Add blog posts with tags
posts["post_1"] = ["python", "tutorial", "beginner"]
posts["post_2"] = ["python", "advanced", "performance"]
posts["post_3"] = ["javascript", "tutorial", "beginner"]
posts["post_4"] = ["devops", "kubernetes", "advanced"]

# Find all tutorials
tutorials = posts.query("tutorial")
# Result: ['post_1', 'post_3']

# Find beginner-friendly Python tutorials
beginner_python = posts.query("python", "tutorial", "beginner")
# Result: ['post_1']

# Find posts for beginners OR intermediate
easy_posts = posts.query_any("beginner", "intermediate")
# Result: ['post_1', 'post_3']

# Count advanced posts
advanced_count = posts.count_any(["advanced"])
# Result: 2
```

---

## Example 3: Feature Flags & Deployment

Track which features are deployed to which environments:

```python
features = tagmap.TagMap({
    "auth_v2": ["production", "staging", "beta"],
    "new_dashboard": ["staging", "beta"],
    "payment_api": ["production"],
    "dark_mode": ["beta"],
})

# What's deployed to production?
prod_features = features.query("production")
# Result: ['auth_v2', 'payment_api']

# What's available for testing (staging or beta)?
testing_features = features.query_any("staging", "beta")
# Result: ['auth_v2', 'new_dashboard', 'dark_mode']

# What's in both staging AND beta? (already tested)
well_tested = features.query("staging", "beta")
# Result: ['auth_v2']

# Add a feature to beta
features.add_tag("payment_api", "beta")

# Count production features
prod_count = features.count(["production"])
# Result: 2
```

---

## Example 4: Document Classification

Classify documents by type, sensitivity, and department:

```python
docs = tagmap.TagMap()

# Add documents with multiple classification tags
docs["report_2024"] = ["financial", "confidential", "finance"]
docs["policy_handbook"] = ["hr", "public", "general"]
docs["source_code"] = ["technical", "proprietary", "engineering"]
docs["public_data"] = ["data", "public", "marketing"]

# Find all confidential documents
confidential = docs.query("confidential")
# Result: ['report_2024']

# Find all public documents
public = docs.query("public")
# Result: ['policy_handbook', 'public_data']

# Find technical documents that are NOT public
technical_private = [
    key for key in docs
    if "technical" in docs[key] and "public" not in docs[key]
]
# Result: ['source_code']

# Count proprietary documents
proprietary_count = docs.count(["proprietary"])
# Result: 1
```

---

## Example 5: Conditional Filtering

Filter data based on tag combinations:

```python
users = tagmap.TagMap({
    "user_1": ["premium", "active", "verified"],
    "user_2": ["free", "active", "unverified"],
    "user_3": ["premium", "inactive", "verified"],
    "user_4": ["free", "inactive", "unverified"],
})

# Send notification to active users
active_users = users.query("active")
# Result: ['user_1', 'user_2']

# Upgrade eligible users (premium AND active AND verified)
eligible = users.query("premium", "active", "verified")
# Result: ['user_1']

# Deactivate old premium users
old_premium = users.find_any(["premium", "old"])

# Remove inactive users
users.erase_where(["inactive"])
# Removes: ['user_3', 'user_4']

# Retain only active AND premium users
kept = users.retain_where(["active", "premium"])
# After this: only 'user_1' remains
```

---

## Example 6: Dynamic Tag Updates

Manage tags dynamically based on events:

```python
devices = tagmap.TagMap()

# Register a device
devices["device_001"] = ["online", "trusted"]

# Device goes offline
devices.discard_tag("device_001", "online")
devices.add_tag("device_001", "offline")

# Multiple updates
devices.add_tags("device_001", ["maintenance", "quarantine"])

# Check device status
is_trusted = devices.has_tag("device_001", "trusted")
is_online = devices.has_tag("device_001", "online")

# Remove from quarantine after inspection
devices.discard_tag("device_001", "quarantine")

# Get all devices needing maintenance
maintenance_devices = devices.query("maintenance")
```

---

## Example 7: Bulk Operations

Perform operations on multiple entries at once:

```python
services = tagmap.TagMap({
    "api_auth": ["backend", "critical", "v2"],
    "api_users": ["backend", "critical", "v1"],
    "api_posts": ["backend", "v1"],
    "frontend_app": ["frontend", "v2"],
})

# Deprecate all v1 services
old_services = services.query("v1")
for service in old_services:
    services.add_tag(service, "deprecated")

# Migrate old backend services
backend_v1 = services.query("backend", "v1")
for service in backend_v1:
    services.remove_tag(service, "v1")
    services.add_tag(service, "v2")
    services.add_tag(service, "migrated")

# Remove all deprecated services
services.erase_where(["deprecated"])

# Get all tags in use
all_tags = services.tags()
# Result: ['backend', 'critical', 'v2', 'frontend', 'migrated']
```

---

## Example 8: Reporting & Analytics

Generate reports from tagged data:

```python
users = tagmap.TagMap({
    "john": ["premium", "active", "us"],
    "jane": ["premium", "active", "uk"],
    "bob": ["free", "inactive", "us"],
    "alice": ["premium", "inactive", "eu"],
})

# Generate report
print(f"Total users: {len(users)}")
print(f"Premium users: {users.count(['premium'])}")
print(f"Active users: {users.count(['active'])}")
print(f"US-based users: {users.count(['us'])}")
print(f"Active premium users: {users.count(['active', 'premium'])}")

# Segment analysis
regions = {
    "us": users.query("us"),
    "uk": users.query("uk"),
    "eu": users.query("eu"),
}

status = {
    "active": users.query("active"),
    "inactive": users.query("inactive"),
}

# Create a report
for region, users_in_region in regions.items():
    print(f"\n{region.upper()} ({len(users_in_region)} users):")
    for user in users_in_region:
        print(f"  {user}: {users[user]}")
```

---

## Performance Tips

```python
# Prefer query() over filtering in Python
# FAST ✓
results = m.query("dev", "python")

# SLOW ✗
results = [k for k, v in m.items() if "dev" in v and "python" in v]

# Batch operations are efficient
m.add_tags("alice", ["tag1", "tag2", "tag3"])  # Single operation

# Use count() for counting instead of len(query())
# FAST ✓
count = m.count(["dev"])

# SLOW ✗
count = len(m.query("dev"))

# Update TagMap once if making multiple changes to the same entry
m["alice"] = {"tag1", "tag2"}  # Replaces all tags
m.add_tag("alice", "tag3")  # Adds one tag
```
