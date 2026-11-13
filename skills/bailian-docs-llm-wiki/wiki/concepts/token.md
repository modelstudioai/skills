# Token 计量

Token 计量是百炼平台对模型调用资源消耗的核心度量方式，指将输入文本、输出文本、图像/音视频内容等多模态数据按统一规则切分为基础语义单元（Token），并以此为单位进行用量统计、成本核算与配额控制。所有模型推理类服务（含文本生成、视觉理解、向量嵌入、重排序等）均以 Token 为最小计费粒度。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时推理调用**：每次 `POST /v1/models/{model_id}/invoke` 请求的 `input`（如 prompt、image_url、audio_url）和 `output`（如生成文本、embedding 向量、rerank 分数）均被解析为 Token；输入 Token 和输出 Token 分别计量，价格可能不同（例如 `qwen3.8-max` 输入 ¥12/百万 Token，输出 ¥24/百万 Token）。
- **Agent 场景**：Managed Agents、Flow Agent 中调用大模型或向量/排序模型时，Token 消耗计入对应模型账单；知识库检索流程中，“向量模型 + 排序模型”两阶段调用产生的 Token 均独立计量，TopK 参数直接影响送入排序模型的文档切片数量，从而显著影响 Token 总量。
- **[异步任务](asynchronous-task.md)**：生图、生视频等异步模型（如 `wan2.7-i2v`）虽按任务结算，但底层仍基于输入帧数、分辨率、时长等换算为等效 Token 用于资源调度与成本归因。
- **模型训练与微调**：训练费用按“每千 Token”计价（如 `qwen3-vl-8b-instruct` ¥0.012/千 Token），此处 Token 指训练数据集经 tokenizer 处理后的总 token 数，不含推理阶段的 output。
- **监控与告警**：模型监控系统提供 `模型消耗 TotalToken 数` 指标，支持配置环比突增告警（如“24 小时内 Token 消耗增长 >200%”），帮助快速识别异常调用或 Prompt 泄露风险。

## 关键参数和配置

- **计费单位**：统一以“千 Token”（kToken）或“百万 Token”（MToken）为计价单位，具体取决于服务类型（推理多用 MToken，训练多用 kToken）。
- **输入/输出分离计量**：所有模型调用均区分 `input_tokens` 和 `output_tokens`，二者在账单明细中分别列示，不可互相抵扣。
- **多模态 Token 换算规则**：
  - 文本：标准 tokenizer（如 Qwen 的 tiktoken）分词结果；
  - 图像：按 `min_pixels`/`max_pixels` 缩放后，以固定比例映射为视觉 Token（如 Qwen-VL 每 512×512 区域 ≈ 128 tokens）；
  - 视频：按 `fps` 抽帧后，每帧按图像规则换算，再叠加时序建模开销；
  - 音频：ASR/TTS 按音频时长 × 采样率 × 编码系数折算为等效文本 Token。
- **免费额度绑定**：新人免费额度（如 100 万 Token）按模型 ID 精确隔离，`qwen3.8-max` 与 `qwen3.8-max-2026-05-17` 视为两个独立模型，额度不共享。
- **地域价格差异**：同一模型在不同地域（如北京 vs 弗吉尼亚）Token 单价不同，调用前需确认 `base_url` 对应地域的刊例价。

## 面向开发者，简洁实用

- ✅ **查用量**：控制台 → [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看各模型、各 API Key 的 Token 消耗明细；也可调用 `POST /usage/summary` 获取结构化数据。
- ✅ **控成本**：通过 `max_tokens` 限制输出长度、精简 Prompt、启用缓存（`cache_enabled: true`）、选择轻量模型（如 `qwen3.6-flash` 替代 `qwen3.8-max`）直接降低 Token 消耗。
- ✅ **避陷阱**：流式响应（`stream=true`）下，`output` 中每个 `delta` 帧均计入 Token；图片 URL 若返回超大尺寸原图，将触发更高像素换算 —— 建议预处理为 `min_pixels=24576` 合理尺寸。
- ✅ **对账要点**：账单中“阿里云百炼大模型推理”商品下的实例 ID 后缀（如 `-embedding-`、`-rerank-`）可精准定位 Token 归属模型与用途，勿与“知识库规格费”混淆。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)


