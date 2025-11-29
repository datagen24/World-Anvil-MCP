"""In-memory cache with TTL expiration and LRU eviction.

This module provides a session-scoped cache for World Anvil API responses with:
- TTL-based expiration (automatic cleanup on access)
- LRU eviction when at capacity
- Pattern-based invalidation for write operations
- Statistics tracking for monitoring

Thread Safety:
    Safe for single-threaded async operations (GIL-protected).
    No explicit locks needed for async/await usage.

Example:
    >>> cache = InMemoryCache(default_ttl=300, max_entries=1000)
    >>> cache.set("world:123", {"name": "Eberron"})
    >>> cache.get("world:123")
    {'name': 'Eberron'}
    >>> cache.invalidate_pattern("world:.*")
    1
"""

from __future__ import annotations

import re
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    """Single cache entry with expiration timestamp.

    Attributes:
        value: Cached data (can be any type).
        expires_at: Unix timestamp when entry expires.
    """

    value: Any
    expires_at: float


class InMemoryCache:
    """In-memory cache with TTL and LRU eviction.

    This cache is designed for session-scoped API response caching with:
    - Automatic expiration after TTL seconds
    - LRU eviction when cache reaches max_entries
    - Pattern-based invalidation for related keys
    - Lazy cleanup (expired entries removed on access)

    Performance:
        - get(): O(1) average
        - set(): O(1) average, O(n) worst case (eviction)
        - invalidate(): O(1)
        - invalidate_pattern(): O(n)
        - Memory: O(max_entries)

    Attributes:
        default_ttl: Default time-to-live in seconds (300 = 5 minutes).
        max_entries: Maximum number of cached entries before LRU eviction.
    """

    def __init__(
        self,
        default_ttl: int = 300,
        max_entries: int = 1000,
    ) -> None:
        """Initialize cache with TTL and capacity limits.

        Args:
            default_ttl: Default expiration time in seconds. Defaults to 300.
            max_entries: Maximum cache entries before LRU eviction. Defaults to 1000.

        Example:
            >>> cache = InMemoryCache(default_ttl=600, max_entries=500)
            >>> cache.stats()
            {'current': 0, 'expired': 0, 'max_entries': 500}
        """
        self._default_ttl = default_ttl
        self._max_entries = max_entries
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()

    def get(self, key: str) -> Any | None:  # noqa: ANN401
        """Retrieve cached value if not expired.

        Automatically removes expired entries and updates LRU access order
        for valid entries.

        Args:
            key: Cache key to retrieve.

        Returns:
            Cached value if found and not expired, None otherwise.

        Example:
            >>> cache.set("article:123", {"title": "Dragons"}, ttl=60)
            >>> cache.get("article:123")
            {'title': 'Dragons'}
            >>> # After 60 seconds...
            >>> cache.get("article:123")
            None
        """
        if key not in self._cache:
            return None

        entry = self._cache[key]
        now = time.time()

        # Check expiration
        if now >= entry.expires_at:
            # Expired, remove and return cache miss
            del self._cache[key]
            return None

        # Valid entry, update LRU order and return value
        self._cache.move_to_end(key)
        return entry.value

    def set(
        self,
        key: str,
        value: Any,  # noqa: ANN401
        ttl: int | None = None,
    ) -> None:
        """Store value in cache with TTL.

        If cache is at capacity and a new key is added, the least recently
        used entry is evicted. Updates to existing keys do not trigger eviction.

        Args:
            key: Cache key to store.
            value: Value to cache (can be any type).
            ttl: Time-to-live in seconds. Uses default_ttl if None.

        Example:
            >>> cache = InMemoryCache(max_entries=2)
            >>> cache.set("a", 1)
            >>> cache.set("b", 2)
            >>> cache.set("c", 3)  # Evicts "a" (LRU)
            >>> cache.get("a")
            None
            >>> cache.get("b")
            2
        """
        # Calculate expiration
        effective_ttl = ttl if ttl is not None else self._default_ttl
        expires_at = time.time() + effective_ttl

        # Evict LRU if at capacity and adding new key
        if len(self._cache) >= self._max_entries and key not in self._cache:
            self._cache.popitem(last=False)  # Remove oldest (first) entry

        # Store entry and mark as most recently used
        self._cache[key] = CacheEntry(value=value, expires_at=expires_at)
        self._cache.move_to_end(key)

    def invalidate(self, key: str) -> None:
        """Remove specific cache entry.

        Args:
            key: Cache key to remove.

        Example:
            >>> cache.set("world:123", {"name": "Eberron"})
            >>> cache.invalidate("world:123")
            >>> cache.get("world:123")
            None
        """
        if key in self._cache:
            del self._cache[key]

    def invalidate_pattern(self, pattern: str) -> int:
        """Remove all keys matching regex pattern.

        This is used for write operations to invalidate related cached data.
        For example, updating an article should invalidate all article list caches.

        Args:
            pattern: Regular expression pattern to match keys.

        Returns:
            Number of entries removed.

        Example:
            >>> cache.set("world:123:articles", [...])
            >>> cache.set("world:123:categories", [...])
            >>> cache.set("user:456", {...})
            >>> cache.invalidate_pattern(r"world:123:.*")
            2
            >>> cache.get("user:456")  # Unaffected
            {...}
        """
        regex = re.compile(pattern)
        keys_to_remove = [key for key in self._cache if regex.match(key)]

        for key in keys_to_remove:
            del self._cache[key]

        return len(keys_to_remove)

    def clear(self) -> None:
        """Clear entire cache.

        Example:
            >>> cache.set("a", 1)
            >>> cache.set("b", 2)
            >>> cache.clear()
            >>> cache.stats()['current']
            0
        """
        self._cache.clear()

    def stats(self) -> dict[str, int]:
        """Return cache statistics.

        Returns:
            Dictionary with:
                - current: Current number of entries (including expired).
                - expired: Number of expired entries pending cleanup.
                - max_entries: Maximum cache capacity.

        Example:
            >>> cache = InMemoryCache(max_entries=1000)
            >>> cache.set("a", 1)
            >>> cache.set("b", 2, ttl=0)  # Immediately expired
            >>> stats = cache.stats()
            >>> stats['current']
            2
            >>> stats['expired']
            1
            >>> stats['max_entries']
            1000
        """
        now = time.time()
        expired_count = sum(1 for entry in self._cache.values() if now >= entry.expires_at)

        return {
            "current": len(self._cache),
            "expired": expired_count,
            "max_entries": self._max_entries,
        }
