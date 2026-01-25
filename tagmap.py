#!/usr/bin/env python
import tagmap


def show(m: tagmap.TagMap, title: str = ""):
    if title:
        print("\n" + title)
        print("-" * len(title))
    print("repr:", m)
    print("len:", len(m))
    print("keys:", list(m))
    print("tags:", sorted(m.tags()))
    print("dict:", {k: sorted(v) for k, v in m.to_dict().items()})


m = tagmap.TagMap()

m["alice"] = {"dev", "python"}
m["bob"] = {"dev", "cpp"}
m["carol"] = ["design", "python"]
m["dave"] = ("dev", "ops")

show(m, "after inserts")

print("\ngetitem:")
print("alice ->", sorted(m["alice"]))
print("alice has 'python'?", m.has_tag("alice", "python"))
print("alice in m?", "alice" in m)

m.add_tag("alice", "ml")
m.add_tags("bob", ["linux", "perf"])
m.discard_tag("dave", "ops")
m.remove_tag("carol", "design")

show(m, "after tag edits")

print("\nqueries (all-of / intersection):")
print("dev & cpp ->", sorted(m.query("dev", "cpp")))
print("{python, dev} ->", sorted(m.find(["python", "dev"])))
print("empty query ->", sorted(m.query()))

print("\nqueries (any-of / union):")
print("python OR ops ->", sorted(m.query_any("python", "ops")))
print("{ml, perf} ->", sorted(m.find_any(["ml", "perf"])))

print("\ncounts:")
print("count(dev) ->", m.count(["dev"]))
print("count_any(python, perf) ->", m.count_any(["python", "perf"]))

print("\nsetdefault / get:")
print("get(eve, None) ->", m.get("eve", None))
m.setdefault("eve", ["new"])
print("eve ->", sorted(m["eve"]))

print("\nupdate from dict:")
m.update({"frank": {"dev", "go"}, "gina": ["design"]})
show(m, "after update")

print("\npop / popitem:")
print("pop(eve) ->", sorted(m.pop("eve")))
k, v = m.popitem()
print("popitem ->", k, sorted(v))
show(m, "after pops")

print("\nerase / discard:")
m.erase("bob")
m.discard("not-there")
show(m, "after erase/discard")

print("\nerase_where:")
removed = m.erase_where(["dev"])
print("removed dev-tagged:", sorted(removed))
show(m, "after erase_where(dev)")

m2 = tagmap.TagMap.from_dict({"x": {"a", "b"}, "y": {"b"}, "z": {"c"}})
show(m2, "m2")

print("\nretain_where (keep only all-of):")
kept = m2.retain_where(["b"])
print("kept:", sorted(kept))
show(m2, "m2 after retain_where(b)")

m3 = tagmap.TagMap.from_dict({"x": {"a", "b"}, "y": {"b"}, "z": {"c"}})
print("\nretain_where_any (keep only any-of):")
kept = m3.retain_where_any(["a", "c"])
print("kept:", sorted(kept))
show(m3, "m3 after retain_where_any(a,c)")
