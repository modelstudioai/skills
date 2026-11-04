# 快速开始

了解 ParseX 的控制台体验流程，快速体验平台功能。

## 文档处理完成路径

[

**1\. 选择并上传**

按任务选择 Parse 或 Extract。

](#h-parse-qs-upload)[

**2\. 核对结果**

对照原文检查解析内容或抽取字段。

](#h-parse-qs-results)[

**3\. 保存配置（可选）**

记录生成的 config\_id。

](#h-parse-qs-config)[

**4\. 准备接口调用**

选择复用配置或直接传参。

](#h-parse-qs-api)[

**5\. 查看任务**

查看状态、结果与用量。

](#h-parse-qs-tasks)

## 前置准备

-   已获得控制台访问权限，并从正式授权入口进入目标 Workspace。未获得入口时，先联系服务提供方或管理员，见 [REST API 接入准备](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/rest-api.md)。
-   准备本地文件或样本文档，以及需要核对的内容或待抽取字段。体验页面支持单个文档最大 200MB、单张图片最大 20MB；API 调用的文件大小限制请查看对应 API 文档。
-   **Parse** 将文档解析为可读取的结构化内容；**Extract** 按配置的字段抽取信息。配置要求分别参见[配置文档解析](raw/application-user-guide/agent-context/getting-started-overview/overview/configuration.md)和[信息抽取控制台](raw/application-user-guide/agent-context/getting-started-overview/extract-overview/playground-extract.md)。

## 步骤 1：选择文档并上传

在 Parse 或 Extract 控制台选择本地文件或样本文档，根据目标配置解析能力或待抽取字段，并发起处理。

## 步骤 2：逐项核对结果

等待处理完成，将运行结果与原文和预期对照，检查内容完整性、结构准确度、抽取内容准确性等信息。

-   **Parse**：核对解析得到的内容与结构，确认原文信息是否完整，参见[文档解析](raw/application-api-reference/api-overview/document-parsing.md)。
-   **Extract**：结果区提供「抽取结果 JSON」与「抽取字段详情」两种查看方式，字段详情逐项列出字段值及其来源页码。对照来源页核对抽取内容。

## 步骤 3：保存配置（可选）

可在体验页面将配置好的解析/抽取设置保存成配置，生成唯一的 `config_id` 进行接口调用。记录与当前 Parse 或 Extract 能力对应的配置 ID。

## 步骤 4：按定好的配置或者参数调用

接口可复用同一 `config_id` 进行调用，也可以直接传入解析/抽取的配置参数进行任务调用。保存配置与内联处理参数二选一，不在同一次调用中同时传入。

**说明**生产 Base URL 尚未公开确认。先根据 [REST API 接入](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/rest-api.md)准备集成；正式生产入口发布后再发起 REST 调用。

-   Parse：[提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md) → [查询解析结果](raw/application-api-reference/api-overview/document-parsing/parse-result.md)。
-   Extract：[提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md) → [查询抽取结果](raw/application-api-reference/api-overview/field-extraction/extract-result.md)。

## 步骤 5：查看任务

控制台操作可在“任务记录”中查看页面提供的状态、结果和用量，参见[任务记录](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md)。API 提交后保存返回的 `biz_id`，通过对应结果接口轮询处理状态。

**说明**控制台体验的完成结果是一份可与原文核对的解析内容或抽取字段；若保存了配置，还应记录其 `config_id`。`biz_id` 用于查询异步任务，不是配置 ID。先确认处理完成，再核对结果内容。

## 下一步

[

**接入文档解析 API**

了解 Parse 提交与结果查询。

](raw/application-api-reference/api-overview/document-parsing.md)[

**接入信息抽取 API**

了解 Extract 字段配置与结果查询。

](raw/application-api-reference/api-overview/field-extraction.md)
