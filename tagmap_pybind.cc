#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "tagmap/tagmap.h"

#include <string>
#include <unordered_set>
#include <vector>

namespace py = pybind11;

using Tag = std::string;
using Data = std::string;
using Obj = Object<Data, Tag>;
using Map = Tagmap<Data, Tag>;

static inline std::unordered_set<Tag> to_tagset(const py::iterable &tags) {
  std::unordered_set<Tag> out;
  for (py::handle h : tags)
    out.insert(py::cast<Tag>(h));
  return out;
}

static inline bool has_data(const Map &m, const Data &d) {
  Obj probe(d);
  const size_t k = m.getkey(probe);
  auto it = m.objects.find(k);
  return it != m.objects.end() && it->second.data == d;
}

static inline const Obj &get_obj_or_throw(const Map &m, const Data &d) {
  Obj probe(d);
  const size_t k = m.getkey(probe);
  auto it = m.objects.find(k);
  if (it == m.objects.end() || it->second.data != d)
    throw py::key_error(d);
  return it->second;
}

static inline std::unordered_set<Tag> tags_of_or_empty(const Map &m,
                                                       const Data &d) {
  if (!has_data(m, d))
    return {};
  return get_obj_or_throw(m, d).references;
}

static inline void set_tags(Map &m, const Data &d,
                            const std::unordered_set<Tag> &tags) {
  m.insert(d, tags);
}

static inline bool erase_key_if_exists(Map &m, const Data &d) {
  if (!has_data(m, d))
    return false;
  (void)m.erase(&d);
  return true;
}

static inline std::vector<Data> keys_vec(const Map &m) {
  std::vector<Data> out;
  out.reserve(m.objects.size());
  for (const auto &kv : m.objects)
    out.push_back(kv.second.data);
  return out;
}

static inline std::vector<std::unordered_set<Tag>> values_vec(const Map &m) {
  std::vector<std::unordered_set<Tag>> out;
  out.reserve(m.objects.size());
  for (const auto &kv : m.objects)
    out.push_back(kv.second.references);
  return out;
}

static inline std::vector<std::pair<Data, std::unordered_set<Tag>>>
items_vec(const Map &m) {
  std::vector<std::pair<Data, std::unordered_set<Tag>>> out;
  out.reserve(m.objects.size());
  for (const auto &kv : m.objects)
    out.emplace_back(kv.second.data, kv.second.references);
  return out;
}

static inline std::unordered_set<Data> all_data_set(const Map &m) {
  std::unordered_set<Data> out;
  out.reserve(m.objects.size());
  for (const auto &kv : m.objects)
    out.insert(kv.second.data);
  return out;
}

static inline std::unordered_set<Data>
query_all_of(const Map &m, const std::unordered_set<Tag> &tags) {
  if (tags.empty())
    return all_data_set(m);
  auto s = m.find(tags);
  std::unordered_set<Data> out;
  out.reserve(s.size());
  for (const Data *p : s)
    out.insert(*p);
  return out;
}

static inline std::unordered_set<Data>
query_any_of(const Map &m, const std::unordered_set<Tag> &tags) {
  if (tags.empty())
    return all_data_set(m);
  std::unordered_set<size_t> keys;
  for (const auto &t : tags) {
    auto it = m.references.find(t);
    if (it != m.references.end())
      keys.insert(it->second.begin(), it->second.end());
  }
  std::unordered_set<Data> out;
  out.reserve(keys.size());
  for (size_t k : keys) {
    auto it = m.objects.find(k);
    if (it != m.objects.end())
      out.insert(it->second.data);
  }
  return out;
}

static inline std::unordered_set<Data>
retain_where_all_of(Map &m, const std::unordered_set<Tag> &tags) {
  auto keep = query_all_of(m, tags);
  auto ks = keys_vec(m);
  for (const auto &k : ks)
    if (keep.find(k) == keep.end())
      (void)m.erase(&k);
  return keep;
}

static inline std::unordered_set<Data>
retain_where_any_of(Map &m, const std::unordered_set<Tag> &tags) {
  auto keep = query_any_of(m, tags);
  auto ks = keys_vec(m);
  for (const auto &k : ks)
    if (keep.find(k) == keep.end())
      (void)m.erase(&k);
  return keep;
}

