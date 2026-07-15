# 智能体应用

智能体应用（Agent）是阿里云百炼平台的核心应用构建模式之一，通过自然语言零代码配置，让大模型基于角色设定自主决策、动态规划并调用知识库、MCP、Skill 等工具来完成任务。相较于流程固定的工作流应用，智能体强调 AI 的自主性，适合意图开放、需要动态编排的对话与轻量任务场景。

## 版本演进：Agent 1.0 与 Agent 2.0

百炼提供两代技术架构不同的智能体，**不支持直接升级或版本切换**，迁移需重新创建：

- **新版智能体（Agent 2.0）**：2025 年 12 月 26 日上线。将知识库、MCP 等能力统一抽象为「工具」，由智能体自主规划调用时机与顺序，并完整展示「规划-执行-反思」链路。无旧版依赖时推荐使用。**仅支持 API 调用，不支持任何分享渠道**（魔笔/UI、钉钉、微信、组件、音视频互动）。
- **旧版智能体（Agent 1.0）**：通过知识库（RAG）+ 插件扩展能力，先检索知识再决策是否调用工具，适合意图单一、流程固定的简单任务。自定义插件有 **5 秒超时限制**。分享渠道均为 1.0 功能。

## 核心能力配置（Agent 2.0）

- **模型选择**：推荐具备强工具调用能力的模型（如千问-Max 系列）；可配置最长回复长度、`temperature`、`enable_thinking`（思考模式）等参数。
- **提示词（System Prompt）**：定义角色、行为指令与能力边界，支持自定义变量嵌入。
- **内置工具**：沙箱环境下的 `bash`、`write`、`read`、`edit`、`glob`、`grep`、`download_file`，默认关闭需按需开启。
- **知识库**：作为工具由智能体自主调用，支持标签过滤限定查询范围。
- **MCP**：外部工具以 MCP 协议接入，支持动态非固定顺序调用。
- **Skill**：可扩展能力包，智能体在对话中自动识别匹配任务并调用，无需额外编码。
- **记忆**：短期记忆支持 0-30 轮上下文；长期记忆暂未支持。
- **ReAct 最大轮次**：取值 1-50，限制单次会话内工具调用最大次数。

## 文件问答

智能体应用支持上传文件进行问答，提供三种处理模式：

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| 全文引用 | 文档总结、全文翻译 | 简单直接，受上下文长度限制 |
| 切片检索（RAG） | 长文档问答、知识库检索 | 能处理超长文件，效果依赖检索策略 |
| 自定义处理 | 图片转换、视频分析等 | 功能灵活，依赖配置的工具 |

限制：单会话最多 10 个文件，单文件不超过 10 MB（超出需用文件上传 API）。支持文档、图片、视频、音频等格式。

## 发布与调用

所有应用类型均需先发布才能通过 API 集成，核心步骤：在应用配置页点击「发布」→ 在「发布渠道」查看调用方式。RAM 账号发布前需拥有 `ram:CreateServiceLinkedRole` 权限。

API 调用与工作流应用完全一致，通过 `Application.call` / `POST /apps/{app_id}/completion` 触发：

```python
import os
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)
print(response.output.text)
```

响应结构为 `{"output": {"finish_reason", "session_id", "text"}, "usage": {...}, "request_id": "..."}`，业务侧主要消费 `output.text`。

## 分享与组件化（仅 Agent 1.0）

- **分享渠道**：UI 应用/魔笔、钉钉、微信公众号、音视频实时互动。UI 体验链接与音视频临时二维码有效期均为 **24 小时**。分享产生的费用由应用创建者 UID 账号承担。
- **组件化**：智能体或工作流可发布为模块化组件供其他应用复用。接入智能体时组件作为工具，大模型据「组件描述」自动判断调用；预设系统参数 `query`、`imageList` 无法删除。注意避免嵌套调用（A↔B）和多级调用（A→B→C 易超时）。

## 与 Managed Agents 的区别

Managed Agents 是服务端托管运行时，与无状态的智能体应用不同：它在独立云端沙箱容器中维护会话状态，支持中断与续接、事件历史持久化，面向多步工具调用、代码执行、文件处理等长时运行任务。

## 计费说明

- **模型调用**：按模型类型和 Token 用量计费。
- **知识库**：按量付费，召回的文本切片会增加输入 Token；自 2026 年 1 月 4 日起正式计费。
- **MCP/插件**：部分官方 MCP 按调用计费，第三方 MCP 由第三方收取。

百炼提供限时免费额度，可在模型广场查看。

## 关联主题页

- [llm application](../guides/llm-application.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [managed agents](../guides/managed-agents.md)
- [application publishing and sharing](../guides/application-publishing-and-sharing.md)
- [start using](../guides/start-using.md)
- [skill](../guides/skill.md)


