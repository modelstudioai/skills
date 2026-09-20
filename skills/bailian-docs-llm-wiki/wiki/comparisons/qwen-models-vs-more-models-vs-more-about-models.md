# 通义千问模型、扩展模型与模型管理能力对比

本文档面向百炼平台开发者，系统对比通义千问系列基础模型、垂直领域扩展模型及平台级模型管理能力三大技术路径的核心差异，旨在帮助团队基于业务需求（如响应延迟、多模态支持、工具链集成、地域合规、异步任务调度等）做出高效、可扩展的技术选型决策。对比依据为当前（2024年Q4）百炼平台正式发布的 API 文档与 SDK 行为规范。

## 关键维度对比

| 维度 | 通义千问基础模型（Qwen 系列） | 垂直领域扩展模型（More Models） | 模型管理能力（More About Models） |
|------|------------------------------|----------------------------------|-----------------------------------|
| **输入格式** | • OpenAI 兼容：`messages` 数组（含 `role`/`content`）<br>• Anthropic 兼容：`messages` + `system`（支持 `cache_control`）<br>• DashScope 原生：`input`（文本）或 `input.multimodal`（图像/视频） | • 统一兼容 OpenAI/DashScope 输入格式<br>• 多模态模型（OCR、GUI-Plus）支持 `image_url` 数组输入<br>• 意图识别模型需 `system` 中显式声明 `Response in INTENT_MODE.` | • 不改变输入格式语义<br>• 异步任务：输入同同步模型，但通过 `task_id` 解耦执行与获取<br>• 文件上传：需先调用 `/uploads` 获取策略，再传 `oss://` URL 到 `messages.content` |
| **输出格式** | • Chat API：标准 OpenAI `choices[0].message.content`<br>• Responses API：增强结构化字段（`output_text.delta`, `tool_calls`, `session_id`）<br>• Anthropic：`content` 数组 + `usage` + `cache_creation_input_tokens` | • 统一返回 `choices[0].message.content`（`result_format="message"`）<br>• Deep Research 输出含 `phase`（`"WebResearch"`/`"answer"`）、`status` 字段<br>• GUI-Plus 可选返回 `reasoning_content`（需 `enable_thinking=true`） | • 同步模型：输出格式不变<br>• 异步模型：返回 `task_id`，结果需轮询 `/tasks/{id}` 或监听事件总线<br>• 事件通知 payload 含 `data.task_id`, `data.status`, `data.output.results`（混合成功/失败项） |
| **支持模型** | • Qwen 全系：`qwen3.8-*`、`qwen-plus`、`qwen-flash`、`qwen-vl-*`、`qwen-omni-*`、`qwen-coder-*` 等<br>• 部分第三方模型（DeepSeek、GLM、Kimi），功能受限 | • 法律：`farui-plus`<br>• 意图理解：`tongyi-intent-detect-v3`<br>• 深度研究：`qwen-deep-research`（仅北京）<br>• OCR：`qwen3.5-ocr`、`qwen-vl-ocr-*`<br>• GUI 自动化：`gui-plus-*` | • 不绑定具体模型<br>• 支持所有同步/异步模型（含 Qwen 系列与扩展模型）<br>• 异步模型示例：`wanx2.1-t2i-turbo`（文生图）、`paraformer-16k-1`（语音转写） |
| **API 端点** | • 必须使用业务空间专属域名：<br> `https://{WorkspaceId}.{region}.maas.aliyuncs.com`<br>• 协议路由：<br> Chat：`/v1/chat/completions`<br> Responses：`/v1/responses`<br> Anthropic：`/v1/messages`<br> DashScope：`/text-generation/generation` 等 | • 同样强制使用业务空间专属域名<br>• 接口路径与基础模型一致（如 `/v1/chat/completions`）<br>• `qwen-deep-research` 仅支持 DashScope SDK 调用（无 OpenAI 兼容端点） | • 异步任务管理：`/api/v1/tasks`（创建/查询/取消）<br>• 临时凭证：`/api/v1/credentials/temporary`<br>• 文件上传：`/api/v1/uploads?action=getPolicy`<br>• 所有端点均需匹配业务空间域名与地域 |
| **计费方式** | • 按 token 计费（输入+输出）<br>• Qwen-VL/Qwen-Omni 等多模态模型按像素数折算 token（`min_pixels`/`max_pixels` 影响计费）<br>• `vl_high_resolution_images=true` 触发更高像素上限，对应更高费用 | • 同样按 token 计费，但模型单价独立定价<br>• OCR 类模型默认 `max_tokens=32768`，显著高于通用模型（如 `qwen-plus` 默认 8192）<br>• `qwen-deep-research` 按两阶段流程计费（反问+检索+生成） | • 临时 API Key：不额外计费，继承主 Key 权限与配额<br>• 异步任务：按最终完成的模型调用计费（非任务创建次数）<br>• 文件上传：免费，但 `oss://` URL 48 小时后失效，长期存储需自建 OSS |
| **典型场景** | • 通用对话助手、内容创作、代码生成<br>• 多轮客服会话（配合 `previous_response_id`）<br>• 结构化 JSON 输出（`format.json_schema`）<br>• 视频理解（`max_frames` 控制帧数） | • 法律文书生成与审查（`farui-plus`）<br>• 智能客服意图识别与工具路由（`tongyi-intent-detect-v3`）<br>• 自动化桌面操作（`gui-plus-*`）<br>• 发票/合同 OCR 结构化提取（`qwen3.5-ocr`） | • 长耗时任务（图像生成、视频处理、语音转写）<br>• 多租户隔离（子业务空间 + 临时凭证）<br>• 高并发连接复用（Java/Python SDK 连接池）<br>• 生产环境文件安全流转（OSS 临时 URL） |

