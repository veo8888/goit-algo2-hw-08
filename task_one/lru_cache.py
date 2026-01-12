import random
import time


class LRUCache:
    """LRU Cache implementation using doubly linked list and hash map."""

    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        # Dummy head and tail
        self.head = self.Node(0, 0)
        self.tail = self.Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Get value by key. Returns -1 if key doesn't exist."""
        if key in self.cache:
            node = self.cache[key]
            # Move to head (most recently used)
            self._remove(node)
            self._add_to_head(node)
            return node.value
        return -1

    def put(self, key, value):
        """Put key-value pair into cache."""
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_head(node)
        else:
            # Add new
            node = self.Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)

            if len(self.cache) > self.capacity:
                # Remove LRU (tail.prev)
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

    def keys(self):
        """Return all keys in cache."""
        return list(self.cache.keys())


# Initialize global cache
cache = LRUCache(capacity=1000)


def range_sum_no_cache(array, left, right):
    """Calculate sum without caching."""
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    """Update element without caching."""
    array[index] = value


def range_sum_with_cache(array, left, right):
    """Calculate sum with LRU cache."""
    key = (left, right)
    result = cache.get(key)

    if result == -1:  # Cache miss
        result = sum(array[left : right + 1])
        cache.put(key, result)

    return result


def update_with_cache(array, index, value):
    """Update element and invalidate affected cache entries."""
    array[index] = value

    # Invalidate all ranges that contain the updated index
    keys_to_remove = []
    for key in cache.keys():
        left, right = key
        if left <= index <= right:
            keys_to_remove.append(key)

    # Remove invalidated entries
    for key in keys_to_remove:
        cache.cache.pop(key, None)


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    """Generate query list with hot ranges."""
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% queries are Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% are Range
            if random.random() < p_hot:  # 95% are "hot" ranges
                left, right = random.choice(hot)
            else:  # 5% are random ranges
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


def test_without_cache(array, queries):
    """Execute queries without cache."""
    total = 0
    for query in queries:
        if query[0] == "Update":
            _, index, value = query
            update_no_cache(array, index, value)
        else:  # Range
            _, left, right = query
            result = range_sum_no_cache(array, left, right)
            total += result
    return total


def test_with_cache(array, queries):
    """Execute queries with LRU cache."""
    # Reset cache
    global cache
    cache = LRUCache(capacity=1000)

    total = 0
    for query in queries:
        if query[0] == "Update":
            _, index, value = query
            update_with_cache(array, index, value)
        else:  # Range
            _, left, right = query
            result = range_sum_with_cache(array, left, right)
            total += result
    return total


def main():
    # Configuration
    N = 100_000
    Q = 50_000

    print("=== LRU Cache Optimization Demo ===\n")
    print(f"Array size: {N:,}")
    print(f"Number of queries: {Q:,}")
    print(f"Cache capacity: 1,000\n")

    # Generate test data
    print("Generating test data...")
    array_original = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)
    print(f"Generated {len(queries):,} queries\n")

    # Test without cache
    print("Testing without cache...")
    array_no_cache = array_original.copy()
    start_time = time.time()
    result_no_cache = test_without_cache(array_no_cache, queries)
    time_no_cache = time.time() - start_time

    # Test with cache
    print("Testing with LRU cache...")
    array_with_cache = array_original.copy()
    start_time = time.time()
    result_with_cache = test_with_cache(array_with_cache, queries)
    time_with_cache = time.time() - start_time

    # Results
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"No Cache : {time_no_cache:6.2f} s")
    print(
        f"LRU Cache  : {time_with_cache:6.2f} s  (Speedup:{time_no_cache/time_with_cache:.1f}x)"
    )
    print("=" * 50)

    # Verify correctness
    if result_no_cache == result_with_cache:
        print("\n✓ Results match - implementation is correct!")
    else:
        print(f"\n✗ Results mismatch: {result_no_cache} vs {result_with_cache}")


if __name__ == "__main__":
    main()
