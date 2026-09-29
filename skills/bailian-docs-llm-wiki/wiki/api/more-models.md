# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、OCR识别与GUI自动化等方向。这些模型在通用基座上进行了领域精调或架构增强，支持结构化输入/输出、多阶段交互、图文混合处理等高级能力，适用于对专业性、准确性和响应质量有更高要求的生产环境。

## 支持的模型/功能

当前 `more models` 类别下包含以下核心模型：

- **通义法睿（`farui-plus`）**：法律行业专用大模型，支持法律咨询、文书生成、案情分析、合同审查等任务，基于千问基座并融合RAG、法律Agent及司法小模型技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与工具调用决策模型，支持两种模式：`INTENT_MODE`（输出[函数调用](../concepts/function-calling.md)JSON）和纯标签分类模式，适用于智能客服、语音助手等需快速路由的场景 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互的深度研究模型，首阶段反问澄清需求，第二阶段执行网络检索、规划与报告生成，**仅支持华北2（北京）地域及Python SDK调用** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR系列（如 `qwen3.5-ocr`, `qwen-vl-ocr-latest`）**：多模态OCR模型，支持图像文本提取、结构化信息抽取（如车票、合同关键字段），兼容OpenAI接口与DashScope API，支持`min_pixels`/`max_pixels`精细控制图像分辨率 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（`gui-plus-2026-02-26`等）**：界面自动化专用模型，可解析UI截图并生成鼠标/键盘操作指令（如`left_click`, `type`, `wait`），需配合`computer_use`工具定义使用 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档4与文档5中关于`min_pixels`默认值存在不一致——文档4对`qwen3.5-ocr`等新模型标注为3072，而文档5对`gui-plus`统一标注为3136。实际调用时请以各模型最新API文档或控制台说明为准，建议显式传入参数避免歧义。

## 关键参数

所有模型均支持以下通用参数（部分为OpenAI兼容接口特有）：

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 模型标识符，如 `"farui-plus"`、`"tongyi-intent-detect-v3"` | 必填 |
| `messages` | array | 对话历史，含`role`（`system`/`user`/`assistant`）、`content`（支持text/image_url混合） | 必填 |
| `stream` | boolean | 是否启用流式响应 | `false` |
| `max_tokens` | integer | 输出Token上限 | 因模型而异（如`qwen3.5-ocr`: 32768；`gui-plus`: 模型最大输出长度） |
| `temperature` / `top_p` | float | 控制生成多样性，二者选一即可 | `0.01`（多数模型） |
| `seed` | integer | 随机种子，保障结果可复现 | 不设置则随机 |

**模型特有参数**：
- `tongyi-intent-detect-v3`：依赖特定`system` message格式（含`Response in INTENT_MODE.`或明确意图字典）；
- `qwen-deep-research`：支持`output_format`（`model_detailed_report`/`model_summary_report`）控制报告详略；
- `qwen-ocr` & `gui-plus`：支持`min_pixels`/`max_pixels`控制图像预处理，且`gui-plus`额外支持`vl_high_resolution_images`开关；
- `gui-plus`：支持`enable_thinking`（返回`reasoning_content`）及`extra_body`透传非标准参数（如`top_k`）。

## 使用方式

### 基础调用流程
1. **准备环境**：安装对应SDK（[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)），获取并配置API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)），**强烈建议配置至环境变量**；
2. **选择域名**：优先使用业务空间专属域名（如`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)中的迁移指引；
3. **构造请求**：按模型要求组织`messages`（注意`system` role的格式约束），设置必要参数；
4. **处理响应**：解析`output.choices[0].message.content`，流式场景需逐块拼接；`qwen-deep-research`需按`phase`字段区分研究阶段（`ResearchPlanning`/`WebResearch`/`answer`）。

### 示例片段（Python）
```python
# 法睿单轮对话
from dashscope import Generation
response = Generation.call(
    model="farui-plus",
    messages=[{"role": "user", "content": "生成一份离婚协议书"}],
    result_format="message"
)

# 意图识别（INTENT_MODE）
tools = [{"name": "search_db", "description": "查询数据库"}]
system_prompt = f"""You are Qwen... tools: {json.dumps(tools)}\nResponse in INTENT_MODE."""
response = Generation.call(
    model="tongyi-intent-detect-v3",
    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": "查张三的订单"}],
    result_format="message"
)

# GUI-Plus自动化（需OpenAI SDK）
from openai import OpenAI
client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
completion = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "screenshot.png"}}]}],
    extra_body={"vl_high_resolution_images": True}
)
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**，其他模型虽多地可用，但推荐使用业务空间专属域名以获得最佳性能 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **SDK支持差异**：
  - `qwen-deep-research` **暂不支持Java SDK与OpenAI兼容接口**，仅限Python DashScope SDK；
  - `tongyi-intent-detect-v3` 的`understanding`子命令在dashscope CLI中不可用，需用Python SDK [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
- **输入规范**：
  - OCR与GUI模型要求`messages`中`user` content为`array`类型（支持`text`+`image_url`组合），不可直接传字符串；
  - `farui-plus`等文本模型接受`string` content，但多轮对话需手动维护`messages`列表；
- **成本与配额**：`tongyi-intent-detect-v3`提供90天内100万Token免费额度；其余模型按实际Token消耗计费，详情参见各模型文档中的成本说明；
- **安全提示**：API Key切勿硬编码，务必通过环境变量或密钥管理服务注入；Java SDK中`Generation`对象非线程安全，需自行管理复用与同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


