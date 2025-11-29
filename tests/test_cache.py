"""Tests for in-memory cache with TTL expiration and LRU eviction.

Tests InMemoryCache and CacheEntry components including:
- Basic get/set operations
- TTL expiration and lazy cleanup
- LRU eviction when at capacity
- Pattern-based invalidation
- Statistics tracking
"""

import time
from unittest.mock import patch

import pytest

from world_anvil_mcp.cache import CacheEntry, InMemoryCache


class TestCacheEntry:
    """Tests for CacheEntry dataclass."""

    @pytest.mark.unit
    def test_cache_entry_creation(self) -> None:
        """Test creating a CacheEntry with value and expiration."""
        # Arrange
        expires_at = time.time() + 300

        # Act
        entry = CacheEntry(value={"key": "value"}, expires_at=expires_at)

        # Assert
        assert entry.value == {"key": "value"}
        assert entry.expires_at == expires_at

    @pytest.mark.unit
    def test_cache_entry_with_any_value_type(self) -> None:
        """Test CacheEntry stores any value type."""
        # Arrange
        expires_at = time.time() + 300

        # Act & Assert - string
        entry_str = CacheEntry(value="test", expires_at=expires_at)
        assert entry_str.value == "test"

        # Act & Assert - int
        entry_int = CacheEntry(value=42, expires_at=expires_at)
        assert entry_int.value == 42

        # Act & Assert - list
        entry_list = CacheEntry(value=[1, 2, 3], expires_at=expires_at)
        assert entry_list.value == [1, 2, 3]

        # Act & Assert - None
        entry_none = CacheEntry(value=None, expires_at=expires_at)
        assert entry_none.value is None


class TestInMemoryCacheBasics:
    """Tests for basic InMemoryCache get/set operations."""

    @pytest.mark.unit
    def test_cache_initialization(self) -> None:
        """Test cache initializes with correct defaults."""
        # Act
        cache = InMemoryCache()

        # Assert
        assert cache._default_ttl == 300
        assert cache._max_entries == 1000
        assert len(cache._cache) == 0

    @pytest.mark.unit
    def test_cache_initialization_with_custom_values(self) -> None:
        """Test cache initializes with custom TTL and max entries."""
        # Act
        cache = InMemoryCache(default_ttl=600, max_entries=500)

        # Assert
        assert cache._default_ttl == 600
        assert cache._max_entries == 500

    @pytest.mark.unit
    def test_cache_set_and_get(self) -> None:
        """Test basic set and get operations."""
        # Arrange
        cache = InMemoryCache()

        # Act
        cache.set("key1", {"name": "test"})
        result = cache.get("key1")

        # Assert
        assert result == {"name": "test"}

    @pytest.mark.unit
    def test_cache_get_nonexistent_key(self) -> None:
        """Test get returns None for nonexistent key."""
        # Arrange
        cache = InMemoryCache()

        # Act
        result = cache.get("nonexistent")

        # Assert
        assert result is None

    @pytest.mark.unit
    def test_cache_set_overwrites_existing_key(self) -> None:
        """Test set overwrites value for existing key."""
        # Arrange
        cache = InMemoryCache()
        cache.set("key1", "value1")

        # Act
        cache.set("key1", "value2")
        result = cache.get("key1")

        # Assert
        assert result == "value2"

    @pytest.mark.unit
    def test_cache_set_various_types(self) -> None:
        """Test cache stores various value types."""
        # Arrange
        cache = InMemoryCache()

        # Act & Assert - dict
        cache.set("dict_key", {"a": 1})
        assert cache.get("dict_key") == {"a": 1}

        # Act & Assert - list
        cache.set("list_key", [1, 2, 3])
        assert cache.get("list_key") == [1, 2, 3]

        # Act & Assert - string
        cache.set("str_key", "test_string")
        assert cache.get("str_key") == "test_string"

        # Act & Assert - int
        cache.set("int_key", 42)
        assert cache.get("int_key") == 42

        # Act & Assert - None
        cache.set("none_key", None)
        assert cache.get("none_key") is None

    @pytest.mark.unit
    def test_cache_invalidate(self) -> None:
        """Test invalidate removes specific key."""
        # Arrange
        cache = InMemoryCache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        # Act
        cache.invalidate("key1")

        # Assert
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"

    @pytest.mark.unit
    def test_cache_invalidate_nonexistent_key(self) -> None:
        """Test invalidate handles nonexistent key gracefully."""
        # Arrange
        cache = InMemoryCache()

        # Act & Assert - no error
        cache.invalidate("nonexistent")
        assert cache.get("nonexistent") is None

    @pytest.mark.unit
    def test_cache_clear(self) -> None:
        """Test clear removes all entries."""
        # Arrange
        cache = InMemoryCache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        # Act
        cache.clear()

        # Assert
        assert cache.get("key1") is None
        assert cache.get("key2") is None
        assert cache.get("key3") is None


