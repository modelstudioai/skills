# 创建自定义评测任务

介绍如何创建自定义评测任务：选择评测模型、配置数据来源（单轮 prompt&completion 或多轮 ChatML 评测集）、关联评测维度，并设置并发数与单样本推理次数。

## 创建自定义评测任务概述

自定义评测基于业务效果，使用您的数据集和自定义维度评测模型。创建任务前，请确认已创建至少一个评测维度（参见[评测维度](raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)），并已在数据管理模块上传评测数据集（参见[训练集与评测集](raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)）。

在[百炼控制台的模型评测页面](https://bailian.console.aliyun.com/cn-beijing/model/evaluate/task/creation)，选择**评测任务**页签，单击**创建评测任务**，选择自定义评测。

## 选择评测模型

从控制台模型列表中选择要评测的目标模型。支持预置模型和调优后的模型，具体支持的模型请参见[预置模型列表](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。模型选择弹层支持按官方模型/我的模型切换，并按能力（Function Calling、结构化输出等）筛选；灰色显示的模型表示当前不支持评测。

## 配置数据来源

数据来源支持两种方式：

-   **评测数据集**：支持**文本生成（prompt&completion）**单轮格式（Prompt 与 Completion）与**文本生成（ChatML-messages）**多轮对话格式（参考答案为最后一条 assistant 消息）。系统调用被评测模型推理生成 Output 后再评分，会产生推理费用；多轮对话数据以完整对话送评，默认以最后一轮 user 消息作为当前问题。须为评测集（EvaluationSet）类型且已发布版本，在数据管理模块提前上传。
-   **推理结果集**：已包含模型 Output，系统直接评分不调用模型推理，不产生推理费用。适用于已有模型输出想降低成本的场景。

**对比项**

**评测数据集**

**推理结果集**

数据内容

包含 Prompt 和 Completion

已包含模型 Output

推理调用

系统调用被评测模型推理

不调用模型推理

推理费用

产生

不产生

适用场景

首次评测、标准流程

已有模型输出，降低成本

数据要求

评测集类型且已发布版本

按模板上传文件

数据量建议：小规模验证 50-100 条，正式评测 200-500 条，全面评估 500 条以上。

## 关联维度与任务配置

从已创建的评测维度中多选要关联的维度，可混用自定义评测维度与预置模板，须提前在评测维度页面创建。

推理参数按所选模型动态加载，可配置项包括 System Prompt（不超过 5000 字符，为被评测模型设定角色定位，大多数场景可留空）、推理模式（enable\_thinking）、核采样（top\_p）、温度（temperature）、停止词（stop）、联网搜索（enable\_search）与思维链长度（thinking\_budget）。

**并发数**默认为 8，可设置 1~20，影响评测任务的执行速度，不改变评测结果。

**单样本推理次数**默认为 1。设置为大于 1 时，每条样本推理多次并基于多次采样结果计算 Pass@K 等聚合指标，用于判断样本难度与模型表现稳定性（推理与评分费用随推理次数相应增加）。

是否参与排行开关默认关闭。开启后须选择一个排行榜，评测结果将加入排行参与排名。排行榜绑定维度为空时系统将阻止提交并显示错误提示。

清空评测维度时系统会自动清空排行榜选择。任务名称最长 50 字符（默认自动填充为「评测\_日期时间」）。配置完成后，单击**开始评测**提交任务，费用以实际发生为准（详见[计费说明](https://help.aliyun.com/zh/model-studio/model-evaluation-overview#ta12pj4r2re00)），提交前可查看计算详情。

任务提交后进入执行流程，状态流转与结果查看请参见[查看评测结果](raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)。

## 常见问题

问题：创建评测任务时选错了被评测模型，想更换模型。

任务一旦提交不可更换目标模型。处理方式：删除任务后重建。已消耗的 Token 费用不可追回。

问题：提交评测任务后状态显示失败。

请依次检查：数据集必须为评测集（EvaluationSet）类型并已发布版本（训练集不可用于评测），模型是否可选（灰色表示暂不支持），数据格式是否正确（prompt&completion 格式须包含 Prompt 和 Completion 列，ChatML 格式须为包含 messages 数组的合法 jsonl）。
