# Individual methods

Each notebook here drills into one annotation backend, calling its
low-level entry point directly rather than going through
`ov.single.Annotation`. Useful when you need to tune a specific method
beyond what the unified `Annotation.annotate(method=...)` interface
exposes, or when comparing how each backend behaves on the same input.

```{toctree}
:maxdepth: 1

t_cellanno
t_gptanno
t_metatime
t_scmulan
t_tosica
```

For the recommended, unified workflows that combine these methods, see:

- [Reference-free annotation (Annotation API)](../t_anno_noref.ipynb)
- [Reference-based annotation (Annotation API)](../t_anno_ref.ipynb)
- [Consensus across methods (CellVote)](../t_cellvote.ipynb)
