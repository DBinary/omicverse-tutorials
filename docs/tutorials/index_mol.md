# Molecular structure & drug-binding

Tutorials for the `omicverse.mol` module — the bridge from an omics **target
protein** to its **3D structure** and **drug context**.

A typical omicverse analysis ends with a target: a differential gene from
`ov.bulk`, a marker or driver from `ov.single`, a variant from `ov.genetics`.
The natural next questions are structural and pharmacological — *what does the
protein look like in 3D, where are its confident regions, does it have a
druggable pocket, are there known drugs against it, and can a candidate
molecule bind it?* `ov.mol` answers them, with **interactive 3D
visualization** (py3Dmol) that renders inline in Jupyter and **persists in the
exported HTML docs**.

The three notebooks follow the natural arc *see the target → assess it → test
a drug*, and each one follows the analysis workflow the field actually uses —
with the discipline (model-confidence assessment, redocking validation) a
structural biologist or computational chemist would apply. All three run one
real target, **EGFR**, framed as a hit handed over by an upstream omics
analysis.

| Notebook | What you learn |
|---|---|
| **Structure** | Fetch / predict and interactively visualize a target's structure — and assess model confidence (pLDDT, PAE) *before* trusting it. |
| **Druggability** | Detect binding pockets, score druggability, and check what drugs are already known — structure-based target prioritization. |
| **Docking** | Validate a docking protocol by redocking, then dock a candidate molecule and inspect the binding pose. |

```{toctree}
:maxdepth: 1

../Tutorials-mol/t_mol_structure
../Tutorials-mol/t_mol_druggability
../Tutorials-mol/t_mol_docking
```

## Installation

The structural-biology stack is optional. The core layer — structure
acquisition, interactive visualization and known-drug lookup:

```bash
pip install 'omicverse[mol]'
```

The docking layer (AutoDock Vina + receptor / ligand preparation):

```bash
pip install 'omicverse[mol-dock]'
```

Binding-pocket detection uses `rust-fpocket`, a pip-installable Rust port of
fpocket:

```bash
pip install fpocket-rs
```