class TestInMemoryCacheTTL:
    """Tests for TTL expiration and lazy cleanup."""

    @pytest.mark.unit
    def test_cache_ttl_expiration(self) -> None:
        """Test entries expire after TTL."""
        # Arrange
        cache = InMemoryCache(default_ttl=1)

        # Act
        cache.set("expiring_key", "value")
        time.sleep(1.1)
        result = cache.get("expiring_key")

        # Assert
        assert result is None

    @pytest.mark.unit
    def test_cache_custom_ttl(self) -> None:
        """Test custom TTL overrides default."""
        # Arrange
        cache = InMemoryCache(default_ttl=300)

        # Act
        cache.set("short_ttl", "value", ttl=1)
        time.sleep(1.1)
        result = cache.get("short_ttl")

        # Assert
        assert result is None

    @pytest.mark.unit
    def test_cache_ttl_zero_expires_immediately(self) -> None:
        """Test TTL=0 expires immediately."""
        # Arrange
        cache = InMemoryCache()

        # Act
        cache.set("immediate", "value", ttl=0)
        time.sleep(0.01)
        result = cache.get("immediate")

        # Assert
        assert result is None

    @pytest.mark.unit
    def test_cache_valid_entry_before_ttl(self) -> None:
        """Test valid entry is returned before TTL expires."""
        # Arrange
        cache = InMemoryCache(default_ttl=10)

        # Act
        cache.set("valid_key", "value")
        time.sleep(0.1)
        result = cache.get("valid_key")

        # Assert
        assert result == "value"

    @pytest.mark.unit
    def test_cache_lazy_cleanup_on_get(self) -> None:
        """Test expired entries are cleaned up on access."""
        # Arrange
        cache = InMemoryCache(default_ttl=1)
        cache.set("exp1", "val1", ttl=1)
        cache.set("exp2", "val2", ttl=1)
        cache.set("persist", "val3", ttl=10)

        # Act
        time.sleep(1.1)
        cache.get("exp1")
        stats = cache.stats()

        # Assert - expired entries removed on access
        assert cache.get("exp1") is None
        assert cache.get("exp2") is None
        assert cache.get("persist") == "val3"

    @pytest.mark.unit
    def test_cache_stats_tracks_expired(self) -> None:
        """Test stats correctly count expired entries."""
        # Arrange
        cache = InMemoryCache()
        cache.set("key1", "val1", ttl=1)
        cache.set("key2", "val2", ttl=10)

        # Act
        time.sleep(1.1)
        stats = cache.stats()

        # Assert - both entries present, one expired
        assert stats["current"] == 2
        assert stats["expired"] == 1


class TestInMemoryCacheLRU:
    """Tests for LRU eviction when at capacity."""

    @pytest.mark.unit
    def test_cache_lru_eviction_at_capacity(self) -> None:
        """Test LRU eviction when adding beyond max_entries."""
        # Arrange
        cache = InMemoryCache(max_entries=2)
        cache.set("a", 1)
        cache.set("b", 2)

        # Act - adding third entry should evict "a" (oldest)
        cache.set("c", 3)

        # Assert
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    @pytest.mark.unit
    def test_cache_lru_eviction_sequence(self) -> None:
        """Test LRU eviction follows FIFO order."""
        # Arrange
        cache = InMemoryCache(max_entries=3)

        # Act - set 5 entries in order
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache.set("d", 4)  # Evicts a
        cache.set("e", 5)  # Evicts b

        # Assert
        assert cache.get("a") is None
        assert cache.get("b") is None
        assert cache.get("c") == 3
        assert cache.get("d") == 4
        assert cache.get("e") == 5

    @pytest.mark.unit
    def test_cache_lru_update_moves_to_end(self) -> None:
        """Test accessing entry updates LRU order."""
        # Arrange
        cache = InMemoryCache(max_entries=2)
        cache.set("a", 1)
        cache.set("b", 2)

        # Act - access "a" to move it to end
        cache.get("a")

        # Now add "c" - should evict "b" not "a"
        cache.set("c", 3)

        # Assert
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3

    @pytest.mark.unit
    def test_cache_lru_update_existing_no_eviction(self) -> None:
        """Test updating existing key doesn't trigger eviction."""
        # Arrange
        cache = InMemoryCache(max_entries=2)
        cache.set("a", 1)
        cache.set("b", 2)

        # Act - update existing key
        cache.set("a", 1)

        # Should not evict
        assert len(cache._cache) == 2
        assert cache.get("a") == 1
        assert cache.get("b") == 2

    @pytest.mark.unit
    def test_cache_lru_single_entry_at_capacity(self) -> None:
        """Test LRU with single entry max."""
        # Arrange
        cache = InMemoryCache(max_entries=1)

        # Act
        cache.set("a", 1)
        cache.set("b", 2)

        # Assert
        assert cache.get("a") is None
        assert cache.get("b") == 2


