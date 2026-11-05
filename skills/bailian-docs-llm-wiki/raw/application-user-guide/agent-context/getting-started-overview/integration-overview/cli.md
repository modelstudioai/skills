# 使用 CLI

在终端用阿里云百炼 CLI 提交 ParseX 文档解析与字段抽取任务。

阿里云百炼 CLI（`bailian-cli`）把 ParseX 的解析与字段抽取封装为命令，便于在终端或 Agent 中调度。

**说明**ParseX 服务目前仅在中国站提供，CLI 默认使用北京业务空间域名；可用性取决于业务空间和开通状态。CLI 使用业务空间专属 API 和普通 API Key，不支持上传本地文件。

## 前提条件

-   已[安装阿里云百炼 CLI](https://help.aliyun.com/zh/model-studio/cli/installation)并配置 API Key。
-   已取得 ParseX 可用的业务空间 ID，并通过 `--workspace-id`、`BAILIAN_WORKSPACE_ID` 或配置项 `workspace_id` 指定。
-   输入文件存放在可访问的 HTTP(S) URL，包括带签名的 OSS URL。

## 命令

能力

命令

说明

常用参数

文档或音视频解析

`bl parsex parse submit`

提交解析任务，立即返回 `data.biz_id`

`--file-url` 源文件 URL、`--config-id` 已保存配置、`--processing-file` 处理配置

查询解析结果

`bl parsex parse result`

查询状态、结果或分片，`--follow` 轮询到终态

`--biz-id` 任务 ID、`--follow`、`--poll-timeout`

字段抽取

`bl parsex extract submit`

按 JSON Schema 抽取字段并返回原文引用

`--file-url` 或 `--parsed-file-biz-id`、`--schema-file`

查询抽取结果

`bl parsex extract result`

查询抽取状态、字段和引用

`--biz-id` 任务 ID、`--follow`

完整参数见 [ParseX 命令参考](https://help.aliyun.com/zh/model-studio/cli/parsex)。

## 示例

```
bl parsex parse submit --workspace-id <workspace-id> --file-url "https://example.com/document.pdf" --file-name document.pdf --output-file-format markdown --output json
bl parsex parse result --workspace-id <workspace-id> --biz-id <parse-biz-id> --follow --output json
bl parsex extract submit --workspace-id <workspace-id> --parsed-file-biz-id <parse-biz-id> --schema-file schema.json --output json
bl parsex extract result --workspace-id <workspace-id> --biz-id <extract-biz-id> --follow --output json
```

-   提交类命令不等待任务完成，使用对应的 `result --follow` 获取结果。
-   单次查询时任务失败仍返回退出码 0；`--follow` 失败退出码 1，超时 5，Ctrl-C 130。
-   内联的处理配置优先于 `--config-id`。抽取的 Schema 以对象发送，不要写成 JSON 字符串。
-   抽取不支持音视频；复用的解析结果需仍被服务保存且可复用。

任意命令追加 `--help` 查看完整参数。
