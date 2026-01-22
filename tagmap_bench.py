#!/usr/bin/env python
import os
import time
import random
import statistics as stats
import tagmap


def bench(name, fn, repeats=5, warmup=1):
    for _ in range(warmup):
        fn()
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    total = sum(times)
    return {
        "name": name,
        "repeats": repeats,
        "total_s": total,
        "avg_s": total / repeats,
        "median_s": stats.median(times),
        "min_s": min(times),
        "max_s": max(times),
    }


def pct(x, p):
    if not x:
        return None
    x = sorted(x)
    i = int(round((p / 100) * (len(x) - 1)))
    return x[max(0, min(i, len(x) - 1))]


def run_stress(
    n_objects=200_000,
    n_tags=2_000,
    tags_per_obj=6,
    n_queries=50_000,
    query_k=2,
    query_any_ratio=0.5,
    erase_ratio=0.05,
    seed=1,
):
    random.seed(seed)

    tags = [f"t{i}" for i in range(n_tags)]
    objs = [f"obj{i}" for i in range(n_objects)]

    m = tagmap.TagMap()

    obj_tags = []
    for _ in range(n_objects):
        obj_tags.append(random.sample(tags, tags_per_obj))

    def do_insert():
        m.clear()
        for i, ot in enumerate(obj_tags):
            m[objs[i]] = ot

    def do_queries():
        q_times = []
        any_cnt = 0
        all_cnt = 0
        hits = 0
        for _ in range(n_queries):
            qs = random.sample(tags, query_k)
            t0 = time.perf_counter()
            if random.random() < query_any_ratio:
                r = m.find_any(qs)
                any_cnt += 1
            else:
                r = m.find(qs)
                all_cnt += 1
            t1 = time.perf_counter()
            q_times.append(t1 - t0)
            hits += len(r)
        return q_times, any_cnt, all_cnt, hits

    def do_mutations():
        ops = int(n_queries * erase_ratio)
        erased = 0
        readded = 0
        for _ in range(ops):
            o = random.choice(objs)
            if random.random() < 0.5:
                if o in m:
                    m.erase(o)
                    erased += 1
            else:
                m[o] = random.sample(tags, tags_per_obj)
                readded += 1
        return erased, readded

    results = []

    r = bench("insert_all", do_insert, repeats=3, warmup=0)
    results.append(r)

    q_times = []
    meta = {"any_cnt": 0, "all_cnt": 0, "hits": 0}

    def q_run():
        qt, ac, alc, h = do_queries()
        q_times.extend(qt)
        meta["any_cnt"] += ac
        meta["all_cnt"] += alc
        meta["hits"] += h

    r = bench("queries_mixed", q_run, repeats=3, warmup=1)
    results.append(r)

    mut_meta = {"erased": 0, "readded": 0}

    def mut_run():
        e, a = do_mutations()
        mut_meta["erased"] += e
        mut_meta["readded"] += a

    r = bench("mutations", mut_run, repeats=3, warmup=1)
    results.append(r)

    results.append(
        {
            "name": "query_latency_stats",
            "repeats": len(q_times),
            "total_s": sum(q_times),
            "avg_s": (sum(q_times) / len(q_times)) if q_times else 0.0,
            "median_s": stats.median(q_times) if q_times else 0.0,
            "min_s": min(q_times) if q_times else 0.0,
            "max_s": max(q_times) if q_times else 0.0,
        }
    )

    print(f"Python {os.sys.version.split()[0]}")
    print(
        f"Objects={n_objects:,} Tags={n_tags:,} Tags/obj={tags_per_obj} Queries={n_queries:,} k={query_k}"
    )
    print(
        f"Query mix: any={query_any_ratio:.2f} all={1.0 - query_any_ratio:.2f} erase_ratio={erase_ratio:.2f}"
    )
    print()

    for r in results:
        print(
            f"{r['name']}: total={r['total_s']:.4f}s avg={r['avg_s']:.6f}s "
            f"median={r['median_s']:.6f}s min={r['min_s']:.6f}s max={r['max_s']:.6f}s "
            f"(repeats={r['repeats']})"
        )

    if q_times:
        q_us = [t * 1e6 for t in q_times]
        print()
        print(
            f"query latency (us): p50={pct(q_us, 50):.2f} p90={pct(q_us, 90):.2f} p99={pct(q_us, 99):.2f} "
            f"avg={sum(q_us) / len(q_us):.2f} min={min(q_us):.2f} max={max(q_us):.2f}"
        )
        print(
            f"query calls: any={meta['any_cnt']:,} all={meta['all_cnt']:,} total_hits={meta['hits']:,}"
        )

    print()
    print(f"mutations: erased={mut_meta['erased']:,} readded={mut_meta['readded']:,}")
    print(f"final size: {len(m):,}")
    print(f"unique tags in map: {len(m.tags()):,}")


if __name__ == "__main__":
    run_stress(
        n_objects=200_000,
        n_tags=2_000,
        tags_per_obj=6,
        n_queries=50_000,
        query_k=2,
        query_any_ratio=0.5,
        erase_ratio=0.05,
        seed=1,
    )
