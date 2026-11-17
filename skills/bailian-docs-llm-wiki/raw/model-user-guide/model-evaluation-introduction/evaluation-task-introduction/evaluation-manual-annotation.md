# 人工标注评测

介绍使用人工评估维度的评测任务的人工标注流程：Case 分析页配置人工维度、快速标注模式、评测详情抽屉内对比参考答案与模型输出并打标签。

## 人工标注评测概述

人工标注评测适用于需要人工判断的场景，如创意性写作、专业性内容评审等。使用人工评估-分类型维度（参见[人工评估](raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)）创建的评测任务，需要人工逐条为模型推理结果标注 Pass/Fail 标签。基线评测任务不可进入人工标注页面。

## 标注流程

1.  在[评测任务列表](https://bailian.console.aliyun.com/cn-beijing/model/evaluate/task)中，找到使用人工评估维度的评测任务，单击任务名称打开详情。
2.  在 Case 分析页签，可先单击**人工维度配置**，在弹层中从已创建的人工评测维度列表单击**添加**，或单击**创建人工维度**新建（最多 10 个人工标注维度），并可切换**快速标注**模式提高标注效率。
3.  单击样本的**详情**打开评测详情抽屉：左侧以对话形式展示完整多轮对话内容，可对比参考答案与模型输出；底部标签区展示人工标注维度与标签，为当前样本选择对应标签完成标注。
4.  使用**上一条**、**下一条**按钮在样本间翻页，直至所有数据标注完成。

## 标注进度与任务状态

全部数据标注完成后，任务状态自动变为评测完成，结果解读参见[查看评测结果](raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)。标注完成前，任务始终处于进行中状态。

与自动评测相比，人工评估无裁判模型评分费用，但需要人力投入且耗时更长。标签设计的详细说明请参见[人工评估](https://help.aliyun.com/zh/model-studio/evaluation-dimension-manual#h2-manual-labels)。
