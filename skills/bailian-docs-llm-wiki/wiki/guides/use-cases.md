# use cases

本页汇总阿里云百炼平台上常见使用场景的开发实践，覆盖 Prompt 设计、多模态生成（文生图/文生视频）、RAG 应用构建、自定义模型调优、第三方模型调用、限流应对与显式缓存等。所有场景均通过 OpenAI 兼容接口或 DashScope SDK 调用，统一使用 `DASHSCOPE_API_KEY` 鉴权。

## 调用入口与鉴权

百炼提供两套等价接口：

- **OpenAI 兼容**：`base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，路径 `/chat/completions`，可直接复用 OpenAI SDK。
- **DashScope 原生**：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`。

华北2（北京）推出业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，推理性能与稳定性更优，建议从默认域名迁移。海外地域（弗吉尼亚、新加坡、法兰克福、东京）需使用对应地域的端点，部分端点要求把 `{WorkspaceId}` 替换为真实业务空间 ID。详见 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。

调用前需[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量 `DASHSCOPE_API_KEY`。

## Prompt 设计

### 文生文

Prompt 越清晰、具体、无歧义，模型表现越符合预期。可使用「背景-目的-风格-语气-受众-输出」六要素框架系统化构建 Prompt；百炼控制台 Prompt 页面提供「自动优化」工具，对输入进行自动扩写和细节添加（消耗 Token，按推理费用计费）。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图

适用万相-文生图 V1/V2。关键参数：

- `prompt`：正向提示词，中英文描述目标图像。
- `negative_prompt`：反向提示词，描述不希望出现的内容。
- `prompt_extend`（仅 V2）：是否开启大模型智能改写，默认 `true`。

提示词公式：

- 基础公式：`主体 + 场景 + 风格`
- 进阶公式：`主体（主体描述）+ 场景（场景描述）+ 风格（定义风格）+ 镜头语言 + 氛围词 + 细节修饰`

提示词词典覆盖景别（特写/近景/中景/远景）、视角（平视/俯视/仰视）、镜头拍摄类型、风格与光线五大维度。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频 / 图生视频

万相视频生成支持文生视频、图生视频（首帧、首尾帧）、参考生视频。提示词公式按场景区分：

- 文生视频基础：`主体 + 场景 + 运动`
- 文生视频进阶：`主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化`
- 图生视频：`运动 + 运镜`（图像已确定主体/场景/风格）
- 声音公式（wan2.5+）：在主体/场景/运动之外追加 `声音描述`，分为人声（角色内容+情绪+语调+语速+音色+口音）、音效（音源材质+行为+环境音）、背景音乐（配乐+风格）。
- 多镜头公式（wan2.6/2.7）：`总体描述 + 镜头序号 + 时间戳 + 分镜内容`。
- 参考生视频（wan2.7）：`参考指代（图n/视频n）+ 动作 + 场景 + 台词（可选）+ 背景音乐（可选）`；wan2.6 改用 `character1/character2` 引用主角，最多 3 个。

wan2.7 不再支持 `shot_type` 指定单/多镜头，改由提示词控制；要强制单镜头，中文写「生成单镜头」，英文写「Generate single shot.」。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

Vidu 视频生成提示词公式为「主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介」，并通过关键词词典控制动态幅度（大/中/小动态）、运镜（move left/right/up/down、zoom in/out、固定镜头）、特殊拍摄（延时、微距、FPV、航拍）、景别、视角、构图、画面风格、特效与氛围。首次提示词效果不佳时，可通过调整主体与背景的比例关系、追加镜头控制等手段调优。

## RAG 应用

基于 LlamaIndex 接入百炼检索增强服务：

1. 安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`（Python 3.8–3.12）。
2. 用 `DashScopeParse` 解析 .doc/.docx/.pdf（单文件 ≤100M、页数 ≤1000），通过 `DASHSCOPE_WORKSPACE_ID` 指定业务空间。
3. `DashScopeCloudIndex.from_documents` 创建知识库，`DashScopeCloudRetriever` 或 `index.as_retriever()` 检索，`index.as_query_engine(llm=...)` 问答。
4. `index._insert(documents)` 增文档，`index.delete_ref_doc([doc_id])` 删文档。

详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优

流程为「模型调优 → 模型部署 → 模型评测」三步，外加训练数据准备、评测模板设计、训练策略调整三个辅助环节。**完成调优的模型必须部署后才能调用和评测**。

- **数据**：编排成 `Prompt-Completion` 格式，建议 ≥500 条；注意来源多样化、质量控制和分布平衡，并做脱敏。
- **数据集**：在数据管理页面创建训练集（Prompt+Completion）与评测集（仅 Prompt），支持版本管理与发布。
- **部署**：将自定义模型部署到独占实例，部署后即可在代码或评测中调用。
- **计费**：调优、部署、评测分别计费。

评测结果不满意可更换基础模型、扩充数据、调整超参数后重训，直至满足预期。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 第三方模型调用

百炼聚合了多家供应商的第三方模型，统一通过 OpenAI 兼容接口或 DashScope SDK 调用，模型名以 `供应商/模型` 形式标识。多数模型支持 `enable_thinking` 切换思考/非思考模式（OpenAI Python SDK 走 `extra_body`，Node.js SDK 走顶层参数），思考过程通过 `reasoning_content` 字段返回；部分模型还支持 `reasoning_effort`（low/medium/high/max）控制推理深度。

| 供应商 | 模型名示例 | 默认思考 | 备注 |
| --- | --- | --- | --- |
| 阿里云（DeepSeek） | `deepseek-v4-pro` | 可切换 | 多地域；旧版 v3/r1 系列将于 2026-07-09 下架 |
| 硅基流动（DeepSeek） | `siliconflow/deepseek-v3.2` | 可切换 | 仅华北2；上下文更长；不支持联网/缓存 |
| 快手万擎（DeepSeek） | `vanchin/deepseek-v4-pro` | 可切换 | 仅华北2 |
| 月之暗面（Kimi） | `kimi/kimi-k2.6` 等 | 可切换 | 仅华北2；多模态模型走 `multimodal-generation` |
| 阿里云（Kimi） | `kimi-k2-thinking` 等 | 因模型而异 | 多地域；旧版 K2 将于 2026-07-09 下架 |
| 智谱（GLM） | `ZHIPU/GLM-5.2` | 可切换 | 仅华北2；1M 上下文 |
| 阿里云（GLM） | `glm-5.2` 等 | 可切换 | 多地域；旧版 4.6/4.7 将于 2026-07-09 下架 |
| 稀宇（MiniMax 直供） | `MiniMax/MiniMax-M2.7` | 默认思考 | 仅华北2 |
| 阿里云（MiniMax） | `MiniMax-M2.5` | 默认思考 | 仅中国内地；旧版 M2.1 将于 2026-07-09 下架 |
| 小米（MiMo） | `xiaomi/mimo-v2.5-pro` | 默认开启 | 仅华北2；混合推理 |
| 阶跃星辰（Step） | `stepfun/step-3.7-flash` | 默认关闭 | 仅华北2；多模态推理 |

> **注意**：多家供应商的旧版模型（deepseek-v3/r1、kimi-k2、glm-4.6/4.7、MiniMax-M2.1 等）将于 2026 年 7 月 9 日下架，官方推荐迁移到 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash`。新接入建议直接选择推荐模型或各系列的最新版本。

> **注意**：阿里云百炼与硅基流动都提供 DeepSeek 服务，硅基流动支持更[长上下文](../concepts/long-context.md)，但阿里云供应商限流更宽松且支持联网搜索与[上下文缓存](../concepts/prompt-caching.md)。DeepSeek 直供（月之暗面/快手万擎/智谱/小米/阶跃等）仅华北2（北京）可用，需用华北2 的 API Key。

## 限流应对

百炼按**主账号**维度、**模型**独立限流，触发后通常 1 分钟内恢复。三类规则：分钟级配额（RPM/TPM）、瞬时频率（RPS/TPS）、增速限制（Traffic Burst）。

按改动成本从低到高的应对方案：

1. **平台配置**
   - 服务端排队等待（首选，针对增速限流）：请求头 `X-DashScope-Wait-Timeout: 30`（建议 3–120 秒），服务端排队而非直接 429；需相应调大客户端超时（非流式 = 基础超时 + Wait-Timeout）。
   - 提升限流额度：控制台临时提升，立即生效（华北2/新加坡）。
   - PTU 预置吞吐单元：专享算力，避免公共池竞争；未满负荷也持续计费。
   - Batch API：异步批处理，不受在线限流约束。
2. **客户端流控**：令牌桶、并发信号量、双重令牌桶（同时限 RPM/TPM）、平滑限速器、自适应拥塞控制。
3. **架构兜底**：模型降级（Fallback）、基于消息队列削峰填谷。

错误码定位：`Throttling.RateQuota`/`limit_requests` 对应请求频率超限；`Throttling.AllocationQuota`/`insufficient_quota` 对应 Token 用量超限；`Throttling.BurstRate`/`limit_burst_rate` 对应流量增速超限。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 显式缓存

显式缓存通过在请求中添加缓存标记，确保相同输入**确定性命中**缓存（不受后端调度影响），首次写入产生标准价格 25% 的额外开销，后续命中节省 90% 成本，发生一次命中即整体便宜于不使用缓存。适用场景：需要稳定命中、高频复用相同 Prompt、工业级 Agent [长上下文](../concepts/long-context.md)管理。

百炼 Anthropic 兼容端点原生支持显式缓存，常见 Coding 工具接入后自动启用：

- **Claude Code**：v2.x 起默认对 system、env、最近 user message 携带 `cache_control`，无需额外配置。端点：按量计费 `https://dashscope.aliyuncs.com/apps/anthropic`，Coding Plan `https://coding.dashscope.aliyuncs.com/apps/anthropic`，Token Plan 团队版 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`。可用 `--exclude-dynamic-system-prompt-sections` 把动态信息移到 user message 以提升跨会话命中率；`DISABLE_PROMPT_CACHING=1` 关闭。
- **OpenCode**：通过 `@ai-sdk/anthropic` 接入，默认对 system 与最近非 system 消息注入 `cache_control`，`baseURL` 末尾需带 `/v1`。
- **OpenClaw**：provider base URL 指向 `/apps/anthropic` 即自动启用；可在 system [prompt](prompt.md) 中插入 `<!-- OPENCLAW_CACHE_BOUNDARY -->` 标记分隔稳定前缀与动态后缀。
- **Hermes**：通过 `hermes config set` 配置 base URL。

## 文档转视频

借助大模型把文档自动转为含图文、语音、字幕的视频，方案分四步：文档切片（大模型总结标题分段）→ 生成演示文稿图片（整合标题/正文/图片）→ 生成讲解语音与字幕（多模态 TTS + 按音频时长生成字幕）→ 生成视频（图片剪辑 + 音频/字幕嵌入）。依赖 FFmpeg、Marp（演示文稿）和浏览器引擎渲染，提供完整代码包。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)



