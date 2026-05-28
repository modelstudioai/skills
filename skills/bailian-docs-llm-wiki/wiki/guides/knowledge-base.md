# knowledge base

知识库基于检索增强生成（RAG）架构，为大模型提供私有数据与最新业务信息的语义检索能力。系统自动完成文件解析、智能切分、向量化存储与重排序召回，有效解决通用模型在垂直领域的知识滞后与幻觉问题。开发者可通过控制台或 API 将其无缝集成至自有 AI 应用中，实现精准、可控的问答服务。

## 支持的模型/功能
- **支持模型**：兼容阿里云百炼预置的千问全系（含 QwQ/Max/Plus/Turbo/Long、VL 多模态及开源版）、DeepSeek、Llama 等第三方文本模型。同时支持基于千问系列[[微调]]后的自定义模型。详细模型清单见[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **知识库类型**：提供文档搜索（基础问答/图文并茂/视觉理解/极速问答）、数据查询、图片问答及音视频搜索。不同类型底层自动匹配对应的[[向量模型]]与解析器。
- **多模态解析**：内置电子文档、大模型文档、Qwen VL 解析及音视频结构化对齐能力，支持保留图表、版面与时间轴上下文。

## 关键参数
配置以下参数直接影响检索准确率、Token 消耗与模型推理效果：
- **相似度阈值**：语义相似度低于该阈值的切片将被过滤。阈值设置过高易导致相关片段被丢弃，建议结合[[命中测试]]反复校准。
- **召回片段数（Final TopK）**：返回给大模型的切片上限为 20。针对“总结/对比/列举”类复杂 Query，调高该值可提升生成完整性，但受模型上下文长度限制。
- **初步召回 TopK（向量/关键词）**：控制送入[[排序模型]]的候选池大小。**排序模型调用费用按此初步召回总量计费，而非最终返回数量**。
- **知识库权重**：多路召回时干预不同数据源的优先级。仅在同类型知识库间生效，系统按 `相似度 × 权重` 重新排序。
- **切分策略**：推荐“智能切分”以维持语义完整性。单个切片上限为 6000 Token。规格与配额限制详见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

## 使用方式
提供零代码集成与全链路 API 开发两种路径：
1. **控制台集成**：创建知识库并导入文件后，在[[智能体应用]]配置页直接挂载，或在[[工作流应用]]画布中拖拽“知识库”节点。支持配置固定知识库或通过 `CodeList` 变量实现动态路由。
2. **API 调用**：适用于自动化流水线或外部业务对接。标准链路为：申请上传租约 → 上传文件至 OSS/平台存储 → 注册文件 → 初始化索引 → 提交并轮询任务状态。Python/Java SDK 示例与鉴权流程见[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
3. **效果优化**：若出现漏召回或生成偏差，可启用[[多轮对话改写]]、为文件绑定 Metadata/Tags 进行结构化过滤，或调整 Prompt 模板约束输出格式。完整调优方法论见[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

> **注意**：
> 1. **配置不可逆**：知识库创建完成后，**知识库类型、Meta 信息抽取模板及文档切分策略均无法修改**。如需变更，必须重建知识库。
> 2. **计费逻辑分离**：规格费用（按实例运行时长）与模型调用费用（[[向量模型]]与[[排序模型]]按 Token 计费）独立核算。挂载 N 个知识库时，单次查询的向量化与重排 Token 消耗将按 N 倍增长。
> 3. **欠费数据保留期**：账户欠费后服务暂停。使用平台存储的知识库欠费满 14 天、使用自建 ADB-PG 的满 8 天将触发**永久数据清除**且不可恢复。
> 4. **计费生效时间**：平台自 2026 年 1 月 4 日起正式计费，此前创建的实例将保留至 2026 年 6 月 30 日，逾期未开通服务将自动清理。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)

