# 内容安全与合规

内容安全与合规是百炼平台面向生成式 AI 应用的核心横切能力，指对模型输入（如用户提示、上传文件、记忆数据）与输出（如大模型回复、RAG 检索结果、工具调用返回）进行实时风险识别、策略化拦截与合规性校验的统一防护机制，确保内容符合中国《生成式人工智能服务管理暂行办法》等监管要求及业务安全基线。

## 在百炼平台的不同场景中，这个概念如何使用

内容安全与合规能力以「分层嵌入、按需启用」方式贯穿全链路，无需开发者重复集成：

- **API 调用层**：通过 `application call` 接口（如 `/v1/chat/completions` 或 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`）自动触发默认内容过滤；支持通过请求头（如 `X-Qwen-Security-Level: high`）动态提升检测强度。
- **Agent 运行时层**：Flow Agent / Managed Agent / RAG / Memory 等模块默认启用内生内容安全 I/O 拦截——包括提示词注入识别、知识库预扫描、记忆读写过滤、工具返回内容校验，全程无感生效。
- **Security API 独立服务层**：提供细粒度、可编程的内容检测能力（文本/图像），适用于需自定义处置逻辑（如人工复审分流）、多模态混合风控或非百炼托管模型的接入场景。
- **应用发布与备案层**：在「AI 应用管理」中完成合规备案前，生产环境调用将被拦截；备案信息自动同步至国家网信办公示页面，且受 `X-Qwen-Compliance-Mode: cn-gov` 等参数驱动的本地化策略约束。

> ✅ 默认防护 = 自动拦截（阻断高危内容）  
> ⚠️ 高级防护 = 风险监测 + 审计告警（不自动阻断，需人工介入）

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 生效范围 |
|------|------|------|------|-----------|
| `X-Qwen-Security-Level` | 请求 Header | `low` / `medium` / `high` | 控制内容过滤强度，默认 `medium`；`high` 启用语义+多模态联合研判 | 所有模型 API 调用（含 [application call](../api/application-call.md)） |
| `X-Qwen-Compliance-Mode` | 请求 Header | `cn-gov` / `global` | 激活境内敏感词库、备案字段校验等策略集 | 中国区租户，影响输入/输出双端 |
| `policy_id` | Security API 请求体 | string | 指定自定义风控策略 ID；未传则使用租户默认策略 | Security API（`/v1/security/detect`） |
| `scene` | Security API 请求体 | string（如 `"chat"`、`"search"`） | 标识业务上下文，动态调整各风险维度权重 | Security API |
| `return_full_result` | Security API 请求体 | boolean | 设为 `true` 时返回各风险维度（涉政、暴恐、色情等）分值与置信度 | Security API（调试/审计必备） |
| `timeout` | Security API 请求体 | integer（ms） | 建议设为 `5000–15000`，避免图像解码超时导致失败 | Security API |

> 💡 提示：所有参数均为可选，未显式指定时采用租户级默认策略；策略变更后 5 分钟内全量生效。

## 面向开发者，简洁实用

- **快速启用**：无需代码改造——只要使用百炼托管的 Agent 或调用标准模型 API，即默认获得基础内容安全防护。
- **精准调试**：调用 Security API 时务必设置 `return_full_result=true`，结合响应中的 `result.risk_level`（0–5）和 `result.action`（`"allow"`/`"block"`/`"review"`）定位问题。
- **规避陷阱**：
  - 图像检测不支持 GIF 动画，需提前转为 JPG/PNG；
  - `policy_id` 更新后新请求立即生效，但历史检测结果不可回溯变更；
  - 免费试用账号无法启用 `high` 安全等级或私网访问，升级企业版后自动解锁；
  - 自建审批流程一旦完成，控制台「内容安全」项将显示为“关闭”，默认防护能力受限。
- **合规上线必做三步**：① 在控制台「安全中心 → 合规策略」配置全局默认等级；② 应用发布前完成 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)；③ 生产调用必须携带 `X-Qwen-Compliance-Mode: cn-gov`（境内场景）。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security guide](../guides/security-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)


