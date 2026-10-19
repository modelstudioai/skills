# 使用 CLI

在终端用阿里云百炼 CLI 直接检索与问答知识库。

阿里云百炼 CLI（`bailian-cli`）把知识库检索与问答封装为命令，便于在终端或 Agent 中调度。

**说明**知识库相关 CLI 能力目前仅对中国站（aliyun.com）账号开放。

## 命令

能力

命令

说明

常用参数

语义检索

`bl knowledge search`

调用检索服务进行语义检索

`--query` 查询内容、`--agent-id` 检索服务 ID

RAG 问答

`bl knowledge chat`

调用问答服务进行 RAG 问答，支持流式输出

`--message` 消息内容、`--agent-id` 问答服务 ID

直接检索（已弃用）

`bl knowledge retrieve`

直接对知识库检索，建议改用 `search`

`--index-id` 知识库 ID、`--query` 查询内容

## 示例

```
bl knowledge search --query "如何配置切片策略？" --agent-id <检索服务ID>
bl knowledge chat --message "如何配置切片策略？" --agent-id <问答服务ID>
```

任意命令追加 `--help` 查看完整参数。控制台 [**服务渠道**](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面提供安装命令和使用示例。
