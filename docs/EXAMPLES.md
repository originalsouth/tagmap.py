# TagMap Usage Examples

Practical examples demonstrating common use cases for TagMap.

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

Track team member skills and query by skill:

```python
team = tagmap.TagMap({
    "alice": ["python", "typescript", "backend"],
    "bob": ["cpp", "rust", "backend"],
    "carol": ["ux", "ui", "design"],
    "dave": ["devops", "kubernetes", "aws"],
})

# Find team members with specific skill
python_devs = team.query("python")        # ['alice']
backend_devs = team.query("backend")      # ['alice', 'bob']

# Find people with both Python AND backend
python_backend = team.query("python", "backend")  # ['alice']

# Find people with Python OR TypeScript
frontend_or_python = team.query_any("typescript", "python")  # ['alice']

# Count
num_backend = team.count(["backend"])     # 2
```

---

## Example 2: Content Classification

Classify and query blog posts by multiple tags:

```python
posts = tagmap.TagMap()

posts["post_1"] = ["python", "tutorial", "beginner"]
posts["post_2"] = ["python", "advanced", "performance"]
posts["post_3"] = ["javascript", "tutorial", "beginner"]
posts["post_4"] = ["devops", "kubernetes", "advanced"]

# Find tutorials
tutorials = posts.query("tutorial")                           # ['post_1', 'post_3']

# Find beginner Python tutorials
beginner_python = posts.query("python", "tutorial", "beginner")  # ['post_1']

# Find beginner OR intermediate content
easy_posts = posts.query_any("beginner", "intermediate")     # ['post_1', 'post_3']

# Count advanced posts
advanced_count = posts.count_any(["advanced"])               # 2
```

---

## Example 3: Feature Flags

Track which features are deployed to which environments:

```python
features = tagmap.TagMap({
    "auth_v2": ["production", "staging", "beta"],
    "new_dashboard": ["staging", "beta"],
    "payment_api": ["production"],
    "dark_mode": ["beta"],
})

# Features in production
prod_features = features.query("production")                  # ['auth_v2', 'payment_api']

# Features available for testing (staging OR beta)
testing_features = features.query_any("staging", "beta")     # ['auth_v2', 'new_dashboard', 'dark_mode']

# Features in both staging AND beta
well_tested = features.query("staging", "beta")              # ['auth_v2']

# Add feature to beta
features.add_tag("payment_api", "beta")

# Count
prod_count = features.count(["production"])                  # 2
```

---

## Example 4: Document Classification

Classify documents by type, sensitivity, and department:

```python
docs = tagmap.TagMap()

docs["report_2024"] = ["financial", "confidential", "finance"]
docs["policy_handbook"] = ["hr", "public", "general"]
docs["source_code"] = ["technical", "proprietary", "engineering"]
docs["public_data"] = ["data", "public", "marketing"]

# Find confidential documents
confidential = docs.query("confidential")                     # ['report_2024']

# Find public documents
public = docs.query("public")                                 # ['policy_handbook', 'public_data']

# Find technical documents that are NOT public
technical_private = [
    key for key in docs
    if "technical" in docs[key] and "public" not in docs[key]
]  # ['source_code']

# Count proprietary documents
proprietary_count = docs.count(["proprietary"])              # 1
```

---

## Example 5: User Filtering

Filter users based on status and subscription:

```python
users = tagmap.TagMap({
    "user_1": ["premium", "active", "verified"],
    "user_2": ["free", "active", "unverified"],
    "user_3": ["premium", "inactive", "verified"],
    "user_4": ["free", "inactive", "unverified"],
})

# Active users
active_users = users.query("active")                          # ['user_1', 'user_2']

# Upgrade-eligible (premium AND active AND verified)
eligible = users.query("premium", "active", "verified")      # ['user_1']

# Remove inactive users
users.erase_where(["inactive"])

# Keep only active premium users
kept = users.retain_where(["active", "premium"])
```

---

## Example 6: Tag Management

Dynamically update tags based on events:

```python
devices = tagmap.TagMap()

# Register device
devices["device_001"] = ["online", "trusted"]

# Device goes offline
devices.discard_tag("device_001", "online")
devices.add_tag("device_001", "offline")

# Add multiple tags
devices.add_tags("device_001", ["maintenance", "quarantine"])

# Check status
is_trusted = devices.has_tag("device_001", "trusted")
is_online = devices.has_tag("device_001", "online")

# Remove from quarantine
devices.discard_tag("device_001", "quarantine")

# Find devices needing maintenance
maintenance_devices = devices.query("maintenance")
```

---

## Example 7: Bulk Operations

Apply operations to multiple entries:

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

# Remove deprecated services
services.erase_where(["deprecated"])

# Get all tags
all_tags = services.tags()
```

---

## Example 8: Reporting

Generate reports from tagged data:

```python
users = tagmap.TagMap({
    "john": ["premium", "active", "us"],
    "jane": ["premium", "active", "uk"],
    "bob": ["free", "inactive", "us"],
    "alice": ["premium", "inactive", "eu"],
})

# Summary
print(f"Total users: {len(users)}")
print(f"Premium users: {users.count(['premium'])}")
print(f"Active users: {users.count(['active'])}")
print(f"US-based users: {users.count(['us'])}")
print(f"Active premium users: {users.count(['active', 'premium'])}")

# Segment by region
regions = {
    "us": users.query("us"),
    "uk": users.query("uk"),
    "eu": users.query("eu"),
}

# Segment by status
status = {
    "active": users.query("active"),
    "inactive": users.query("inactive"),
}
```

---

## Performance Tips

Use TagMap methods for efficient querying:

```python
# Efficient: use built-in query
results = m.query("dev", "python")

# Less efficient: filter in Python
results = [k for k, v in m.items() if "dev" in v and "python" in v]
```

Batch tag operations:

```python
# Efficient: single operation
m.add_tags("alice", ["tag1", "tag2", "tag3"])

# Less efficient: multiple operations
m.add_tag("alice", "tag1")
m.add_tag("alice", "tag2")
m.add_tag("alice", "tag3")
```

Use `count()` instead of `len(query())`:

```python
# Efficient
count = m.count(["dev"])

# Less efficient
count = len(m.query("dev"))
```
