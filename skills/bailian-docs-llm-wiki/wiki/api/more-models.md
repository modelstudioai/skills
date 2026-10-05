# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、OCR识别和GUI自动化等方向。这些模型在通用基座上进行了领域精调或架构增强，具备更强的专业能力与任务适配性。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，需注意地域限制、API 域名迁移及参数兼容性。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 地域支持 | 文档参考 |
|----------|------|-----------|-----------|-----------|
| `farui-plus` | 法律大模型 | 法律咨询、文书生成、案情分析、合同审查、RAG检索增强 | 华北2（北京）、新加坡、中国香港 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策、多标签分类 | 华北2（北京）、新加坡、中国香港 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 + 网络检索+报告生成） | **仅华北2（北京）** | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr`, `qwen-vl-ocr-*` | 多模态OCR模型 | 图像文本提取、结构化信息抽取（如车票、合同）、支持自定义Prompt | 华北2（北京）、新加坡、美国（弗吉尼亚） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus`, `gui-plus-2026-02-26` | GUI自动化模型 | 基于截图的桌面操作（点击、输入、等待、终止），支持高分辨率图像与思考模式 | 华北2（北京）、新加坡 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而其他模型（如 `farui-plus`、`tongyi-intent-detect-v3`）在文档中均明确列出多地域支持，二者存在地域覆盖范围不一致。请严格按模型文档要求配置 `base_url` 或 `base_http_api_url`。

## 关键参数

所有模型共用以下基础参数（部分为可选）：
- `model`: 必填，模型标识符（如 `"farui-plus"`）；
- `messages`: 必填，对话消息数组，支持 `system`/`user`/`assistant` 角色；
- `result_format`（DashScope）或 `response_format`（OpenAI）: 推荐设为 `"message"` 以获取结构化输出；
- `stream`: 布尔值，启用流式响应（`True`/`true`）；
- `max_tokens`: 输出长度上限，各模型默认值不同（如 `qwen-deep-research` 默认 `model_detailed_report` 约6000 Token，`qwen3.5-ocr` 默认32768）；
- `temperature` / `top_p`: 控制生成随机性，默认值普遍较低（`0.01`），生产环境建议保持默认。

**模型特有参数**：
- `qwen-deep-research`: 支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）；
- `qwen-vl-ocr-*` 和 `gui-plus`: 支持图像缩放控制 `min_pixels`/`max_pixels`，且像素-Token换算规则因模型版本而异（`32×32` vs `28×28`）；
- `gui-plus`: 支持 `vl_high_resolution_images`（覆盖 `max_pixels`）和 `enable_thinking`（返回 `reasoning_content`）；
- `tongyi-intent-detect-v3`: 要求 `system` 消息中显式包含 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.` 指令。

## 使用方式

### 1. 基础调用（Python DashScope SDK）
```python
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"  # 注意替换 WorkspaceId

response = dashscope.Generation.call(
    model="farui-plus",
    messages=[{"role": "user", "content": "生成一份离婚协议书"}],
    result_format="message"
)
```

### 2. [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（推荐新域名）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 各地域名见[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
)
response = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "https://..."}}]}]
)
```

### 3. 特殊流程示例
- **`qwen-deep-research` 两阶段调用**：先发起研究请求获取澄清问题，再将用户回答与原始请求组合为多轮 `messages` 进行第二步深入分析；
- **`tongyi-intent-detect-v3` 工具调用模式**：`system` 消息需嵌入工具 JSON Schema 并声明 `Response in INTENT_MODE.`，响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构；
- **`gui-plus` 多模态操作**：`messages` 中 `user` 内容为 `[{"type": "image_url", ...}, {"type": "text", "text": "..."}]`，系统提示需定义 `<tools>` 和响应格式规则。

## 限制和注意事项

- **地域强约束**：`qwen-deep-research` 仅支持华北2（北京），调用其他地域 endpoint 将失败；其余模型虽支持多地域，但必须使用对应地域的专属域名（如 `cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐；
- **SDK 支持差异**：`qwen-deep-research` **仅支持 Python SDK**，Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)暂不可用；`tongyi-intent-detect-v3` 的 `dashscope CLI` 不支持 `understanding` 子命令；
- **成本与限流**：`farui-plus` 的输入/输出成本为 20 元/百万 Token；`tongyi-intent-detect-v3` 提供 100 万 Token 免费额度（90 天）；所有模型限流策略详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **安全实践**：API Key **必须配置到环境变量**（如 `DASHSCOPE_API_KEY`），禁止硬编码或明文写入代码，Java SDK 中 `Generation` 对象非线程安全，需自行管理同步；
- **图像处理细节**：`qwen-vl-ocr-*` 和 `gui-plus` 的 `min_pixels`/`max_pixels` 默认值与取值范围因模型版本而异，务必查阅对应文档确认（如 `qwen-vl-ocr` 系列旧版默认 `min_pixels=3136`，新版为 `3072`）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


