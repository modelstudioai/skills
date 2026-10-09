# agenteval

`agenteval` 是百炼平台提供的面向智能体（Agent）应用的端到端评测与可观测性工具，支持自动化评估任务完成质量、响应一致性、工具调用准确性等核心指标。它不依赖人工标注，可基于预定义的评测协议（如 `task_success`, `tool_call_f1`）对 Agent 输出进行结构化打分。该能力深度集成于百炼控制台与 SDK，适用于开发、测试与迭代阶段。

## 支持的模型与功能

- 支持所有已在百炼平台部署并启用 `agent` 类型的模型服务（含 Qwen 系列、自定义 LLM + Tool Router 架构）；
- 核心功能包括：**自动任务评测**（基于黄金标准或规则引擎）、**链路级可观测性追踪**（含 Thought/Action/Observation 完整序列）、**多维度聚合分析**（按标签、版本、会话 ID 分组）；
- 不支持纯文本生成类模型（如仅开启 `chat` 模式且未配置 tools 的模型），此类场景需先通过 [应用评测](raw/application-user-guide/agenteval/agenteval-evaluation.md) 文档确认适配性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `eval_config` | object | 是 | 包含 `metric`, `reference`, `timeout_ms`；其中 `metric` 必须为预注册指标（如 `"task_success"`），详见 [应用评测](raw/application-user-guide/agenteval/agenteval-evaluation.md) |
| `trace_id` | string | 否 | 关联已有观测链路，用于将评测结果注入对应 trace；若为空则新建 trace |
| `tags` | map[string]string | 否 | 键值对形式的元数据，用于后续按业务维度筛选（如 `{"env": "staging", "version": "v2.1"}`），参考 [标签管理](raw/application-user-guide/agenteval/agenteval-tags.md) |

> **注意**：`eval_config.reference` 在 v3.2+ 版本中已改为支持 JSON Schema 校验模式，旧版文档中描述的纯字符串 reference 已过时，请以 [应用评测](raw/application-user-guide/agenteval/agenteval-evaluation.md) 最新说明为准。

## 使用方式

1. **SDK 调用（推荐）**：  
   ```python
   from alibabacloud_bailian20231219 import models as agenteval_models
   client = AgentevalClient(config)
   req = agenteval_models.EvaluateRequest(
       app_id="app-xxx",
       input={"query": "查上海今天天气"},
       eval_config={"metric": "task_success", "reference": {"weather": "sunny"}}
   )
   resp = client.evaluate(req)
   ```

2. **控制台操作**：在「应用详情 → 评测」页上传测试集（JSONL 格式），选择指标后启动批量评测；结果实时同步至 [应用观测](raw/application-user-guide/agenteval/agenteval-observability.md) 页面。

## 限制和注意事项

- 单次评测请求最大输入长度为 8192 tokens，超长输入将被截断并记录 warning 日志；
- 批量评测任务最多支持 1000 条样本，超出需分批提交；
- 评测结果默认保留 30 天，如需长期归档，请导出至 OSS 并配置生命周期策略；
- 当前不支持跨模型对比评测（例如同时评测 Qwen-Agent 与 Llama-Agent），此能力计划在下一版本上线，当前请分别执行并手动比对，详见 [更新日志](raw/application-user-guide/agenteval/agenteval-changelog.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agenteval.md)