class TestInMemoryCachePatternInvalidation:
    """Tests for pattern-based key invalidation."""

    @pytest.mark.unit
    def test_invalidate_pattern_basic(self) -> None:
        """Test invalidate_pattern matches and removes keys."""
        # Arrange
        cache = InMemoryCache()
        cache.set("world:123:articles", [])
        cache.set("world:123:categories", [])
        cache.set("user:456", {})

        # Act
        removed = cache.invalidate_pattern(r"world:123:.*")

        # Assert
        assert removed == 2
        assert cache.get("world:123:articles") is None
        assert cache.get("world:123:categories") is None
        assert cache.get("user:456") == {}

    @pytest.mark.unit
    def test_invalidate_pattern_no_matches(self) -> None:
        """Test invalidate_pattern returns 0 for no matches."""
        # Arrange
        cache = InMemoryCache()
        cache.set("key1", "val1")
        cache.set("key2", "val2")

        # Act
        removed = cache.invalidate_pattern(r"nonexistent:.*")

        # Assert
        assert removed == 0
        assert cache.get("key1") == "val1"
        assert cache.get("key2") == "val2"

    @pytest.mark.unit
    def test_invalidate_pattern_exact_match(self) -> None:
        """Test invalidate_pattern with exact match regex."""
        # Arrange
        cache = InMemoryCache()
        cache.set("exact_key", "value1")
        cache.set("other_key", "value2")

        # Act
        removed = cache.invalidate_pattern(r"exact_key")

        # Assert
        assert removed == 1
        assert cache.get("exact_key") is None
        assert cache.get("other_key") == "value2"

    @pytest.mark.unit
    def test_invalidate_pattern_wildcard(self) -> None:
        """Test invalidate_pattern with wildcard matching."""
        # Arrange
        cache = InMemoryCache()
        cache.set("article:1", "val")
        cache.set("article:2", "val")
        cache.set("article:3", "val")
        cache.set("world:1", "val")

        # Act
        removed = cache.invalidate_pattern(r"article:.*")

        # Assert
        assert removed == 3
        assert cache.get("article:1") is None
        assert cache.get("article:2") is None
        assert cache.get("article:3") is None
        assert cache.get("world:1") == "val"

    @pytest.mark.unit
    def test_invalidate_pattern_partial_match(self) -> None:
        """Test invalidate_pattern with partial string patterns."""
        # Arrange
        cache = InMemoryCache()
        cache.set("world:123:data", "val1")
        cache.set("world:124:data", "val2")
        cache.set("world:999:data", "val3")

        # Act
        removed = cache.invalidate_pattern(r"world:12[34]:data")

        # Assert
        assert removed == 2
        assert cache.get("world:123:data") is None
        assert cache.get("world:124:data") is None
        assert cache.get("world:999:data") == "val3"

    @pytest.mark.unit
    def test_invalidate_pattern_returns_count(self) -> None:
        """Test invalidate_pattern returns correct count."""
        # Arrange
        cache = InMemoryCache()
        for i in range(10):
            cache.set(f"key:{i}", i)

        # Act
        removed = cache.invalidate_pattern(r"key:[0-4]")

        # Assert
        assert removed == 5
        for i in range(5):
            assert cache.get(f"key:{i}") is None
        for i in range(5, 10):
            assert cache.get(f"key:{i}") == i


