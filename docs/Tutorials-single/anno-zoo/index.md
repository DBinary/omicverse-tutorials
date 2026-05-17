# Individual methods

Each notebook here drills into one annotation backend, calling its
low-level entry point directly rather than going through
`ov.single.Annotation`. Useful when you need to tune a specific method
beyond what the unified `Annotation.annotate(method=...)` interface
exposes, or when comparing how each backend behaves on the same input.

- [SCSA — marker-based annotation](t_cellanno.ipynb)
- [GPT-cell-type — LLM annotation from top markers](t_gptanno.ipynb)
- [MetaTiME — tumor microenvironment meta-components](t_metatime.ipynb)
- [scMulan — single-cell foundation model](t_scmulan.ipynb)
- [TOSICA — transformer-based reference-supervised classifier](t_tosica.ipynb)

For the recommended, unified workflows that combine these methods, see:

- [Reference-free annotation (Annotation API)](../t_anno_noref.ipynb)
- [Reference-based annotation (Annotation API)](../t_anno_ref.ipynb)
- [Consensus across methods (CellVote)](../t_cellvote.ipynb)
