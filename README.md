# goit-algo2-hw-08

## 🗂️ task_one: LRU Cache Optimization

### Implementation

- **File**: [lru_cache.py](task_one/lru_cache.py)
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

### 🚀 Running Task 1 on Windows (PowerShell or CMD)

1. Navigate to the project directory

```bash
cd path/to/task_one
```

2. Running Task 1

```bash
python lru_cache.py
```

### 🖥️ Example Output

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

## 🗂️ Task-2 Sliding Window Rate Limiter

### Implementation

- **File**: [rate_limiter.py](task_two/rate_limiter.py)
- **Features**:
  - Sliding Window algorithm for precise time interval control
  - Window size: 10 seconds
  - Maximum messages per window: 1
  - Automatic cleanup of expired messages
  - User removal when window is empty

### Key Methods

- `_cleanup_window()` - removes expired requests and updates active window
- `can_send_message()` - checks if message can be sent in current window
- `record_message()` - records new message and updates user history
- `time_until_next_allowed()` - calculates wait time until next allowed message

### 🚀 Running Task 2 on Windows (PowerShell or CMD)

1. Navigate to the project directory

```bash
cd path/to/task_two
```

2. Running Task 2

```bash
python rate_limiter.py
```

### Test Scenario

- 20 messages from 5 different users
- First 10 messages with random delays (0.1-1 second)
- 4-second wait period
- Another 10 messages with random delays

### Expected Behavior

1. First message from each user is always allowed (✓)
2. Second message within 10 seconds is blocked (×)
3. After 10+ seconds from first message, user can send again
4. Wait time is calculated based on oldest message in window

### 🖥️ Example Output

```
=== Simulating Message Stream ===
Message  1 | User 2 | ✓
Message  2 | User 3 | ✓
Message  3 | User 4 | ✓
Message  4 | User 5 | ✓
Message  5 | User 1 | ✓
Message  6 | User 2 | × (wait 6.9 s)
Message  7 | User 3 | × (wait 6.3 s)
Message  8 | User 4 | × (wait 6.6 s)
Message  9 | User 5 | × (wait 6.4 s)
Message 10 | User 1 | × (wait 6.7 s)

Waiting for 4 seconds...

=== New Message Batch After Delay ===
Message 11 | User 2 | × (wait 0.0 s)
Message 12 | User 3 | ✓
Message 13 | User 4 | × (wait 0.6 s)
Message 14 | User 5 | × (wait 0.5 s)
Message 15 | User 1 | × (wait 0.9 s)
Message 16 | User 2 | ✓
Message 17 | User 3 | × (wait 7.7 s)
Message 18 | User 4 | ✓
Message 19 | User 5 | ✓
Message 20 | User 1 | ✓
```

---

## Dependencies

- Python 3.7+
- Standard library only (no external packages needed)

## ✔ Notes

- Results may vary slightly due to random query generation and system performance
- Cache invalidation in Task 1 uses linear scan (as specified in requirements)
