# skill

skill 是百炼平台中用于封装和复用 AI 能力的可调用单元，支持将大模型推理、工具调用、数据处理等逻辑打包为标准化接口。开发者可通过 API 或低代码方式集成 skill，实现业务流程自动化。其设计目标是解耦模型能力与业务逻辑，提升开发效率与可维护性。

## 支持的模型/功能

skill 支持绑定 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Baichuan、GLM 等主流开源及平台托管模型，并可组合调用函数工具（Function Calling）、RAG 检索节点、HTTP 请求节点等。部分高级功能（如多 step 流程编排、异步事件触发）仅在企业版中可用，详见 [Skill](https://help.aliyun.com/zh/model-studio/introduction-to-skill) 的官方说明。当前技能运行时默认使用 `qwen-max` 作为 fallback 模型，但该行为已在 [Skill (raw/application-user-guide/skill.md)](../../raw/application-user-guide/skill.md) 中明确标注为历史兼容策略，新创建 skill 应显式指定模型。

## 关键参数

- `model_id`: 必填，指定所用模型 ID（如 `qwen-plus`），不支持通配符或别名  
- `input_schema`: JSON Schema 格式，定义输入字段名、类型、是否必填及示例值  
- `output_schema`: 同上，用于结构化输出校验与前端映射  
- `timeout`: 单位秒，默认 60，最大 300；超时后返回 `504 Gateway Timeout`  
- `enable_tracing`: 布尔值，启用后记录完整执行链路（含 token 消耗、各 step 耗时），对调试至关重要，参考 [Skill (raw/application-user-guide/skill.md)](../../raw/application-user-guide/skill.md)

## 使用方式

1. **创建**：通过控制台「技能中心」新建，或调用 `/v1/skills` POST 接口上传 YAML/JSON 定义  
2. **部署**：发布前需通过「测试运行」验证输入输出符合 schema，否则部署失败  
3. **调用**：HTTP POST 到 `https://dashscope.aliyuncs.com/api/v1/skills/{skill_id}/invoke`，Header 需含 `Authorization: Bearer {api_key}`，Body 为符合 `input_schema` 的 JSON 对象  
4. **调试**：推荐使用控制台内置调试器，支持断点查看中间变量；日志详情见 [Skill (raw/application-user-guide/skill.md)](../../raw/application-user-guide/skill.md)

## 限制和注意事项

- 单次请求 payload 不得超过 2 MB；输入文本长度上限为 32768 tokens（按模型 tokenizer 计算）  
- skill 内部不支持跨账号资源访问（如其他用户的 RAG 知识库），需确保所有依赖资源权限已正确授予  
- > **注意**：文档中提及的 “支持 WebSocket 长连接调用” 属于已下线功能，自 v2024.07 版本起仅保留 HTTP RESTful 接口，旧版 SDK 示例已过时，请以当前 OpenAPI 文档为准  
- 异步 skill（`execution_mode=async`）返回 `task_id` 后，需轮询 `/v1/tasks/{task_id}` 获取结果，最长保留 24 小时

## 来源文档

- [Skill](../../raw/application-user-guide/skill.md)


