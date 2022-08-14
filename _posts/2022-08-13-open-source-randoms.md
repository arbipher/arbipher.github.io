---
layout: post
title: Open-source randoms
comments: true
category:
- english
- open-source
---

# LLVM

I made a few PRs and reviews for llvm.

# Health check

[copy/gdbprofiler](https://github.com/copy/gdbprofiler/issues/11) is a cross-platform OCaml profiler. It works under Windows WSL2 and MacOS 12. See my experiment [note](https://github.com/copy/gdbprofiler/issues/11). The author suggests [perf](https://discuss.ocaml.org/t/ann-perf-demangling-of-ocaml-symbols-a-short-introduction-to-perf/7143) over gdbprofiler nowadays, though it only runs on linux.