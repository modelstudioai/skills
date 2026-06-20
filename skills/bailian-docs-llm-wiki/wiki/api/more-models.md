# [more](more.md) models

百炼平台除了 Qwen 通用大语言模型外，还提供多个专用领域模型的 API 接入，覆盖法律、意图理解、深度研究、机器翻译、OCR 文字提取和界面交互自动化等场景。这些模型均可通过 [DashScope SDK](../concepts/dashscope-sdk.md) 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，但各模型在支持的调用方式、地域可用性和参数结构上存在差异。

## 模型总览

| 模型 | 模型名称（API） | 主要用途 | 调用方式 | 地域限制 |
|------|--------------|---------|---------|---------|
| 通义法睿 | `farui-plus` | 法律咨询、文书生成、合同审查 | [DashScope SDK](../concepts/dashscope-sdk.md)（Python/Java） | - |
| 意图理解 | `tongyi-intent-detect-v3` | 快速意图解析、工具选择 | OpenAI 兼容 / [DashScope SDK](../concepts/dashscope-sdk.md) | - |
| Deep Research | `qwen-deep-research` | 深度研究与分析 | 仅 Python DashScope SDK | 仅华北2（北京） |
| Qwen-MT | `qwen-mt-plus` | 机器翻译 | OpenAI 兼容 / DashScope SDK | 北京、新加坡、弗吉尼亚 |
| Qwen-OCR | `qwen3.5-ocr` | 图片文字提取与结构化 | OpenAI 兼容 / DashScope SDK | 北京、新加坡、弗吉尼亚 |
| GUI-Plus | `gui-plus-2026-02-26` | 界面交互自动化（鼠标键盘操控） | OpenAI 兼容 / DashScope SDK | - |

## 通义法睿（法律大模型）

通义法睿是基于千问基座、经法律行业数据专门训练的垂直领域模型，支持法律问答、法律推理、案情分析、文书生成、法律知识检索和合同条款审查等功能。详见[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

- **模型名称**：`farui-plus`
- **上下文长度**：12k tokens（最大输入 12k，最大输出 2k）
- **计费**：输入+输出 20 元/百万 Token

调用方式与标准 Qwen 模型一致，通过 `dashscope.Generation.call()` 指定 `model="farui-plus"` 即可：

```python
import dashscope

response = dashscope.Generation.call(
    model="farui-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "劳动合同到期不续签，公司需要支付经济补偿金吗？"}
    ],
    result_format="message",
)
```

## 意图理解（Intent Detection）

千问意图理解模型能在百毫秒级时间内解析用户意图并选择合适的工具，适用于需要快速路由的 Agent 场景。详见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

- **模型名称**：`tongyi-intent-detect-v3`
- **上下文长度**：8,192 tokens（最大输入 8,192，最大输出 1,024）
- **计费**：输入 0.4 元/百万 Token，输出 1 元/百万 Token
- **免费额度**：100 万 Token（百炼开通后 90 天内有效）

使用时需在 System Message 中声明 `Response in INTENT_MODE.` 并提供工具描述信息，模型将同时输出意图分类和[函数调用](../concepts/function-calling.md)参数。

## Qwen-Deep-Research（深度研究）

Qwen-Deep-Research 采用两阶段调用流程，适合需要深入分析的研究型任务。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

- **模型名称**：`qwen-deep-research`
- **调用方式**：仅支持 Python DashScope SDK，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)

> **注意**：该模型仅支持华北2（北京）地域，需使用北京地域的 API Key。

**两阶段调用流程：**

1. **第一步（反问确认）**：发送初始研究主题，模型返回澄清式问题以明确研究方向。
2. **第二步（深入研究）**：将第一步的模型回复和用户补充说明一起发送，模型进行深度分析并输出研究结果。

```python
import dashscope

# 第一步：模型反问确认
messages = [{"role": "user", "content": "研究一下人工智能在教育中的应用"}]
responses = dashscope.Generation.call(
    model="qwen-deep-research",
    messages=messages,
    stream=True
)
step1_content = ""
for response in responses:
    content = response.output.get("message", {}).get("content", "")
    if content:
        step1_content += content

# 第二步：深入研究
messages = [
    {"role": "user", "content": "研究一下人工智能在教育中的应用"},
    {"role": "assistant", "content": step1_content},
    {"role": "user", "content": "我主要关注个性化学习和智能评估这两个方面"}
]
responses = dashscope.Generation.call(
    model="qwen-deep-research",
    messages=messages
)
```

## Qwen-MT（机器翻译）

Qwen-MT 是专用翻译模型，通过 `translation_options` 参数指定源语言和目标语言。详见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。

- **模型名称**：`qwen-mt-plus`
- **多地域可用**：北京、新加坡、弗吉尼亚（各地域 API Key 不同）

调用时需要通过 `extra_body`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）传入 `translation_options`，包含 `source_lang`、`target_lang` 和可选的 `domains`（领域提示）：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
    extra_body={
        "translation_options": {
            "source_lang": "Chinese",
            "target_lang": "English"
        }
    }
)
```

可通过 `domains` 字段提供领域上下文以提升专业术语翻译质量。

## Qwen-OCR（文字提取）

Qwen-OCR 是基于视觉语言模型的 OCR 服务，支持从图片中提取文字并进行结构化输出。详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

- **模型名称**：`qwen3.5-ocr`
- **多地域可用**：北京、新加坡、弗吉尼亚

调用方式与多模态模型类似，通过 `messages` 中的 `image_url` 类型传入图片：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "图片URL"}},
            {"type": "text", "text": "请提取图片中的文字信息"}
        ]
    }]
)
```

## GUI-Plus（界面交互自动化）

GUI-Plus 是界面交互专用模型，能够通过分析屏幕截图来执行鼠标点击、键盘输入等操作，适用于 GUI 自动化测试和 RPA 场景。详见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

- **模型名称**：`gui-plus-2026-02-26`
- **核心能力**：识别屏幕元素并输出 `computer_use` 工具调用（包含 `left_click`、`type`、`key`、`mouse_move` 等动作）

调用时需要在 System Message 中定义 `computer_use` 工具签名，并在用户消息中以截图形式传入当前屏幕画面，模型会返回下一步操作指令。可通过 `vl_high_resolution_images: True` 开启高分辨率图像处理。

## 通用注意事项

- **前提条件**：所有模型均需先获取 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`。各地域的 API Key 不同，请在对应地域的百炼控制台获取。
- **限流**：各模型的并发和速率限制不同，具体请参见百炼平台的限流文档。
- **SDK 版本**：使用 DashScope Java SDK 时建议版本 >= 2.12.0；使用 OpenAI SDK 时需要 Node.js >= 18。
- **新加坡地域域名**：新加坡地域推出了新版专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，性能和稳定性更优，建议迁移。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


