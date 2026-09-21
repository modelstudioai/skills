# 任务记录

通过任务记录查找某次解析或抽取处理、确认任务状态、核对当时使用的设置，并重新打开结果。

解析或抽取任务提交成功后，会生成一条任务记录。通过任务记录，可以查找某次处理、确认状态、核对当时使用的设置，并重新打开结果。

## 使用前准备

-   已提交解析或抽取任务。
-   准备完整任务 ID，或记下大致提交日期和所用能力。
-   登录 [ParseX 控制台](https://bailian.console.aliyun.com/cn-beijing/parsex/document-parse)，从左侧进入「任务记录」。

## 查找一次处理

1.  按日期缩小查找范围。注意：考虑到隐私安全，当前只会保存最近7天的历史任务。
2.  根据需要选择能力和任务状态。
3.  有任务 ID 时，将完整 ID 粘贴到「任务 ID」搜索框，按 Enter（回车）搜索。
4.  核对文件名称、能力和时间，打开目标任务详情。

同一份文件多次运行会产生不同任务。确认任务 ID 后，再检查该次结果，避免混淆不同时间的处理。

## 了解状态和处理信息

**页面状态**

**含义**

**接下来做什么**

排队中

任务已提交，等待处理

等待状态更新

运行中

正在处理文件

等待任务完成

已完成

本次处理成功

打开结果，检查内容是否满足应用要求

失败

本次处理未成功

查看详情中的错误提示，按[常见问题](raw/application-user-guide/getting-started-overview/settings-configurations/faq.md)检查

**详情信息**

**用途**

任务 ID、文件和时间

确认正在查看哪一次处理

处理状态

确认任务是否结束、是否成功

耗时

了解本次处理花费的时间

单次用量

查看本次处理的数量

配置快照

查看本次运行使用的设置

比较历史结果时，应比较两次任务各自使用的设置。当前配置经过编辑后，不代表历史任务也使用了新设置。两者关系见[保存与复用配置](raw/application-user-guide/getting-started-overview/settings-configurations.md)。

## 返回结果页

1.  在目标任务详情中确认任务和状态。
2.  点击「前往playground查看结果」。
3.  在打开的解析或抽取工作台中查看原文和结果。

**结果类型**

**阅读说明**

文档、图片、音频或视频解析

[获取文档解析结果](raw/application-user-guide/getting-started-overview/overview/results-and-best-practices.md)

字段抽取

[获取信息抽取结果](raw/application-user-guide/getting-started-overview/extract-overview/extract-results.md)

完成后，你应能找到目标任务并打开对应结果。需要查看一段时间的处理总量时，进入[用量](raw/application-user-guide/getting-started-overview/settings-configurations/usage.md)。
