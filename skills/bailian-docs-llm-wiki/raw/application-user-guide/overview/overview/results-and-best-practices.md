# 获取文档解析结果

获取 Parse 的解析过程和结果。

Parse 返回的是供下游使用的结构化结果。本页介绍如何阅读解析内容、对照原文件核验，以及把结果交给 Agent 应用。

## 开始前与入口

**项目**

**要求**

任务

已成功完成的文档解析任务

当前结果

运行完成后，在「文档解析」工作区查看

历史结果

从[任务记录](raw/application-user-guide/overview/configurations/tasks.md)打开对应任务的结果

## 查看图文结果

### 选择查看结果

**视图**

**用途**

**重点查看**

Markdown

连续阅读解析内容

标题、段落、表格和图片说明

JSON

查看结构化内容

程序需要读取的内容及相关信息

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dce.png)

_在 Markdown 视图中阅读解析内容，并与左侧原文件对照。_

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dc9.png)

_切换到 JSON 视图，检查结果的结构化内容。_

### 对照原文件

1.  在原文件中选定要核验的页面。
2.  在结果中找到对应标题、段落或表格。
3.  逐项核对关键内容，尤其是业务将直接使用的数据。

**内容**

**核对方法**

正文

检查标题、段落顺序和内容是否完整

表格

检查表头、行列关系、金额、日期和单位

图片说明

对照原图，检查描述与图中关系是否一致

内容位置

需要应用定位原文时，检查结果中的位置信息

需要补充位置信息或调整保留内容时，阅读[配置文档解析](raw/application-user-guide/overview/overview/configuration.md)。

## 查看音视频结果

音视频按内容和时间位置组织结果。音频重点查看语音；视频还需查看画面与文字说明是否对应。

### 选择视频结果视图

**页面视图**

**用来了解什么**

剧情概述

视频整体内容及主要角色等信息

解析段落结果

各时间段的语音、画面及相关说明

剧情分段

内容划分出的片段及片段主题

剧情摘要

视频中的主要要点

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9dda.png)

### 定位并核对片段

1.  打开「解析段落结果」。
2.  在时间线中找到要查看的片段。
3.  点击片段的时间位置，将播放器定位到对应内容。
4.  播放原文件，核对文字、画面和前后语境。

![](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9db7.png)

_通过时间线中的片段，回看视频对应内容。_

概述和摘要用于快速浏览。引用原话、精确数字和操作细节时，使用段落结果并回听或回看原文件。

## 取用结果

**使用方式**

**操作**

手动查看或复制

使用控制台结果区域的复制按钮，取用文本或结构化内容

交给自己的 Agent 应用

按 [REST API 接入](raw/application-user-guide/overview/overview/rest-api.md)取得任务结果，并读取返回内容或结果文件

从图文结果中继续取得指定字段

在[信息抽取控制台](raw/application-user-guide/overview/overview/extract.md)选择可复用的已解析文档

## 相关指南

-   [文档解析概览](raw/application-user-guide/overview/overview.md)：回顾文档解析能力与完整任务流程。
-   [配置文档解析](raw/application-user-guide/overview/overview/configuration.md)：检查文件信息、解析范围、增强选项和输出形式。
