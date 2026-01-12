import random
from typing import Dict
import time
from collections import deque


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        """
        Initialize rate limiter with sliding window algorithm.

        Args:
            window_size: Size of the time window in seconds (default: 10)
            max_requests: Maximum number of requests allowed in the window (default: 1)
        """
        self.window_size = window_size
        self.max_requests = max_requests
        # Dictionary to store deque of timestamps for each user
        self.user_windows: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """
        Clean up expired requests from the user's window.

        Args:
            user_id: User identifier
            current_time: Current timestamp
        """
        if user_id not in self.user_windows:
            return

        window = self.user_windows[user_id]
        cutoff_time = current_time - self.window_size

        # Remove all timestamps older than window_size
        while window and window[0] <= cutoff_time:
            window.popleft()

        # If window is empty, remove user from dictionary
        if not window:
            del self.user_windows[user_id]

    def can_send_message(self, user_id: str) -> bool:
        """
        Check if user can send a message in the current time window.

        Args:
            user_id: User identifier

        Returns:
            True if user can send message, False otherwise
        """
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        # First message from user is always allowed
        if user_id not in self.user_windows:
            return True

        # Check if user has reached the limit
        return len(self.user_windows[user_id]) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """
        Record a new message and update user's history.

        Args:
            user_id: User identifier

        Returns:
            True if message was recorded, False if rate limit exceeded
        """
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        # Check if user can send message
        if not self.can_send_message(user_id):
            return False

        # Initialize window for new user
        if user_id not in self.user_windows:
            self.user_windows[user_id] = deque()

        # Record the message
        self.user_windows[user_id].append(current_time)
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Calculate time until next message is allowed.

        Args:
            user_id: User identifier

        Returns:
            Time in seconds until next message is allowed (0 if can send now)
        """
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        # User can send immediately if not in dictionary or below limit
        if user_id not in self.user_windows:
            return 0.0

        window = self.user_windows[user_id]

        if len(window) < self.max_requests:
            return 0.0

        # Calculate time until oldest message expires
        oldest_message_time = window[0]
        time_until_expired = (oldest_message_time + self.window_size) - current_time
        return max(0.0, time_until_expired)


# Demo
def test_rate_limiter():
    # Initialize rate limiter: 10-second window, 1 request limit
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Simulate incoming message stream (sequential IDs 1-20)
    print("\n=== Simulating Message Stream ===")
    for message_id in range(1, 11):
        # Simulate different users (IDs 1-5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (wait {wait_time:.1f} s)'}"
        )

        # Slight delay between messages for realism
        # Random delay from 0.1 to 1.0 seconds
        time.sleep(random.uniform(0.1, 1.0))

    # Wait for the window to clear
    print("\nWaiting for 4 seconds...")
    time.sleep(4)

    print("\n=== New Message Batch After Delay ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (wait {wait_time:.1f} s)'}"
        )
        # Random delay from 0.1 to 1.0 seconds
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
