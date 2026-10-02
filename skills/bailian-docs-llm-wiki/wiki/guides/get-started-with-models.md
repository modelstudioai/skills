# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准 API（OpenAI 兼容、DashScope 原生）快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署运维，只需完成账号开通、API Key 配置与 Base URL 设置，即可在数分钟内发起首次推理请求。所有模型均按需计费，新用户可享北京地域专属免费额度。

## 支持的模型/功能

百炼支持覆盖文本、图像、音频、视频、3D、全模态、向量与重排序、决策等多类模型，全部可通过统一 API 接口调用：

- **文本生成**：旗舰模型 `qwen3.8-max`（推荐用于复杂任务）、均衡型 `qwen3.7-plus`（[文档明确标注为多数场景的推荐选择](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）、高性价比 `qwen3.8-flash`；同时支持 DeepSeek、Kimi、GLM、MiniMax 等第三方模型。
- **多模态能力**：`qwen3.8-omni-flash`（离线音视频分析+文本生成）、`qwen3.8-omni-flash-realtime`（实时音视频对话）、`qwen-image-3.0-pro`、`wan3.0-video` 等。
- **专业能力**：语音识别（ASR）、语音合成（TTS）、音乐生成、3D 生成（Tripo）、嵌入向量（`qwen3.7-text-embedding`）与重排序（`qwen3.7-text-rerank`）。
- **结构化决策**：`decision-model-preview` 支持一次前向输出分类、评分与置信度。

> **注意**：文档 3 中列出的 `kimi/kimi-k3` 和 `kimi-k3` 为同一模型的两种命名形式，实际调用时应使用控制台模型市场展示的完整标识符（如 `kimi/kimi-k3`），避免因路径解析歧义导致 404 错误。

完整模型列表请参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)，各模型上下文长度、支持地域及详细能力以控制台实时信息为准。

## 关键参数

调用模型必需且关键的参数包括：

- **`model`**：字符串，指定模型 ID（如 `"qwen3.7-plus"`）。该参数在请求体中传入，**不依赖 API Key 创建时的权限配置**（除非显式启用了“访问模型范围”开关）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。
- **`base_url`**：必须与所选地域、计费方案（按量付费 / [Token](../concepts/token.md) Plan / Coding Plan）严格匹配。例如：
  - 华北2（北京）按量付费 + 业务空间专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡按量付费 + DashScope 域名：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
  - Coding Plan（仅限交互式工具）：`https://coding.dashscope.aliyuncs.com/v1`
  详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **`api_key`**：从 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建，**不同地域的 API Key 不通用**，且需与 `base_url` 所属计费方案一致（如 Coding Plan 的 Key 不能用于按量付费域名）。
- **`workspace_id`**：仅当使用业务空间专属域名时必需，需在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace) 页面获取。

## 使用方式

1. **开通与准备**  
   - 注册阿里云账号并完成实名认证；
   - 开通百炼服务（主账号操作）；
   - 创建 API Key，并按需配置模型访问范围；
   - （若使用业务空间专属域名）创建业务空间并记录 `WorkspaceId`。

2. **环境配置**  
   - 将 `DASHSCOPE_API_KEY` 设为环境变量（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 推荐系统属性设置），避免硬编码 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

3. **代码调用（OpenAI SDK 示例）**  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
   )
   response = client.chat.completions.create(
       model="qwen3.7-plus",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   print(response.choices[0].message.content)
   ```

4. **其他方式**  
   - `curl`：直接发送 HTTP POST 请求（见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）；
   - DashScope Python SDK：适用于多模态等非 OpenAI 标准接口场景；
   - 可视化 Chatbox：适合无编程经验的快速体验。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国等）的 API Key、Base URL、模型列表、监控数据完全独立，**严禁跨地域混用** [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **限流机制**：
  - 按主账号维度合并计算所有子账号、业务空间、API Key 的调用量；
  - 分 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗，含输入+输出）双重限制；
  - `qwen3.8-max`、`qwen3.8-flash` 等模型采用 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值随月消费档位自动提升，但 RPM 通常充足；
  - 触发限流返回 `429 Too Many Requests`，恢复时间通常 ≤1 分钟。
- **域名与计费绑定**：DashScope 域名（`dashscope.aliyuncs.com`）将于 2026 年 9 月 30 日起停止支持新特性，**生产环境务必迁移至业务空间专属域名** [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **安全与合规**：按量付费与 [Token](../concepts/token.md) Plan 团队版默认不使用客户数据训练模型；但 **Token Plan 个人版与 Coding Plan 明确允许使用输入/输出数据优化服务**，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的“常见问题”章节。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


