# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、深度研究、OCR、界面交互和机器翻译等方向。这些模型在通用能力基础上，通过领域精调、多阶段推理、工具调用、视觉-语言联合建模等技术增强特定任务效果。所有模型均通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用，支持[流式输出](../concepts/streaming.md)、Token 级成本控制与细粒度参数配置。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 适用场景 | 文档引用 |
|----------|------|-----------|------------|-----------|
| `farui-plus` | 法律大模型 | 法律问答、案情分析、文书生成、合同审查、RAG检索增强 | 法律咨询、司法辅助、合规审查 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、[函数调用](../concepts/function-calling.md)决策（INTENT_MODE）、多标签分类 | 智能客服、Agent 工具路由、语音助手前端解析 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 → 网络搜索 → 报告生成）、引用溯源、学习地图构建 | 行业调研、竞品分析、学术预研、长周期知识生产 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | 多模态 OCR 模型 | 高精度文本提取、结构化信息抽取（如车票、合同、表格）、支持 [prompt](../guides/prompt.md) 控制输出格式 | 单据识别、文档数字化、金融票据处理 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-*` | 界面交互模型 | GUI 自动化操作（鼠标/键盘模拟）、截图理解、工具调用（computer_use）、高分辨率图像支持 | RPA 流程自动化、桌面应用测试、无障碍辅助 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen-mt-plus` | 机器翻译模型 | 多语言互译、术语干预（terms）、翻译记忆（tm_list）、领域提示（domains） | 技术文档本地化、多语种内容分发、专业术语一致性保障 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)”，而其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`）在文档中均明确列出多地域（北京/新加坡/弗吉尼亚）支持。该地域与 SDK 限制需严格遵循 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)，不可套用通用规则。

## 关键参数

所有模型共享以下基础参数（部分为 OpenAI 标准参数，部分为百炼扩展）：

- **`model`**：必填字符串，指定模型标识符（如 `"farui-plus"`、`"qwen-mt-plus"`）。
- **`messages`**：必填数组，按角色（`system`/`user`/`assistant`）组织上下文；OCR 和 GUI-Plus 支持 `image_url` 类型 content。
- **`stream`**：布尔值，默认 `false`；设为 `true` 启用流式响应（需客户端逐块解析）。
- **`max_tokens`**：整数，限制输出长度；各模型默认值不同（如 `qwen-mt-plus` 无显式默认，`qwen3.5-ocr` 默认 32768）。
- **`temperature` / `top_p`**：控制生成随机性；建议二者仅选其一，`temperature=0.01` 和 `top_p=0.001` 是多个模型（如 `tongyi-intent-detect-v3`, `gui-plus-*`）的默认值。
- **`seed`**：整数，用于结果复现。

**模型特有关键参数**：
- **OCR 模型**：`min_pixels` / `max_pixels` 控制图像缩放（单位：像素），`vl_high_resolution_images`（GUI-Plus）启用超高分辨率模式。
- **意图模型**：必须在 `system` message 中声明 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.` 才能触发对应输出格式。
- **翻译模型**：`translation_options` 对象（传入 `extra_body` 或顶层）包含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains`。
- **深度研究模型**：`output_format`（`model_detailed_report` / `model_summary_report`）控制报告详略程度。

## 使用方式

### 1. 基础前提
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）：[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- 安装最新版 SDK：Python 或 Java 版 DashScope SDK，或 OpenAI Python/Node.js SDK。
- **强制使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 均明确建议迁移。

### 2. 调用示例（统一风格）
```python
import os
from openai import OpenAI  # 或 from dashscope import Generation

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # OpenAI 兼容
)
# 或
# from dashscope import Generation
# Generation.call(model="farui-plus", ..., api_key=os.getenv("DASHSCOPE_API_KEY"))

response = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "你好"}],
    extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}}
)
print(response.choices[0].message.content)
```

### 3. 特殊流程
- **深度研究（qwen-deep-research）**：必须分两步调用——先发送初始请求获取模型反问，再将反问 + 用户澄清作为第二轮输入。
- **意图识别（tongyi-intent-detect-v3）**：需严格按文档要求构造 `system` message，响应需用正则解析 `<tags>` / `<tool_call>` / `<content>` 区块。
- **GUI 自动化（gui-plus）**：依赖 `computer_use` 工具调用，`system` message 必须包含完整工具定义与 XML 格式规范。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus-*`）明确支持北京/新加坡/弗吉尼亚三地，调用时需匹配对应 `base_url` 和 API Key。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，仅限 Python DashScope SDK；`tongyi-intent-detect-v3` 的 dashscope CLI 不支持 `understanding` 子命令，需用 Python SDK。
- **[流式输出](../concepts/streaming.md)**：所有模型均支持 `stream=True`，但 `qwen-deep-research` 的响应结构含多阶段字段（`phase`, `status`, `extra.deep_research`），需按阶段解析；OCR 和 GUI-Plus 的流式响应需处理 `delta` 内容拼接。
- **图像参数一致性**：`qwen3.5-ocr` 与 `qwen-vl-ocr-*` 系列的 `min_pixels`/`max_pixels` 计算基准不同（32×32 vs 28×28），混用易导致图像失真；`gui-plus` 的 `min_pixels` 默认值（3136）与 `qwen-vl-ocr` 一致，但 `max_pixels` 行为受 `vl_high_resolution_images` 开关影响。
- **成本与限流**：`farui-plus` 的计费单位为每百万 Token（输入 20 元，输出未标），具体限流策略见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；免费额度（如 `tongyi-intent-detect-v3` 的 100 万 Token）仅限开通后 90 天内有效。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)


