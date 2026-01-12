# goit-algo2-hw-08

## 🗂️ task_one: LRU Cache Optimization

### Implementation

- **File**: [lru_cache.py](lru_cache.py)
- **Features**:
  - Complete LRU Cache implementation using doubly linked list and hash map
  - Array size: 100,000 elements
  - Query count: 50,000 queries
  - Cache capacity: 1,000 entries
  - Two types of queries: Range sum (97%) and Update (3%)
  - Hot ranges: 95% of queries target 30 pre-defined popular ranges

### Key Functions

- `range_sum_no_cache()` - calculates sum without caching
- `update_no_cache()` - updates element without caching
- `range_sum_with_cache()` - uses LRU cache for range sums
- `update_with_cache()` - updates element and invalidates affected cache entries

### 🚀 Running on Windows (PowerShell or CMD)

1. Navigate to the project directory

```bash
cd path/to/task_one
```

2. Running Task 1

```bash
python lru_cache.py
```

### Example Output

```
=== LRU Cache Optimization Demo ===

Array size: 100,000
Number of queries: 50,000
Cache capacity: 1,000

Generating test data...
Generated 50,000 queries

Testing without cache...
Testing with LRU cache...

==================================================
RESULTS
==================================================
No Cache :   7.78 s
LRU Cache  :   2.65 s  (Speedup:2.9x)
==================================================

✓ Results match - implementation is correct!
```

---
