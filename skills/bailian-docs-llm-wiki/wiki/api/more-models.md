# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、多语言翻译、意图识别、OCR、GUI交互及深度研究等任务。这些模型通过统一 API 接口调用，支持按需选用。所有模型均需通过 `model` 参数显式指定，不参与通用模型的自动路由。

## 支持的模型与功能

当前支持的专用模型包括：
- **通义法睿**：面向法律文书理解、类案推荐与法条推理的领域大模型，详见 [通义法睿](../../raw/model-api-reference/more-models/tongyi-farui-api.md)；
- **意图理解**：轻量级端侧可部署模型，专用于用户查询意图分类（如“查订单”“退换货”），详见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
- **Qwen-MT**：支持 100+ 语种双向翻译的高质量机器翻译模型，低延迟设计，适用于实时对话场景，详见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)；
- **Qwen-Deep-Research**：长上下文（最高 1M tokens）支持的深度分析模型，适用于研报生成、技术文档精读等复杂推理任务；
- **Qwen-OCR**：基于[多模态](../concepts/multimodal.md)架构的高精度文字提取模型，支持图片/扫描件中的中英文混合文本、表格结构识别；
- **GUI-Plus**：专为 GUI 自动化设计的视觉-语言联合模型，可解析截图并生成操作指令（如“点击右上角设置按钮”）。

> **注意**：[Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 文档中声明的默认 `max_tokens=8192` 与实际 API 限制（`max_tokens=32768`）存在不一致，以 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中描述的通用 token 限制策略为准——即 `max_tokens` 受输入图像分辨率与文本长度共同约束，需在请求前预估。

## 关键参数

- `model`: 必填，值为模型标识符（如 `"qwen-farui"`、`"qwen-mt-zh2en"`、`"gui-plus"`），区分大小写；
- `input`: 结构依模型而异：  
  - 法睿/意图/Qwen-MT 接受 `text` 字段；  
  - Qwen-OCR 要求 `image_url` 或 `image_base64` + 可选 `language_hint`；  
  - GUI-Plus 需同时提供 `screenshot` 和 `instruction` 字段；
- `temperature`: 仅对法睿、Deep-Research、GUI-Plus 生效（范围 0.0–1.0），Qwen-MT 与 OCR 固定为确定性解码；
- `top_p`: 同上，OCR 与意图模型不支持该参数。

## 使用方式

调用路径统一为 `POST /v1/models/{model}/invoke`（非 `/v1/chat/completions`）。示例请求：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/qwen-mt-zh2en/invoke" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "今天天气很好。"}}'
```

所有模型均支持流式响应（`stream=true`），但 OCR 与意图识别因输出确定性高，流式无实际收益。

## 限制和注意事项

- 单次请求最大输入长度：Qwen-MT ≤ 5000 字符；Qwen-OCR 图像尺寸 ≤ 4096×4096 像素；GUI-Plus 截图建议 ≤ 1920×1080；
- 计费按实际调用模型独立计费，不与通用模型共享配额；
- GUI-Plus 模型暂不支持 `system` 消息，所有指令必须置于 `instruction` 字段；
- 多语言翻译模型（如 `qwen-mt-en2ja`）需严格匹配目标语言代码，错误代码将返回 `400 Bad Request`，而非静默降级。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


