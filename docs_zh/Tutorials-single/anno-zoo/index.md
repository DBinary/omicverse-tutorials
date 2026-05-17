# 单独的注释方法

下面这些教程分别针对一个注释 backend 直接调其低层入口，不走
`ov.single.Annotation` 统一接口。适合需要对某一方法做精细调参，或者
希望在相同输入上对比每个 backend 表现的场景。

- [SCSA — 基于 marker 的注释](t_cellanno.ipynb)
- [GPT-cell-type — 用 LLM 从 top marker 注释](t_gptanno.ipynb)
- [MetaTiME — 肿瘤微环境元组件](t_metatime.ipynb)
- [scMulan — 单细胞基础模型](t_scmulan.ipynb)
- [TOSICA — 基于 transformer 的参考监督分类器](t_tosica.ipynb)

推荐的统一工作流入口：

- [无参考注释（Annotation API）](../t_anno_noref.ipynb)
- [参考注释（Annotation API）](../t_anno_ref.ipynb)
- [多方法共识（CellVote）](../t_cellvote.ipynb)