class TestInMemoryCacheStats:
    """Tests for statistics tracking."""

    @pytest.mark.unit
    def test_stats_empty_cache(self) -> None:
        """Test stats for empty cache."""
        # Arrange
        cache = InMemoryCache(max_entries=1000)

        # Act
        stats = cache.stats()

        # Assert
        assert stats["current"] == 0
        assert stats["expired"] == 0
        assert stats["max_entries"] == 1000

    @pytest.mark.unit
    def test_stats_populated_cache(self) -> None:
        """Test stats for cache with entries."""
        # Arrange
        cache = InMemoryCache(max_entries=500)
        cache.set("key1", "val1")
        cache.set("key2", "val2")
        cache.set("key3", "val3")

        # Act
        stats = cache.stats()

        # Assert
        assert stats["current"] == 3
        assert stats["expired"] == 0
        assert stats["max_entries"] == 500

    @pytest.mark.unit
    def test_stats_expired_entries(self) -> None:
        """Test stats counts expired entries."""
        # Arrange
        cache = InMemoryCache()
        cache.set("valid", "value", ttl=10)
        cache.set("expired1", "value", ttl=1)
        cache.set("expired2", "value", ttl=1)

        # Act
        time.sleep(1.1)
        stats = cache.stats()

        # Assert
        assert stats["current"] == 3
        assert stats["expired"] == 2

    @pytest.mark.unit
    def test_stats_after_invalidation(self) -> None:
        """Test stats after invalidating entries."""
        # Arrange
        cache = InMemoryCache(max_entries=1000)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)

        # Act
        cache.invalidate("a")
        stats = cache.stats()

        # Assert
        assert stats["current"] == 2
        assert stats["expired"] == 0

    @pytest.mark.unit
    def test_stats_after_pattern_invalidation(self) -> None:
        """Test stats after pattern-based invalidation."""
        # Arrange
        cache = InMemoryCache()
        cache.set("world:123:a", 1)
        cache.set("world:123:b", 2)
        cache.set("user:456", 3)

        # Act
        cache.invalidate_pattern(r"world:123:.*")
        stats = cache.stats()

        # Assert
        assert stats["current"] == 1
        assert stats["expired"] == 0

    @pytest.mark.unit
    def test_stats_after_clear(self) -> None:
        """Test stats after clearing cache."""
        # Arrange
        cache = InMemoryCache(max_entries=500)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)

        # Act
        cache.clear()
        stats = cache.stats()

        # Assert
        assert stats["current"] == 0
        assert stats["expired"] == 0
        assert stats["max_entries"] == 500


class TestInMemoryCacheEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_cache_with_zero_max_entries(self) -> None:
        """Test cache behavior with max_entries=1."""
        # Arrange
        cache = InMemoryCache(max_entries=1)

        # Act
        cache.set("a", 1)
        cache.set("b", 2)

        # Assert
        assert cache.get("a") is None
        assert cache.get("b") == 2

    @pytest.mark.unit
    def test_cache_with_large_ttl(self) -> None:
        """Test cache with very large TTL."""
        # Arrange
        cache = InMemoryCache(default_ttl=86400)  # 24 hours

        # Act
        cache.set("key", "value")
        result = cache.get("key")

        # Assert
        assert result == "value"

    @pytest.mark.unit
    def test_cache_complex_nested_values(self) -> None:
        """Test cache stores complex nested structures."""
        # Arrange
        cache = InMemoryCache()
        complex_value = {
            "user": {
                "id": "123",
                "profile": {
                    "name": "Test User",
                    "tags": ["tag1", "tag2"],
                },
            },
            "metadata": [1, 2, 3],
        }

        # Act
        cache.set("complex", complex_value)
        result = cache.get("complex")

        # Assert
        assert result == complex_value
        assert result["user"]["profile"]["name"] == "Test User"

    @pytest.mark.unit
    def test_cache_empty_string_key(self) -> None:
        """Test cache handles empty string as key."""
        # Arrange
        cache = InMemoryCache()

        # Act
        cache.set("", "value")
        result = cache.get("")

        # Assert
        assert result == "value"

    @pytest.mark.unit
    def test_cache_special_chars_in_keys(self) -> None:
        """Test cache handles special characters in keys."""
        # Arrange
        cache = InMemoryCache()
        special_keys = [
            "key:with:colons",
            "key-with-dashes",
            "key_with_underscores",
            "key/with/slashes",
            "key.with.dots",
        ]

        # Act & Assert
        for key in special_keys:
            cache.set(key, f"value_for_{key}")
            assert cache.get(key) == f"value_for_{key}"

    @pytest.mark.unit
    def test_cache_pattern_invalid_regex(self) -> None:
        """Test invalidate_pattern with invalid regex raises."""
        # Arrange
        cache = InMemoryCache()
        cache.set("key1", "value1")

        # Act & Assert
        with pytest.raises(Exception):  # re.error
            cache.invalidate_pattern(r"[invalid(regex")