PYBIND11_MODULE(tagmap, m) {
  m.doc() = "Pythonic bindings for Tagmap<std::string,std::string>";

  py::class_<Obj>(m, "Object")
      .def(py::init<>())
      .def(py::init<const Data &>())
      .def(py::init<const Data &, const std::unordered_set<Tag> &>(),
           py::arg("data"), py::arg("tags"))
      .def_readwrite("data", &Obj::data)
      .def_property(
          "tags", [](const Obj &o) { return o.references; },
          [](Obj &o, const std::unordered_set<Tag> &t) { o.references = t; })
      .def("__repr__", [](const Obj &o) {
        return "Object(data=" + o.data +
               ", tags=" + std::to_string(o.references.size()) + ")";
      });

  py::class_<Map>(m, "TagMap")
      .def(py::init<>())

      .def("__len__", [](const Map &self) { return self.objects.size(); })
      .def("__bool__", [](const Map &self) { return !self.objects.empty(); })
      .def("__contains__",
           [](const Map &self, const Data &data) {
             return has_data(self, data);
           })

      .def("__getitem__",
           [](const Map &self, const Data &data) {
             return get_obj_or_throw(self, data).references;
           })

      .def("__setitem__",
           [](Map &self, const Data &data, const py::iterable &tags) {
             set_tags(self, data, to_tagset(tags));
           })

      .def("__delitem__",
           [](Map &self, const Data &data) {
             if (!erase_key_if_exists(self, data))
               throw py::key_error(data);
           })

      .def("__iter__",
           [](const Map &self) {
             py::list ks;
             ks.attr("extend")(py::cast(keys_vec(self)));
             return ks.attr("__iter__")();
           })

      .def("__repr__",
           [](const Map &self) {
             return "<tagmap.TagMap size=" +
                    std::to_string(self.objects.size()) +
                    " tags=" + std::to_string(self.references.size()) + ">";
           })

      .def("clear",
           [](Map &self) {
             auto ks = keys_vec(self);
             for (const auto &k : ks)
               (void)self.erase(&k);
           })

      .def("keys", [](const Map &self) { return keys_vec(self); })
      .def("values", [](const Map &self) { return values_vec(self); })
      .def("items", [](const Map &self) { return items_vec(self); })

      .def("tags", [](const Map &self) { return self.listtags(); })
      .def("data", [](const Map &self) { return keys_vec(self); })

      .def("to_dict",
           [](const Map &self) {
             py::dict d;
             for (const auto &kv : self.objects)
               d[py::cast(kv.second.data)] = py::cast(kv.second.references);
             return d;
           })

      .def_static("from_dict",
                  [](const py::dict &d) {
                    Map out;
                    for (auto item : d) {
                      Data data = py::cast<Data>(item.first);
                      auto tags = py::cast<py::iterable>(item.second);
                      set_tags(out, data, to_tagset(tags));
                    }
                    return out;
                  })

      .def("copy",
           [](const Map &self) {
             Map out;
             for (const auto &kv : self.objects)
               out.insert(kv.second.data, kv.second.references);
             return out;
           })

      .def(
          "get",
          [](const Map &self, const Data &data,
             py::object default_value) -> py::object {
            if (!has_data(self, data))
              return default_value;
            return py::cast(get_obj_or_throw(self, data).references);
          },
          py::arg("data"), py::arg("default") = py::none())

      .def(
          "setdefault",
          [](Map &self, const Data &data, const py::iterable &tags) {
            if (has_data(self, data))
              return get_obj_or_throw(self, data).references;
            auto t = to_tagset(tags);
            set_tags(self, data, t);
            return tags_of_or_empty(self, data);
          },
          py::arg("data"), py::arg("default") = py::tuple())

      .def("update",
           [](Map &self, const py::dict &d) {
             for (auto item : d) {
               Data data = py::cast<Data>(item.first);
               auto tags = py::cast<py::iterable>(item.second);
               set_tags(self, data, to_tagset(tags));
             }
           })

      .def(
          "discard",
          [](Map &self, const Data &data) {
            (void)erase_key_if_exists(self, data);
          },
          py::arg("data"))
      .def(
          "erase",
          [](Map &self, const Data &data) {
            if (!erase_key_if_exists(self, data))
              throw py::key_error(data);
          },
          py::arg("data"))

      .def(
          "pop",
          [](Map &self, const Data &data,
             py::object default_value) -> py::object {
            if (!has_data(self, data))
              return default_value;
            auto t = get_obj_or_throw(self, data).references;
            (void)self.erase(&data);
            return py::cast(t);
          },
          py::arg("data"), py::arg("default") = py::none())

      .def("popitem",
           [](Map &self) {
             if (self.objects.empty())
               throw py::key_error("popitem(): TagMap is empty");
             auto it = self.objects.begin();
             Data k = it->second.data;
             auto v = it->second.references;
             (void)self.erase(&k);
             return py::make_tuple(k, v);
           })

      .def(
          "tags_of",
          [](const Map &self, const Data &data) {
            return get_obj_or_throw(self, data).references;
          },
          py::arg("data"))

      .def(
          "has_tag",
          [](const Map &self, const Data &data, const Tag &tag) {
            if (!has_data(self, data))
              return false;
            const auto &t = get_obj_or_throw(self, data).references;
            return t.find(tag) != t.end();
          },
          py::arg("data"), py::arg("tag"))

      .def(
          "add_tag",
          [](Map &self, const Data &data, const Tag &tag) {
            auto t = tags_of_or_empty(self, data);
            t.insert(tag);
            set_tags(self, data, t);
          },
          py::arg("data"), py::arg("tag"))

      .def(
          "add_tags",
          [](Map &self, const Data &data, const py::iterable &tags) {
            auto t = tags_of_or_empty(self, data);
            for (py::handle h : tags)
              t.insert(py::cast<Tag>(h));
            set_tags(self, data, t);
          },
          py::arg("data"), py::arg("tags"))

      .def(
          "discard_tag",
          [](Map &self, const Data &data, const Tag &tag) {
            if (!has_data(self, data))
              return;
            auto t = get_obj_or_throw(self, data).references;
            t.erase(tag);
            set_tags(self, data, t);
          },
          py::arg("data"), py::arg("tag"))

      .def(
          "remove_tag",
          [](Map &self, const Data &data, const Tag &tag) {
            if (!has_data(self, data))
              throw py::key_error(data);
            auto t = get_obj_or_throw(self, data).references;
            if (t.find(tag) == t.end())
              throw py::key_error(tag);
            t.erase(tag);
            set_tags(self, data, t);
          },
          py::arg("data"), py::arg("tag"))

      .def("query",
           [](const Map &self, py::args tags) {
             std::unordered_set<Tag> t;
             t.reserve(tags.size());
             for (auto h : tags)
               t.insert(py::cast<Tag>(h));
             return query_all_of(self, t);
           })

      .def("query_any",
           [](const Map &self, py::args tags) {
             std::unordered_set<Tag> t;
             t.reserve(tags.size());
             for (auto h : tags)
               t.insert(py::cast<Tag>(h));
             return query_any_of(self, t);
           })

      .def(
          "find",
          [](const Map &self, const py::iterable &tags) {
            return query_all_of(self, to_tagset(tags));
          },
          py::arg("tags"))
      .def(
          "find_any",
          [](const Map &self, const py::iterable &tags) {
            return query_any_of(self, to_tagset(tags));
          },
          py::arg("tags"))

      .def(
          "count",
          [](const Map &self, const py::iterable &tags) {
            return query_all_of(self, to_tagset(tags)).size();
          },
          py::arg("tags"))
      .def(
          "count_any",
          [](const Map &self, const py::iterable &tags) {
            return query_any_of(self, to_tagset(tags)).size();
          },
          py::arg("tags"))

      .def(
          "erase_where",
          [](Map &self, const py::iterable &tags) {
            auto t = to_tagset(tags);
            if (t.empty())
              return std::unordered_set<Data>{};
            auto removed = self.erase(t);
            std::unordered_set<Data> out;
            out.reserve(removed.size());
            for (const auto &v : removed)
              out.insert(v);
            return out;
          },
          py::arg("tags"))

      .def(
          "retain_where",
          [](Map &self, const py::iterable &tags) {
            return retain_where_all_of(self, to_tagset(tags));
          },
          py::arg("tags"))

      .def(
          "retain_where_any",
          [](Map &self, const py::iterable &tags) {
            return retain_where_any_of(self, to_tagset(tags));
          },
          py::arg("tags"));
}
