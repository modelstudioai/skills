# [more](more.md) models

本页汇总百炼平台上除通义千问主对话模型之外的一组专用模型的 API 参考，涵盖法律、意图理解、深度研究、翻译、OCR、界面交互等场景。这些模型大多通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用，但各模型在地域、协议、请求参数和调用流程上存在差异，使用前需对照本文确认。

## 支持的模型与功能

| 模型名称 | 用途 | 调用方式 | 地域 |
| --- | --- | --- | --- |
| `farui-plus` | 法律行业大模型，支持法律咨询、文书生成、案情分析 | [DashScope SDK](../concepts/dashscope-sdk.md)（Python/Java） | 默认地域 |
| `tongyi-intent-detect-v3` | 意图理解，同时输出意图与[函数调用](../concepts/function-calling.md)信息 | OpenAI 兼容 / DashScope | 默认地域 |
| `qwen-deep-research` | 深度研究，两阶段（反问确认 + 深入研究） | 仅 Python [DashScope SDK](../concepts/dashscope-sdk.md)，仅华北2（北京） | 华北2（北京） |
| `qwen-mt-plus` | 翻译，支持术语干预、翻译记忆、领域提示 | OpenAI 兼容 / DashScope | 北京 / 新加坡 / 美国（弗吉尼亚） |
| `qwen3.5-ocr` | 图像文字提取（OCR）与结构化字段抽取 | OpenAI 兼容 / DashScope | 北京 / 新加坡 / 美国（弗吉尼亚） |
| `gui-plus-2026-02-26` | 界面交互专用模型，通过 `computer_use` 工具操控桌面 GUI | OpenAI 兼容 | 华北2（北京） |

> **注意**：`qwen-deep-research` 当前**仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，且仅支持华北2（北京）地域。如需使用，必须使用该地域的 [API Key](../concepts/api-key.md)。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

## 关键参数

### 通用参数

- `model`（string，必选）：模型名称，取值见上表。
- `messages`（array，必选）：对话消息列表，按顺序排列。
- `stream`（bool，可选）：是否[流式输出](../concepts/streaming-output.md)。`qwen-deep-research` 第一步反问阶段需设为 `true`。

### Qwen-MT 专属参数（`translation_options`）

Qwen-MT 通过 `translation_options`（OpenAI SDK 中放入 `extra_body`）控制翻译行为，详见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)：

- `source_lang`（string）：源语言，可填 `auto` 自动识别。
- `target_lang`（string）：目标语言。
- `terms`（array）：术语干预，元素为 `{"source": "...", "target": "..."}`，强制指定术语译法。
- `tm_list`（array）：翻译记忆，元素为 `{"source": "...", "target": "..."}`，提供历史译文供模型参考，提升一致性。
- `domain_prompt`（string）：领域提示，向模型注入领域上下文（如 IT、金融）。

### Qwen-OCR 专属参数

Qwen-OCR 的 `messages.content` 为[多模态](../concepts/multimodal.md)数组，图像元素支持：

- `min_pixels`（int）：图像最小像素阈值，小于该值会放大，示例 `32 * 32 * 3`（即 3072）。
- `max_pixels`（int）：图像最大像素阈值，超过该值会缩小，示例 `32 * 32 * 8192`（即 8388608）。
- `text` 段：可传入自定义 Prompt；未传入时使用默认 Prompt `Please output only the text content from the image without any additional descriptions or formatting.`。

详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

### GUI-Plus 专属参数

- `vl_high_resolution_images`（bool）：通过 `extra_body` 传入，启用高分辨率图像处理。
- `computer_use` 工具：在 system [prompt](../guides/prompt.md) 中定义，`action` 枚举包括 `key`、`type`、`mouse_move`、`left_click`、`left_click_drag`、`right_click`、`middle_click`、`double_click`、`triple_click`、`scroll`、`hscroll`、`wait`、`terminate`、`answer`、`interact`。屏幕分辨率固定为 1000x1000。

## 使用方式

### 地域与域名

多数模型推荐使用[业务空间](../concepts/workspace.md)专属域名以获得更好性能与稳定性：

- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台「[业务空间](../concepts/workspace.md)详情」页面查看。现有域名（如 `https://dashscope.aliyuncs.com`）仍可正常使用。

> **注意**：各地域的 [API Key](../concepts/api-key.md) 不同，切换地域时需同时更换 [API Key](../concepts/api-key.md) 与 `base_url`。

### 前提条件

- 已开通百炼服务并[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，建议配置到环境变量 `DASHSCOPE_API_KEY`。
- 已[安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（Python/Java）或 OpenAI SDK（Python/Node.js，需 Node.js v18+ 且在 ES Module 环境运行）。

### 调用示例

**通义法睿单轮对话**（DashScope Python SDK）：

```python
import dashscope
messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '我哥欠我10000块钱，给我生成起诉书。'}]
response = dashscope.Generation.call(model="farui-plus", messages=messages)
```

**Qwen-MT 基础翻译**（OpenAI 兼容）：

```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
    extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}})
```

**Qwen-OCR 字段抽取**（OpenAI 兼容）：

```python
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": "https://..."},
         "min_pixels": 32*32*3, "max_pixels": 32*32*8192},
        {"type": "text", "text": "请提取车票图像中的发票号码、车次、起始站..."}]}])
```

**GUI-Plus 界面交互**：在 system [prompt](../guides/prompt.md) 中注入 `computer_use` 工具定义，user 消息中传入截图与指令（如「帮我打开浏览器」），模型返回工具调用 JSON，由调用方执行并截图回传，循环直到 `action=terminate`。

## 限制和注意事项

- **限流**：各模型有独立的限流条件，`farui-plus` 等模型限流详见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **上下文与[计费](../concepts/billing.md)**：`farui-plus` 上下文 12k、最大输入 12k、最大输出 2k，输入成本 20 元/百万 [Token](../concepts/token.md)；`tongyi-intent-detect-v3` 上下文 8,192、最大输入 8,192、最大输出 1,024，输入 0.4 元、输出 1 元/百万 [Token](../concepts/token.md)，开通后 90 天内赠送 100 万 [Token](../concepts/token.md) 免费额度。
- **协议限制**：`qwen-deep-research` 仅支持 Python DashScope SDK；`gui-plus-2026-02-26` 仅在华北2（北京）地域提供。
- **SDK 线程安全**：DashScope Java SDK 的 `Generation` 等对象非线程安全，需自行管理同步机制或及时关闭进程。
- **图像像素阈值**：Qwen-OCR 的 `min_pixels`/`max_pixels` 影响识别精度与耗时，过小会放大、过大会缩小，建议按示例值设置。
- **翻译记忆与术语**：Qwen-MT 的 `terms` 强制覆盖译法，`tm_list` 仅作参考；两者可叠加使用以提升专业领域一致性。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)











