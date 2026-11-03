# get started with models

阿里云百炼平台提供统一的模型服务入口，支持通过 OpenAI 兼容 API 或 DashScope SDK 快速调用文本、视觉、语音、视频、全模态及向量模型。开发者无需部署模型即可完成首次推理，所有模型均按需计费，免费额度可立即启用。核心流程包括：开通服务 → 获取 API Key → 选择模型 → 发送请求。

## 支持的模型与功能

百炼支持[多模态](../concepts/multi-modal.md)模型，覆盖文本生成、视觉理解、图像/视频生成、语音识别与合成、全模态交互、[向量嵌入](../concepts/vector-embedding.md)与重排序等场景。主流模型包括：

- **文本生成**：`qwen3.8-max`（旗舰效果）、`qwen3.7-plus`（均衡）、`qwen3.8-flash`（极速高性价比），以及 `deepseek-v4-pro-0813`、`kimi/kimi-k3`、`glm-5.3` 等第三方模型  
- **视觉理解**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-omni-flash` 等支持图文输入与结构化输出  
- **图像/视频生成**：`qwen-image-3.0-pro`、`wan3.0-video`、`happyhorse-1.1-t2v` 等  
- **语音处理**：`qwen-audio-3.1-asr-flash`（ASR）、`qwen-audio-3.1-tts-plus`（TTS）、`qwen-audio-3.1-realtime-plus`（S2S）  
- **向量与检索**：`qwen3.7-text-embedding-flash`、`qwen3.7-text-rerank`  
- **全模态**：`qwen3.8-omni-flash`（离线[多模态](../concepts/multi-modal.md)理解与生成）、`qwen3.8-omni-flash-realtime`（实时音视频对话）  

完整模型列表请参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。各模型能力细节（如是否支持工具调用、思考模式、结构化输出等）需查阅对应模型文档，例如 [qwen3.8-omni-flash](../../raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash.md) 明确标注其全模态能力边界。

> **注意**：文档 1 中列出的 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-flash` 模型名与文档 3 中的 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-flash` 一致，但文档 3 新增了 `deepseek-v4.1-flash`、`MiniMax-M3.1-Flash` 等更多第三方模型，且明确区分了“视觉理解”“决策模型”等子类。实际开发中应以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档为准，该文档结构更完整、更新更及时。

## 关键参数

调用模型时需关注以下通用参数（部分为必填）：

- `model`：模型 ID，**必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称完全一致**（大小写敏感、无空格、不混用开源社区命名，如应填 `qwen3.7-plus`，而非 `Qwen/Qwen3.7-Plus`）  
- `messages`：对话消息数组，每条含 `role`（`user`/`assistant`/`system`/`tool`）和 `content`（字符串或结构化数组）。`content` 字段为必填，不可为空或非字符串类型  
- `temperature`：取值范围 `[0.0, 2.0)`，控制输出随机性  
- `top_p`：取值范围 `(0.0, 1.0]`，核采样阈值  
- `max_tokens`：最大输出 token 数，不得超过模型文档中声明的上限  
- `stream`：布尔值，设为 `true` 启用流式响应；**部分模型（如 `qwen-audio-3.1-realtime-plus`）强制要求 `stream=true`**  
- `enable_thinking`：开启思考链模式，但需满足约束：仅支持[流式输出](../concepts/streaming-output.md)（`stream=true`）、`incremental_output=true`、`result_format="message"`，且与 `response_format="json_object"` 互斥  
- `response_format`：结构化输出格式，仅支持 `{"type": "json_object"}`，且提示词中必须包含 `json` 关键词  

其他参数（如 `seed`、`repetition_penalty`、`stop`）的合法范围详见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 文档中的参数校验说明。

## 使用方式

### 1. 前置准备
- 注册阿里云账号并完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)  
- 开通阿里云百炼服务：访问 [模型市场](https://bailian.console.aliyun.com/model/market)，同意协议后自动开通  
- 获取 API Key：前往 [API Key 管理页](https://bailian.console.aliyun.com/model/settings/api-key)，创建密钥并配置权限（可选限制可调用模型范围）  
- （可选）获取业务空间 ID（WorkspaceId）：若使用华北2（北京）、新加坡、日本（东京）、德国（法兰克福）或中国香港地域，Base URL 中需填入 WorkspaceId，可在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace) 查看  

### 2. 配置与调用
推荐将 `DASHSCOPE_API_KEY` 配置为环境变量（避免硬编码），支持 Linux/macOS/Windows 全平台配置方法详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。  

**OpenAI 兼容 API 示例（Python）：**  
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换 {WorkspaceId}
)
response = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(response.choices[0].message.content)
```

**DashScope SDK 示例（Python）：**  
```python
import dashscope
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",  # 替换 {WorkspaceId}
    region="cn-beijing"
)
response = client.multimodal.chat.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": [{"text": "你是谁？"}]}]
)
print(response.output_text)
```

完整代码示例与 Node.js/JavaScript 版本见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 限制和注意事项

### 限流策略
- **账号级聚合限流**：按主账号维度统计，所有 RAM 子账号、业务空间、API Key 的调用量合并计算  
- **模型独立限流**：不同模型配额互不影响  
- **动态限流模型**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.8-omni-flash` 等采用动态 TPM 限流，额度随百炼月消费金额分档调整（如华北2 北京地域，消费 ¥10万~¥100万档对应 `qwen3.8-max` TPM 为 1000万），详情见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)  
- **静态限流模型**：多数模型有固定 RPM/TPM 上限（如 `qwen3.7-plus` 在华北2 为 30,000 RPM / 5,000,000 TPM），详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表格  
- **触发限流响应**：返回 HTTP 429 错误，错误码如 `Throttling.RateQuota`。恢复通常在一分钟内，建议实现指数退避重试  

### 其他关键限制
- **免费额度耗尽**：返回 403 错误（`AccessDenied`），非限流；可通过开通“免费额度用完即停”避免意外扣费  
- **模型未开通**：调用前需在 [模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market) 手动开通目标模型，否则报 `ModelNotFound` 或 `invalid_parameter_error`  
- **地域与 URL 匹配**：Base URL 必须与模型部署地域一致（如北京地域用 `cn-beijing.maas.aliyuncs.com`），且 WorkspaceId 必须正确填写，否则触发 `BailianGateway.Workspace.NotAuthorised`  
- **[Token](../concepts/token.md) 长度限制**：输入 `messages` 总长度或 `max_tokens` 超出模型上限时，报 `InternalError.Algo.InvalidParameter`，需按模型文档调整  

> **注意**：文档 6 的 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 明确指出“充值不改变 RPM/TPM 限流阈值”，而文档 5 的 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 强调“限流值按月消费金额分档调整”。二者逻辑一致：限流是消费驱动的软约束，与账户余额无关。开发者应优先通过提升消费档位或申请提额来扩容，而非依赖充值。

## 来源文档

- [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


