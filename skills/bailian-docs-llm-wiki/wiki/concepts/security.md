# 安全防护

安全防护是百炼平台内生、开箱即用的智能体全生命周期安全治理能力，覆盖开发、运行、数据、记忆与生态链路。它通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」闭环机制，实现资产自动识别、风险实时监测与事件可追溯，无需开发者自行构建底层安全设施。

## 在百炼平台的不同场景中，这个概念如何使用

安全防护以**分层启用、按需生效**方式深度集成于各核心模块：

- **Flow Agent**：默认启用输入/输出内容安全检测（含提示词注入识别）；当接入 RAG 或 Memory 时，自动触发知识库内容与记忆读写内容的安全扫描。
- **Managed Agent**：默认提供沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理；所有运行时行为均在受控环境中执行。
- **RAG（知识库）**：上传文件时默认预扫描（病毒、恶意宏）；启用高级防护后，额外执行知识库内容投毒检测（如恶意指令注入、隐蔽后门文本）。
- **Memory（记忆服务）**：默认对读写内容进行合规性检测（涉政、涉黄、隐私泄露等），防止敏感信息意外留存或泄露。
- **Store（MCP/Skill）**：默认对上架的技能包（.zip/.py）执行供应链静态扫描，识别恶意代码、高危依赖（如 `requests>=2.32.0` 中的 CVE-2023-31519）、硬编码密钥等风险。
- **模型调用层**：通过 `X-DashScope-DataInspection` 请求头可按需启用 AI 安全护栏，对单次请求的 `input` 和 `output` 进行实时内容合规检测（CIP 类型）。

> ⚠️ 注意：**默认防护自动生效，不消耗 Credit，仅记录基础日志；高级防护需开通服务授权（限时免费），才可生成完整风险事件（含风险等级、触发节点、Trace ID）并支持审计回溯。**

## 关键参数和配置

| 参数/配置项 | 说明 | 使用位置 | 备注 |
|-------------|------|----------|------|
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏的 HTTP 请求头 | 模型/Agent 调用 API | 值为 JSON 字符串（需转义双引号），非法值返回 400 |
| `--risk-level high` | CLI 命令中过滤高风险告警 | `bl agents security alerts` | 支持 `high`/`medium`/`low`，默认返回全部 |
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | SDK 级传输加密开关 | DashScope SDK 调用 | 自动管理 AES 密钥与 RSA 加解密，无需手动调用公钥接口 |
| `available: false` | API 响应中表示某策略未开通 | `/policies` 等接口响应体 | 不导致整体失败，便于前端灰度降级 |
| `Credit` | 安全检测计费单位 | 高级防护启用后 | 按被检测内容 [Token](token.md) 数换算，每席位每日 300 Credits 免费额度 |

- **策略配置入口**：控制台 → **Security > 高级防护 > 安全策略**  
- **全局生效性**：所有安全策略对账号下全部 Agent 全局生效，不区分业务空间，修改前请评估影响范围。  
- **审计数据延迟**：防护总览页面数据约每 2 分钟刷新一次，非实时。

## 面向开发者，简洁实用

- ✅ **开箱即用**：只要使用 Flow/Managed Agent、RAG、Memory 或 Store，对应默认防护即自动启用，无需代码改造。  
- ✅ **按需增强**：通过控制台一键开通高级防护，即可获取结构化风险事件与审计日志，用于自动化响应或合规报告。  
- ✅ **统一 API**：所有安全数据通过 `/api/v1/agentstudio/security` 接口族获取，支持告警查询、资产统计、策略管理与日志导出，响应格式统一（`{"success": true, "data": {...}}`）。  
- ✅ **SDK 友好**：DashScope Python/Java SDK 已内置传输加密、安全护栏等能力，一行代码启用（如 `Generation.call(..., enable_encryption=True)`）。  
- ✅ **最小侵入**：安全能力不改变原有调用协议（如 [OpenAI 兼容接口](openai-compatible-api.md)仍可用），仅通过新增 Header 或参数启用。  

> 💡 提示：首次集成建议先运行 `bl agents security overview` 查看当前防护覆盖情况；生产环境务必开通高级防护以满足审计与溯源要求。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [knowledge base](../guides/knowledge-base.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)


