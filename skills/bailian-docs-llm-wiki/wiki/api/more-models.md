# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、OCR识别和GUI自动化等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持开发者快速构建高精度、低延迟的专业应用。所有模型均通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，需配合业务空间专属域名以获得最佳性能。

## 支持的模型/功能

当前 `more models` 类别下支持以下核心模型：

- **通义法睿（`farui-plus`）**：法律行业专用大模型，支持法律咨询、案情分析、文书生成、合同审查等功能，基于千问基座经法律数据精调与RAG增强 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与工具调用决策模型，支持两种模式：① 同时输出意图标签与[函数调用](../concepts/function-calling.md) JSON；② 仅输出预定义意图标签（如 `alarm_set`），适用于对话系统路由与智能助手 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究的专用模型，自动执行研究规划、网络搜索、信息整合与报告生成，**仅支持华北2（北京）地域及 Python SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR 系列（如 `qwen3.5-ocr`, `qwen-vl-ocr-latest`）**：多分辨率图像文字识别模型，支持文本提取、结构化信息抽取（如车票字段）、自定义 Prompt 控制输出格式，兼容 OpenAI 接口与 DashScope API。
- **GUI-Plus（`gui-plus-2026-02-26` 等）**：面向桌面 GUI 自动化的视觉-动作联合模型，可解析截图、生成操作指令（如 `left_click`, `type`），并支持高分辨率图像输入与可选思考链输出。

> **注意**：文档 4 和文档 5 均提及 `min_pixels` 默认值为 3136，但文档 4 明确区分了不同模型版本的像素换算基准（`28×28` vs `32×32`），而文档 5 未说明适用模型范围。实际使用时请以 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中按模型版本划分的像素规则为准。

## 关键参数

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 模型标识符，必填 | 全部 | 如 `"farui-plus"`, `"tongyi-intent-detect-v3"`, `"qwen-deep-research"` |
| `messages` | 对话消息数组，含 `role`（`user`/`system`/`assistant`）与 `content` | 全部 | OCR 与 GUI-Plus 支持 `image_url` 类型 content；`qwen-deep-research` 要求两阶段 message 结构 |
| `result_format` / `response_format` | 输出格式，常用 `"message"` | `farui-plus`, `tongyi-intent-detect-v3` | DashScope SDK 使用 `result_format`；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)通常无需显式设置 |
| `output_format` | Qwen-Deep-Research 专用，控制报告详略程度 | `qwen-deep-research` | 取值：`"model_detailed_report"`（默认，~6000 [Token](../concepts/token.md)）或 `"model_summary_report"`（~1500–2000 [Token](../concepts/token.md)） |
| `min_pixels` / `max_pixels` | 图像预处理像素阈值，影响 OCR/GUI-Plus 输入质量 | `qwen3.5-ocr`, `gui-plus` | 默认值因模型版本而异，详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `vl_high_resolution_images` | GUI-Plus 专用开关，启用后忽略 `max_pixels` 并固定上限为 12845056 像素 | `gui-plus-*` | 需通过 `extra_body` 传入（Python SDK）或顶层参数（HTTP/Node.js） |

## 使用方式

### 基础调用流程
1. **配置环境**：获取 API Key 并设为环境变量 `DASHSCOPE_API_KEY`；[安装最新版 DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK。
2. **选择域名**：**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高稳定性与性能 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
3. **构造请求**：
   - 法律/意图/研究类模型：使用标准 `messages` 数组，注意 `system` 角色对意图识别的必要性（如 `Response in INTENT_MODE.`）；
   - OCR/GUI-Plus：`user` 消息的 `content` 必须为数组，包含 `{"type": "image_url", "image_url": {"url": "..."} }` 及可选 `text` prompt；
   - Qwen-Deep-Research：必须分两步调用，第一步获取模型反问，第二步将反问+用户澄清作为上下文提交。

### 示例：意图识别（DashScope）
```python
from dashscope import Generation
import json

tools = [{"name": "get_weather", "description": "查询天气", "parameters": {...}}]
system_prompt = f"""You are Qwen... tools: {json.dumps(tools)}\nResponse in INTENT_MODE."""

response = Generation.call(
    model="tongyi-intent-detect-v3",
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": "杭州天气"}],
    result_format="message"
)
```

### 示例：OCR 提取（OpenAI 兼容）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://..."}},
            {"type": "text", "text": "提取发票号码、金额、日期"}
        ]
    }]
)
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**，其他地域调用将失败；OCR 与 GUI-Plus 支持北京、新加坡、美国（弗吉尼亚）三地，但需匹配对应 `base_url` [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **SDK 限制**：`qwen-deep-research` **暂不支持 Java SDK 与 OpenAI 兼容接口**，仅可通过 Python DashScope SDK 调用；`tongyi-intent-detect-v3` 的 `understanding` 子命令在 CLI 中不可用，需用 Python SDK [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **[流式输出](../concepts/streaming-output.md)**：`farui-plus` 支持 `stream=True` + `incremental_output=True`；OCR/GUI-Plus 使用 OpenAI 兼容接口时需设 `stream=True` 并处理 SSE 数据块；`qwen-deep-research` 流式响应中 `phase` 字段标识当前阶段（`ResearchPlanning`, `WebResearch`, `answer`），需按阶段解析 `content` 与 `extra.deep_research`。
- **成本与限流**：各模型计费单位为百万 [Token](../concepts/token.md)，具体价格见各文档表格；全局限流策略参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)，法睿模型明确引用该文档 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **安全实践**：API Key **必须优先配置到环境变量**，避免硬编码；Java SDK 中 `Generation` 对象非线程安全，需复用并自行管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


