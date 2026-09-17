# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代及关键机制变更，面向开发者提供可落地的版本演进信息。内容聚焦于**实际可用性变化**（如新增/下线模型、API 行为调整、计费与限流策略更新），不包含营销性描述。所有变更均以正式公告或控制台生效时间为准，建议开发者定期查阅并及时适配。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：  
  - 多模态大模型：`qwen3.8-max`（2.4T MoE）、`deepseek-v4.1-flash`（552B MoE）、`ZHIPU/GLM-5.3-Flash`（320B）、`kimi-k3`（2.8T）；  
  - 视频生成：`kling/kling-v3-turbo-video-generation`、`wan3.0-video-prime`、`pixverse/pixverse-v6-r2v-omni`；  
  - 图像生成：`qwen-image-3.0-pro`（支持图中图密集排版）、`vidu/viduq3-drama_reference2video`（剧集专用）；  
  - 向量与排序：`qwen3.7-text-rerank`（Web检索相对提升35%）、`qwen3.7-text-embedding-flash`（支持128K长文本+Sparse Embedding）。  
- **功能模块上线**：  
  - 知识库RAG：新增[知识检索服务](raw/model-user-guide/knowledge-base/rag-knowledge-retrieval.md)与[知识问答服务](raw/model-user-guide/knowledge-base/rag-knowledge-qa.md)，支持多知识库联合检索与混合排序；  
  - 智能体托管：6月29日上线[智能体托管运行时 API](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)，平台托管会话与工具执行；  
  - 模型调优：5月28日起支持图像生成模型（Wan/Wanx）、5月21日支持视频生成模型、1月22日支持视觉理解（VL）模型调优；  
  - 多模态翻译：5月26日上线[通义多模态翻译 API](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir.md)，覆盖文本/图片/文档/网页翻译。  
- **模型下线动态**：2026年10月10日将下线一批模型，具体清单及历史下线记录详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`glm-5.3`、`kimi-k3`）统一支持 **1M token 上下文**；部分 Flash 模型（如 `qwen3.8-flash`）在保持该能力的同时优化吞吐成本。  
- **输出长度**：`qwen3.8-max` 支持最大 384K 输出；`ZHIPU/GLM-5.3-Flash` 支持 128K 输出；`kling/kling-v3-turbo-video-generation` 固定音画同出，未公开帧数上限。  
- **限流策略**：模型下线前将逐步缩减 QPM/TPM，具体限流基准恢复至[默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)后执行；新上线模型（如 `qwen3.8-flash`）明确标注“高并发、轻量化任务”适用场景，隐含更高默认 QPM。  
- **部署单位**：1月23日起，模型部署 API 新增按**模型单元（MU）时长计费**模式，性能可调，详见 [模型部署快速入门](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

## 使用方式

- **模型调用**：  
  - 文本生成类模型（如 `qwen3.8-max`）兼容 OpenAI `chat/completions` 与 Anthropic `messages` 协议；  
  - 多模态模型（如 `qwen3.8-flash`）需按 [Qwen API 参考](raw/model-api-reference/qwen-api-reference.md) 提交 `messages` 中含 `image_url` 或 `video_url` 的 content；  
  - 视频生成模型（如 `vidu/viduq3-pro-fast_img2video`）需通过 `/v1/services/aigc/video-generation/generation` 接口调用，输入 `prompt` + `image_url`。  
- **功能启用**：  
  - 新增的[Responses API 异步调用](https://help.aliyun.com/zh/model-studio/asynchronous-call-api-reference#7226dca8fe4ld)需在请求中添加 `background=true` 参数；  
  - 知识库 RAG 服务需先创建知识库实例，再调用 `/v1/knowledgebases/{kb_id}/retrieve` 或 `/v1/knowledgebases/{kb_id}/query`；  
  - 智能体托管运行时需通过 `/v1/agents/{agent_id}/runs` 创建托管会话，工具执行由平台自动调度。  
- **配置管理**：  
  - 6月10日上线的[Skill 能力包](../../raw/application-user-guide/skill/introduction-to-skill.md)，可在应用编辑器中为智能体添加官方或自定义技能；  
  - 4月7日上线的[Prompt 工程 API](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering.md)，支持模板版本化管理与灰度发布。

## 限制和注意事项

- > **注意**：文档2中 `kimi/kimi-k3` 与 `kimi-k3` 在2026-07-17和2026-08-19两处出现，但模型ID写法不一致（带斜杠 vs 不带），实际调用应以控制台模型列表或 [模型广场](https://bailian.console.aliyun.com/model/catalog) 显示的 **标准模型ID** 为准，避免因路径分隔符导致404错误。  
- > **注意**：文档3中“6月12日新增美国、德国、日本地域”与文档2中多数新模型（如 `qwen3.8-flash`）仅标注“华北2（北京）”，**未明确声明地域可用性**。调用前须确认目标模型是否已在所选地域部署，否则将返回 `RegionNotSupported` 错误。  
- 模型下线期间（通知发布日至正式下线日），API 接口仍可调用，但 QPM/TPM 会阶梯式缩减，**不保证服务稳定性**；正式下线后，已部署应用将直接失败，需提前切换至替代模型。  
- 部分功能存在灰度范围：如5月31日上线的“强化学习训练（RL）”为邀约制开放；6月29日上线的“智能体托管运行时”当前仅对 Pro 套餐及以上用户开放。  
- 旧版功能逐步淘汰：6月16日下线“企业知识库（旧）”，7月16日生效；6月28日启动 `qwen-turbo` 资源包退市，存量资源包到期后不可续购。相关迁移路径详见 [企业知识库迁移指南](../../raw/application-user-guide/knowledge-base/enterprise-knowledge-base-migration.md) 和 [资源包退市公告](https://www.aliyun.com/notice/118392)。  
- 所有模型限流、地域支持、功能可用性以 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 和 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 的最新公告为准，历史文档（如文档2中2026-06-01的 `fun-music-preview`）若未在后续公告中重申，视为已下线或转为内部测试。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


