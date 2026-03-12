#!/usr/bin/env python
"""Comprehensive test suite for TagMap."""

import pytest
import tagmap


class TestTagMapBasics:
    """Test basic TagMap operations."""

    def test_empty_tagmap(self) -> None:
        """Test creating an empty TagMap."""
        m = tagmap.TagMap()
        assert len(m) == 0
        assert list(m) == []
        assert m.tags() == []

    def test_set_and_get(self) -> None:
        """Test setting and getting entries."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        assert "alice" in m
        assert set(m["alice"]) == {"dev", "python"}

    def test_from_dict(self) -> None:
        """Test creating TagMap from dictionary."""
        m = tagmap.TagMap.from_dict({"alice": {"dev", "python"}, "bob": ["cpp", "dev"]})
        assert len(m) == 2
        assert set(m["alice"]) == {"dev", "python"}
        assert set(m["bob"]) == {"cpp", "dev"}

    def test_to_dict(self) -> None:
        """Test converting TagMap to dictionary."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        m["bob"] = {"cpp"}
        d = m.to_dict()
        assert "alice" in d
        assert "bob" in d
        assert set(d["alice"]) == {"dev", "python"}


class TestTagManipulation:
    """Test tag addition and removal operations."""

    def test_add_tag(self) -> None:
        """Test adding a single tag."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m.add_tag("alice", "python")
        assert set(m["alice"]) == {"dev", "python"}

    def test_add_tags(self) -> None:
        """Test adding multiple tags."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m.add_tags("alice", ["python", "ml"])
        assert set(m["alice"]) == {"dev", "python", "ml"}

    def test_remove_tag(self) -> None:
        """Test removing a tag."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python", "ml"}
        m.remove_tag("alice", "python")
        assert set(m["alice"]) == {"dev", "ml"}

    def test_remove_tag_nonexistent_raises(self) -> None:
        """Test removing non-existent tag raises error."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        with pytest.raises(KeyError):
            m.remove_tag("alice", "nonexistent")

    def test_discard_tag(self) -> None:
        """Test discarding a tag (no error if missing)."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        m.discard_tag("alice", "python")
        assert set(m["alice"]) == {"dev"}
        m.discard_tag("alice", "nonexistent")  # Should not raise

    def test_has_tag(self) -> None:
        """Test checking if entry has a tag."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        assert m.has_tag("alice", "dev")
        assert m.has_tag("alice", "python")
        assert not m.has_tag("alice", "cpp")

    def test_has_tag_nonexistent_key(self) -> None:
        """Test has_tag with non-existent key."""
        m = tagmap.TagMap()
        assert not m.has_tag("nonexistent", "dev")


class TestQueries:
    """Test query operations (all-of and any-of)."""

    def setup_method(self) -> None:
        """Set up test TagMap."""
        self.m = tagmap.TagMap()
        self.m["alice"] = {"dev", "python"}
        self.m["bob"] = {"dev", "cpp"}
        self.m["carol"] = {"design", "python"}
        self.m["dave"] = {"ops"}

    def test_query_single_tag(self) -> None:
        """Test querying with single tag."""
        result = self.m.query("dev")
        assert set(result) == {"alice", "bob"}

    def test_query_multiple_tags(self) -> None:
        """Test querying with multiple tags (AND)."""
        result = self.m.query("dev", "python")
        assert set(result) == {"alice"}

    def test_query_empty(self) -> None:
        """Test empty query returns all entries."""
        result = self.m.query()
        assert set(result) == {"alice", "bob", "carol", "dave"}

    def test_find_with_list(self) -> None:
        """Test find method with list of tags."""
        result = self.m.find(["dev", "python"])
        assert set(result) == {"alice"}

    def test_query_any_single_tag(self) -> None:
        """Test query_any with single tag."""
        result = self.m.query_any("dev")
        assert set(result) == {"alice", "bob"}

    def test_query_any_multiple_tags(self) -> None:
        """Test query_any with multiple tags (OR)."""
        result = self.m.query_any("dev", "ops")
        assert set(result) == {"alice", "bob", "dave"}

    def test_find_any(self) -> None:
        """Test find_any method."""
        result = self.m.find_any(["design", "cpp"])
        assert set(result) == {"bob", "carol"}

    def test_query_nonexistent_tag(self) -> None:
        """Test query with non-existent tag returns empty."""
        result = self.m.query("nonexistent")
        assert set(result) == set()


class TestCounts:
    """Test count operations."""

    def setup_method(self) -> None:
        """Set up test TagMap."""
        self.m = tagmap.TagMap()
        self.m["alice"] = {"dev", "python"}
        self.m["bob"] = {"dev", "cpp"}
        self.m["carol"] = {"design", "python"}
        self.m["dave"] = {"ops"}

    def test_count_single_tag(self) -> None:
        """Test counting entries with a single tag."""
        assert self.m.count(["dev"]) == 2

    def test_count_multiple_tags(self) -> None:
        """Test counting entries with multiple tags (AND)."""
        assert self.m.count(["dev", "python"]) == 1

    def test_count_any(self) -> None:
        """Test counting entries with any tag (OR)."""
        assert self.m.count_any(["dev", "ops"]) == 3

    def test_count_nonexistent(self) -> None:
        """Test counting non-existent tag returns zero."""
        assert self.m.count(["nonexistent"]) == 0


