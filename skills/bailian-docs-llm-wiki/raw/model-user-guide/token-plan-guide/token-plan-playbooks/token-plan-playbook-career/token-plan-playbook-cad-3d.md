# 三维 CAD 建模 · 出 STEP/STL 文件

一句话描述零件，模型生成建模脚本，本地 CAD 内核执行后产出 STEP/STL 文件。

**说明**

**免责声明**：本页展示内容均为 AI 模型生成，仅供参考，不构成任何效果承诺；实际产出效果与 Credits 消耗以控制台「用量详情」为准。

本篇以「40×30×8 mm 底板 + 中心 Ø10 mm 通孔」跑通：`qwen3.8-max` 把一句话需求写成 cadquery 建模脚本，本地内核执行后导出 STEP/STL，并打印体积校验，模型体积与解析值零误差——把建模从点鼠标变成写需求。

调用链：`qwen3.8-max`（需求 → cadquery 参数化建模脚本）→ 本地开源 CAD 内核（cadquery）执行 → 导出 STEP/STL（本地执行不耗 Credits）。

## 实测产出

以「40×30×8 mm 底板 + 中心 Ø10 mm 通孔」跑通，cadquery 导出的三维投影与体积校验：

![底板+通孔三维投影](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9e12.svg)
```
模型体积(mm³): 8971.681469
解析体积(mm³): 8971.681469
差值(mm³): 0.000000
相对误差: 0.000000%
（导出文件：bracket.step 20KB · bracket.stl 26KB）
```

## 步骤：一句话建模

把下面的指令发给 `qwen3.8-max`：

```
用 Python cadquery 写脚本：建一块 40×30×8 mm 底板，正中心钻 Ø10 mm 通孔；
导出 bracket.step 与 bracket.stl；并打印模型体积与解析体积(40*30*8 − π*5²*8)对比。
只输出可直接运行的完整 Python 代码。
```

## 说明

-   **消耗**：本玩法涉及文本生成（`qwen3.8-max`，生成 cadquery 建模脚本）；脚本本地执行导出 STEP/STL 不耗 Credits。
-   **精度**：实测模型体积与解析值零误差（0.000000%），几何精确，可直接用于下游制造。
-   **分工与前置**：模型只负责生成脚本，导出由本地内核完成；执行前需先安装内核（`pip install cadquery`，建议 Python 3.10+ 独立虚拟环境）。本例用开源内核 cadquery，同类可换 Blender / FreeCAD MCP。
