# 人工评估

人工评估维度由评测人员手动按标签对模型输出分类，适合需要主观判断的场景，如创意性写作、专业领域判断。

## 人工评估概述

人工评估由评测人员逐条查看模型推理结果并标注 Pass/Fail 标签，不涉及裁判模型，无评分费用，但需要人力投入且耗时更长。适合机器难以准确评价的场景：

-   创意性写作、语气风格等主观质量判断。
-   专业领域内容合规性审核。

与其他维度类型的对比与选择建议请参见[评测维度](raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 创建人工评估维度

登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/evaluate/dimension_template)，选择左侧导航栏的**模型评测**，切换到**评测维度** Tab，单击**创建评测维度**，在弹窗中单击**\+ 创建自定义评测维度**进入自定义配置页面。公共字段（维度名称不超过 20 字符、描述不超过 100 字符、类型创建后不可更改）填写后，按以下步骤完成配置：

1.  配置**Pass 标签**：定义通过判定的标签含义。
2.  配置**Fail 标签**：定义未通过的判定标签含义。Pass 和 Fail 标签不可重复。
3.  单击**保存**。

## 标签设计建议

Pass 和 Fail 标签应互斥且穷尽，即所有可能的输出都能归入其中一类。简单场景使用二分类即可；复杂场景需要多标签时，控制标签数量以降低评判歧义。标签设计应简洁明确，覆盖所有可能的评判结果。

使用人工评估维度的评测任务须全部数据标注完成后才变为评测完成状态，标注操作请参见[人工标注评测](raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)。
