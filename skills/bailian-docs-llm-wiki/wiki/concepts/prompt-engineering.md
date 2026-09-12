# 提示词工程

提示词工程（Prompt Engineering）是系统性设计、优化和管理输入提示（[prompt](../guides/prompt.md)）以引导大语言模型产生高质量、可控、可复现输出的技术实践。它贯穿模型调用全生命周期，涵盖结构化模板构建、变量注入、自动重写、反馈迭代与效果评估等环节，是百炼平台上实现任务精准适配与效果持续提升的核心能力。

## 在百炼平台的不同场景中如何使用

- **基础模型调用**：通过 `/v1/chat/completions` 接口直接传入 `messages` 数组（含 `system`/`user`/`assistant` 角色），其中 `system` 内容即为显式提示词，用于设定角色、约束格式或注入领域知识（注意：部分旧模型如 `qwen-plus` 不支持 `system` 角色，需降级为 `user` 前置说明）；  
- **模板化生产应用**：在控制台或 API 中使用 `prompt_template_id` + `variables` 调用 `/v1/prompt/render` 渲染动态 Prompt，适用于问答机器人、报告生成、代码辅助等需多实例复用的场景；  
- **RAG 增强应用**：在启用 `retrieval: true` 的请求中，平台自动将检索结果拼接进 Prompt 上下文，此时提示词需明确指示模型“仅依据以下文档回答”，避免幻觉——推荐在模板中预置标准 RAG 指令句式；  
- **智能体（Agent）与工作流**：Agent 2.0 内部调度依赖提示词定义工具调用协议（如 JSON Schema 描述函数）、思考链（CoT）触发逻辑及错误恢复策略，开发者可通过 `system_prompt` 字段定制行为范式；  
- **实时多模态交互**：在 `qwen3.5-omni-plus-realtime` 等模型中，提示词需兼顾文本指令与音视频上下文描述（如 `"当前用户正在说话，请等待语音结束再响应"`），且必须通过 AOQ/WebRTC 协议传递，不可走 HTTP 同步接口。

## 关键参数和配置

- `prompt_template_id`：引用已保存的提示词模板 ID，支持控制台创建、版本管理与跨 API 复用；  
- `variables`：JSON 对象，键名需与模板中 `${key}` 占位符严格一致，值支持字符串、数字、布尔值及嵌套对象（自动 JSON 序列化）；  
- `optimization_mode`：设为 `"auto"` 启用平台自动优化（基于样例库重写提示词），`"feedback"` 启用反馈驱动优化（需配合用户点赞/点踩事件）；  
- `max_prompt_tokens`：硬性截断阈值（单位：token），建议设为所选模型 context length 的 70%~80%，避免因超限导致推理失败；  
- `system_prompt`（部分接口支持）：轻量级角色设定字段，适用于 IM 集成等不支持完整 `messages` 结构的场景，但受长度限制（如微信公众号 ≤200 字符）。

## 面向开发者的实用建议

- ✅ **优先使用模板**：将重复逻辑（如“请用 Markdown 输出”“禁止编造数据”）固化为模板，而非每次硬编码，便于统一维护与 A/B 测试；  
- ✅ **变量注入前校验**：对 `variables` 中的用户输入做基础清洗（如去除控制字符、截断超长文本），防止模板渲染异常或注入攻击；  
- ✅ **监控 token 消耗**：在日志中记录 `rendered_prompt_token_count`（渲染后实际 token 数），结合 `max_prompt_tokens` 设置告警阈值；  
- ⚠️ **避免过度依赖自动优化**：`optimization_mode=auto` 仅对 `text-generation` 类任务生效，且可能改变原始意图，上线前务必人工验证输出一致性；  
- ⚠️ **RAG 场景必加指令锚点**：在提示词中显式声明 `【参考文档开始】...【参考文档结束】` 并要求模型“仅依据上述内容作答”，显著降低幻觉率；  
- 🚫 **勿在流式响应中动态修改提示词**：`stream=true` 时整个 Prompt 在首 chunk 前已固定，运行时无法追加或调整。

## 关联主题页

- [prompt](../guides/prompt.md)
- [start using](../guides/start-using.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)