class TestDictOperations:
    """Test dictionary-like operations."""

    def test_get_existing(self) -> None:
        """Test get on existing key."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        result = m.get("alice")
        assert set(result) == {"dev"}

    def test_get_missing_default_none(self) -> None:
        """Test get on missing key with default None."""
        m = tagmap.TagMap()
        assert m.get("alice") is None

    def test_get_missing_default_value(self) -> None:
        """Test get on missing key with custom default."""
        m = tagmap.TagMap()
        default = {"default"}
        result = m.get("alice", default)
        assert result is default

    def test_setdefault_existing(self) -> None:
        """Test setdefault on existing key."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        result = m.setdefault("alice", {"new"})
        assert set(result) == {"dev"}

    def test_setdefault_missing(self) -> None:
        """Test setdefault on missing key."""
        m = tagmap.TagMap()
        result = m.setdefault("alice", {"dev"})
        assert set(result) == {"dev"}
        assert set(m["alice"]) == {"dev"}

    def test_pop_existing(self) -> None:
        """Test pop on existing key."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        result = m.pop("alice")
        assert set(result) == {"dev", "python"}
        assert "alice" not in m

    def test_pop_missing_raises(self) -> None:
        """Test pop on missing key returns None."""
        m = tagmap.TagMap()
        result = m.pop("alice")
        assert result is None

    def test_pop_missing_default(self) -> None:
        """Test pop on missing key with default."""
        m = tagmap.TagMap()
        result = m.pop("alice", {"default"})
        assert result == {"default"}

    def test_popitem(self) -> None:
        """Test popitem."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m["bob"] = {"cpp"}
        key, tags = m.popitem()
        assert key in ["alice", "bob"]
        assert len(m) == 1

    def test_popitem_empty_raises(self) -> None:
        """Test popitem on empty map raises KeyError."""
        m = tagmap.TagMap()
        with pytest.raises(KeyError):
            m.popitem()

    def test_update_from_dict(self) -> None:
        """Test update from dictionary."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m.update({"bob": {"cpp"}, "carol": {"design"}})
        assert len(m) == 3
        assert set(m["bob"]) == {"cpp"}

    def test_keys(self) -> None:
        """Test keys method."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m["bob"] = {"cpp"}
        keys = list(m)
        assert set(keys) == {"alice", "bob"}


