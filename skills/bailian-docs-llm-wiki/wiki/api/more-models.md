# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、OCR、界面交互、机器翻译和深度研究等方向。这些模型在通用大模型基础上进行了领域精调或架构优化，具备更强的专业能力与任务适配性。所有模型均通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，支持流式/非[流式输出](../concepts/streaming-output.md)、多轮对话及参数精细化控制。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 适用场景 | 文档引用 |
|----------|------|-----------|------------|-----------|
| `farui-plus` | 法律大模型 | 法律问答、案情分析、文书生成、合同审查、RAG检索增强 | 法律咨询、司法辅助、合规审查 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策（INTENT_MODE）、单标签分类 | 智能客服、语音助手、多工具调度系统 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen3.5-ocr` / `qwen-vl-ocr-*` | 多模态OCR模型 | 高精度文本提取、结构化信息抽取（如车票、合同、证件） | 票据识别、文档数字化、表单自动化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-*` | 界面交互模型 | GUI操作理解、屏幕内容解析、鼠标/键盘动作规划（`computer_use`工具） | RPA自动化、桌面智能代理、无障碍交互 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen-mt-plus` | 机器翻译模型 | 多语言互译、术语干预、翻译记忆（TM）、领域提示（IT/医疗/金融等） | 技术文档本地化、实时字幕、跨语言知识库构建 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究模型 | 自动反问澄清、网络搜索、多源信息整合、生成结构化研究报告 | 行业调研、竞品分析、学术预研、政策解读 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |

> **注意**：`qwen-deep-research` **仅支持华北2（北京）地域且仅限 Python DashScope SDK 调用**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)；而其他模型（如 `qwen-mt-plus`、`gui-plus-*`）在多个地域均提供 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)支持 —— 此差异在[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)与[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)中明确体现，开发时需严格按模型约束选型。

## 关键参数

所有模型共享以下通用参数（部分为 OpenAI 标准参数，部分为百炼扩展参数）：

- **`model`**：必填字符串，指定模型标识符（如 `"farui-plus"`、`"qwen-mt-plus"`）。
- **`messages`**：必填数组，按角色（`system`/`user`/`assistant`）组织上下文；视觉模型（OCR、GUI-Plus）支持 `image_url` 类型内容。
- **`stream`**：布尔值，默认 `false`；设为 `true` 启用流式响应（需客户端逐块解析）。
- **`max_tokens`**：整数，限制输出长度；各模型默认值不同（如 `qwen-mt-plus` 无显式默认，`qwen-deep-research` 默认 `model_detailed_report` 约6000 Token）。
- **`temperature` / `top_p`**：控制生成随机性，建议二选一设置；默认值普遍较低（如 `0.01`），适合确定性任务。
- **`seed`**：整数，用于结果可复现；取值范围 `[0, 2^31−1]`。
- **`stop`**：字符串或数组，指定终止词。

**模型特有参数**：
- OCR 模型（`qwen3.5-ocr`）：`min_pixels`、`max_pixels` 控制图像分辨率缩放；`vl_high_resolution_images`（GUI-Plus）启用高分辨率处理。
- 翻译模型（`qwen-mt-plus`）：`translation_options` 对象内含 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）、`domains`（领域提示）。
- 意图模型（`tongyi-intent-detect-v3`）：依赖 `System Message` 中的 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.` 触发对应模式。
- 深度研究模型（`qwen-deep-research`）：`output_format` 指定 `model_detailed_report` 或 `model_summary_report`。

## 使用方式

### 基础调用流程
1. **准备环境**：安装最新版 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 或 OpenAI SDK；获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）。
2. **配置域名**：**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性；旧域名（`dashscope.aliyuncs.com`）仍可用但不推荐 —— 此要求在[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)等多篇文档中反复强调。
3. **构造请求**：按模型要求组织 `messages`（注意 OCR/GUI-Plus 的 `image_url` 结构、意图模型的 System Prompt 格式），传入必要参数。
4. **处理响应**：解析 `output.choices[0].message.content`（非流式）或迭代流式响应块；深度研究模型需按 `phase` 字段区分研究阶段（`ResearchPlanning`/`WebResearch`/`answer`）。

### 示例：OCR 提取车票信息（OpenAI 兼容）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.jpg"}},
            {"type": "text", "text": "提取发票号码、车次、起始站、终点站、发车时间、座位号、票价"}
        ]
    }]
)
print(completion.choices[0].message.content)
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR、GUI-Plus、MT 等模型在华北2、新加坡、美国（弗吉尼亚）等多地可用，但需匹配对应地域的 `base_url` 和 API Key。
- **限流策略**：所有模型受统一限流规则约束，详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；高频调用需申请配额提升。
- **输入格式约束**：
  - OCR/GUI-Plus 模型要求图片 URL 可公开访问（或使用 Base64 Data URL），不支持本地文件直传（需先上传至 OSS 或公网）。
  - 意图模型的 `INTENT_MODE` 输出含 `<tags>`/<tool_call>/`<content>` XML 标签，需用正则解析（见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)示例）。
- **成本与免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度；其他模型按实际 Token 消耗计费（如 `farui-plus` 输入 20元/百万 Token）。
- **SDK 线程安全**：DashScope Java SDK 中 `Generation` 等对象**非线程安全**，需复用实例并自行管理同步（见[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)说明）。
- **模型输出解析**：深度研究模型响应结构复杂，`output.message.phase` 和 `output.message.status` 是判断当前执行阶段的关键字段；直接读取 `content` 可能为空（如 `ResearchPlanning` 阶段）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)