## 各方案适用场景建议

### ✅ 选择通义千问基础模型（Qwen 系列）当：
- 业务以通用大语言能力为核心（如智能问答、文案润色、编程辅助）；
- 需快速迁移现有 OpenAI 应用，且对工具链、多轮缓存、结构化输出有明确需求（优先选 Responses 或 Anthropic 协议）；
- 场景涉及视频理解、高分辨率图像处理，需精细控制 `fps`/`max_frames`/`vl_high_resolution_images`；
- 要求跨地域部署（北京、新加坡、香港、东京等均支持全模型）。

### ✅ 选择垂直领域扩展模型（More Models）当：
- 业务存在强领域约束：法律合规、金融票据识别、GUI 自动化测试、实时意图决策；
- 需要毫秒级低延迟响应（如 `tongyi-intent-detect-v3` 百毫秒级分类）；
- 接受地域限制：`qwen-deep-research` 仅北京可用，需评估部署架构；
- 要求模型行为高度确定：如 OCR 模型对车票/合同字段的结构化抽取精度优于通用 Qwen-VL。

### ✅ 选择模型管理能力（More About Models）当：
- 存在长耗时任务（>5 秒），需避免 HTTP 请求超时，且要求结果可靠投递（推荐事件驱动回调）；
- 构建多租户 SaaS 平台，需子业务空间隔离权限、配额与计费；
- 面临高并发调用压力（>100 QPS），需连接复用与连接池优化；
- 处理用户上传图片/音视频，需安全、临时、可审计的文件流转机制（OSS 临时 URL + 时效管控）。

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 关键动作 |
|----------|-----------|-----------|
| **“我已有 OpenAI 应用，想无缝切换到百炼”** | ✅ Qwen 基础模型 + OpenAI 兼容 Chat API | 替换 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/v1`；检查 `temperature` 范围（Anthropic 协议为 `[0,2)`）；启用 `stream` 时解析 `response.output_text.delta` |
| **“我需要让模型联网搜索并生成报告”** | ✅ Qwen 基础模型 + Responses API | 在 `messages` 中启用 `previous_response_id`；配置 `tool_choice="auto"`；设置 `x-dashscope-session-cache: enable` 实现上下文缓存 |
| **“我要做法律咨询 App，需精准引用法条”** | ✅ `farui-plus` 扩展模型 | 使用 `messages = [{"role":"user","content":"请根据《民法典》第XXX条分析..."}]`；确保地域为北京/新加坡/香港；启用 `stream=True` 获取渐进式输出 |
| **“我的客服系统需实时识别用户意图并调用工具”** | ✅ `tongyi-intent-detect-v3` 扩展模型 | `system` message 必须包含 `Response in INTENT_MODE.`；`messages[0].content` 为用户原始输入；解析响应中的 `<tags>`/`<content>` 三段式结构 |
| **“我要批量处理用户上传的 PDF 合同，提取甲方/乙方/金额”** | ✅ `qwen3.5-ocr` + 模型管理能力 | 先调用 `/api/v1/uploads` 获取策略并上传至 OSS；构造 `messages` 含 `image_url: "oss://..."`；设置 `max_tokens=32768` 防截断；生产环境应将 OSS bucket 设为私有并签名访问 |
| **“我开发的是 AI 绘画工具，生成一张图需 15 秒”** | ✅ 异步任务管理能力 + `wanx2.1-t2i-turbo` | 调用 `/api/v1/tasks` 创建任务；配置 HTTP 回调地址监听 `dashscope:System:AsyncTaskFinish`；收到事件后立即查 `/api/v1/tasks/{id}` 获取结果 URL；禁用轮询，规避 20 QPS 限流 |
| **“我是平台方，需为不同客户分配独立模型配额”** | ✅ 子业务空间 + 临时 API Key | 在控制台创建子空间 → 分配 `farui-plus` 等模型权限 → 为客户生成 `expire_in_seconds=3600` 的临时 Key；所有调用均走子空间专属域名 |

> **重要提醒**：  
> - **域名迁移是强制前提**：所有方案均必须使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，旧域名 `dashscope.aliyuncs.com` 已不推荐，部分新模型（如 `qwen-deep-research`）仅支持新域名。  
> - **SDK 版本需匹配**：`qwen-deep-research` 仅支持 Python DashScope SDK（v1.20.0+），Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不可用。  
> - **地域一致性不可妥协**：API Key 地域、业务空间地域、Endpoint 地域、事件总线地域必须严格一致，否则返回 `InvalidRegionId` 或 `Forbidden.AccessDenied`。  
> - **安全红线**：`oss://` 临时 URL 有效期仅 48 小时，严禁用于生产环境长期服务；敏感业务应使用自有 OSS Bucket + STS 临时凭证。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [more about models](../api/more-about-models.md)