class TestEraseOperations:
    """Test erase operations."""

    def test_erase_existing(self) -> None:
        """Test erasing an existing entry."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m["bob"] = {"cpp"}
        m.erase("alice")
        assert "alice" not in m
        assert "bob" in m

    def test_erase_nonexistent_raises(self) -> None:
        """Test erasing non-existent entry raises KeyError."""
        m = tagmap.TagMap()
        with pytest.raises(KeyError):
            m.erase("alice")

    def test_discard_existing(self) -> None:
        """Test discarding existing entry."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m.discard("alice")
        assert "alice" not in m

    def test_discard_nonexistent(self) -> None:
        """Test discarding non-existent entry (no error)."""
        m = tagmap.TagMap()
        m.discard("alice")  # Should not raise

    def test_erase_where_all_of(self) -> None:
        """Test erase_where with all-of query."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        m["bob"] = {"dev", "cpp"}
        m["carol"] = {"design"}
        removed = m.erase_where(["dev"])
        assert set(removed) == {"alice", "bob"}
        assert set(m) == {"carol"}

    def test_erase_where_returns_removed(self) -> None:
        """Test erase_where returns removed keys."""
        m = tagmap.TagMap()
        m["alice"] = {"dev"}
        m["bob"] = {"dev"}
        removed = m.erase_where(["dev"])
        assert set(removed) == {"alice", "bob"}


class TestRetainOperations:
    """Test retain operations."""

    def test_retain_where_all_of(self) -> None:
        """Test retain_where keeps only entries with all tags."""
        m = tagmap.TagMap()
        m["x"] = {"a", "b"}
        m["y"] = {"b"}
        m["z"] = {"c"}
        kept = m.retain_where(["b"])
        assert set(kept) == {"x", "y"}
        assert set(m) == {"x", "y"}

    def test_retain_where_returns_kept(self) -> None:
        """Test retain_where returns kept keys."""
        m = tagmap.TagMap()
        m["x"] = {"a"}
        m["y"] = {"b"}
        kept = m.retain_where(["a"])
        assert set(kept) == {"x"}

    def test_retain_where_any(self) -> None:
        """Test retain_where_any keeps only entries with any tag."""
        m = tagmap.TagMap()
        m["x"] = {"a", "b"}
        m["y"] = {"b"}
        m["z"] = {"c"}
        kept = m.retain_where_any(["a", "c"])
        assert set(kept) == {"x", "z"}
        assert set(m) == {"x", "z"}

    def test_retain_where_any_returns_kept(self) -> None:
        """Test retain_where_any returns kept keys."""
        m = tagmap.TagMap()
        m["x"] = {"a"}
        m["y"] = {"b"}
        m["z"] = {"c"}
        kept = m.retain_where_any(["a", "c"])
        assert set(kept) == {"x", "z"}


class TestTags:
    """Test tag management operations."""

    def test_tags_returns_all_unique_tags(self) -> None:
        """Test tags method returns all unique tags."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "python"}
        m["bob"] = {"cpp", "dev"}
        m["carol"] = {"design"}
        tags = set(m.tags())
        assert tags == {"dev", "python", "cpp", "design"}

    def test_tags_empty_map(self) -> None:
        """Test tags on empty map."""
        m = tagmap.TagMap()
        assert m.tags() == []


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_tag_set(self) -> None:
        """Test that entries must have at least one tag."""
        m = tagmap.TagMap()
        m["alice"] = set()
        # Empty sets don't create entries
        assert "alice" not in m

    def test_single_tag(self) -> None:
        """Test entry with single tag."""
        m = tagmap.TagMap()
        m["alice"] = ["dev"]
        assert set(m["alice"]) == {"dev"}

    def test_duplicate_tags(self) -> None:
        """Test that duplicate tags are handled correctly."""
        m = tagmap.TagMap()
        m["alice"] = {"dev", "dev"}  # Set deduplicates
        assert set(m["alice"]) == {"dev"}

    def test_mixed_tag_types(self) -> None:
        """Test setting tags with different iterable types."""
        m = tagmap.TagMap()
        m["a"] = {"dev"}
        m["b"] = ["python"]
        m["c"] = ("cpp",)
        assert set(m["a"]) == {"dev"}
        assert set(m["b"]) == {"python"}
        assert set(m["c"]) == {"cpp"}

    def test_large_dataset(self) -> None:
        """Test with large number of entries."""
        m = tagmap.TagMap()
        n = 1000
        for i in range(n):
            m[f"entry_{i}"] = {f"tag_{i % 10}"}
        assert len(m) == n
        result = m.query("tag_0")
        assert len(result) == n // 10

    def test_many_tags_per_entry(self) -> None:
        """Test entry with many tags."""
        m = tagmap.TagMap()
        tags = {f"tag_{i}" for i in range(100)}
        m["alice"] = tags
        assert set(m["alice"]) == tags


class TestConstructors:
    """Test alternate constructors."""

    def test_construct_from_dict(self) -> None:
        """Test creating TagMap from a dictionary."""
        d = {"alice": {"dev", "python"}, "bob": ["cpp", "dev"]}
        m = tagmap.TagMap(d)
        assert len(m) == 2
        assert set(m["alice"]) == {"dev", "python"}
        assert set(m["bob"]) == {"cpp", "dev"}

    def test_construct_from_list_of_tuples(self) -> None:
        """Test creating TagMap from a list of tuples."""
        pairs = [("alice", {"dev", "python"}), ("bob", ["cpp", "dev"])]
        m = tagmap.TagMap(pairs)
        assert len(m) == 2
        assert set(m["alice"]) == {"dev", "python"}
        assert set(m["bob"]) == {"cpp", "dev"}

    def test_construct_from_empty_dict(self) -> None:
        """Test creating TagMap from an empty dictionary."""
        m = tagmap.TagMap({})
        assert len(m) == 0

    def test_construct_from_empty_list(self) -> None:
        """Test creating TagMap from an empty list."""
        m = tagmap.TagMap([])
        assert len(m) == 0

    def test_construct_from_invalid_list_raises(self) -> None:
        """Test that a list of non-pairs raises ValueError."""
        with pytest.raises(TypeError):
            tagmap.TagMap([("a", {"b"}), ("c",)])  # type: ignore[no-matching-overload]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestTagMapInitializers:
    def test_init_from_dict_ctor(self) -> None:
        m = tagmap.TagMap({"a": {"x", "y"}, "b": ["z"]})
        assert set(m["a"]) == {"x", "y"}
        assert set(m["b"]) == {"z"}

    def test_init_from_pairs_ctor(self) -> None:
        m = tagmap.TagMap([("a", ["x"]), ("b", {"y", "z"})])
        assert set(m["a"]) == {"x"}
        assert set(m["b"]) == {"y", "z"}

    def test_init_from_keys_values_ctor(self) -> None:
        m = tagmap.TagMap(["a", "b"], [["x"], ["y", "z"]])
        assert set(m["a"]) == {"x"}
        assert set(m["b"]) == {"y", "z"}

    def test_init_keys_values_length_mismatch(self) -> None:
        with pytest.raises(ValueError):
            tagmap.TagMap(["a", "b"], [["x"]])

    def test_from_keys_values_static(self) -> None:
        m = tagmap.TagMap.from_keys_values(["a"], [["x", "y"]])
        assert set(m["a"]) == {"x", "y"}
