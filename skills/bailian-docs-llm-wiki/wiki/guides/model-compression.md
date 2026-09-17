# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在保持核心推理能力的前提下显著降低部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-deployment-index.md)之前。压缩操作不可逆，且仅适用于平台内微调产出的自定义模型。

## 支持的模型与功能

- **支持模型**：当前仅支持通过百炼平台完成微调训练的自定义模型（如 `qwen3.5-flash-2026-02-23`），不支持基础模型或第三方模型。具体支持列表以控制台实时展示为准，详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 文档中的“支持压缩的模型”表格。
- **功能范围**：百炼当前模型压缩特指**后训练量化（PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术。校准数据可用于提升量化精度，但仅限已发布至数据管理模块的本地数据集（不支持 OSS 挂载）。
- **地域限制**：仅华北2（北京）地域可用。

> **注意**：原始文档中多次强调“压缩不可逆”“不支持继续微调或二次压缩”，该约束在 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 全文一致，无矛盾；但需注意其与部分旧版 API 文档中模糊表述存在潜在歧义，实际行为以本页及 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 为准。

## 关键参数

创建压缩任务时需配置以下必填参数：

- **任务名称**：最长 50 字符，建议含模型简称、量化方式和版本号（如 `qwen35-flash-w4a4-v1`）；
- **量化产出模型名后缀**：仅小写字母与数字，最长 8 位，将拼接至源模型名后形成新模型标识（如源模型 `my-qwen-ft-001` + 后缀 `w4a4` → `my-qwen-ft-001-w4a4`）；
- **量化模板**：卡片式选择，模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加。切换源模型会自动清空已选模板；
- **校准数据（条件必填）**：仅当所选模板要求校准时出现，最多选 5 个已发布数据集。

所有参数在提交前不可修改，详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“创建压缩任务”章节。

## 使用方式

1. **前提**：确保工作空间中已存在状态为“成功”的微调模型（参见 [模型调优](raw/model-user-guide/fine-tuning.md)）；
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**；
3. 配置参数后单击 **开始压缩**（按钮仅在全部必填项完成时启用）；
4. 任务创建后，通过任务列表页查看状态（7 种状态，含 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等），点击任务名称进入详情页查看配置与日志；
5. 日志页支持按级别着色、下载全量日志、自动刷新（30s）等功能，失败排查请优先检查 ERROR 日志及详情页错误信息。

API 用户请参考 [模型压缩 API 参考](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/model-compression-api.md)，其行为与控制台严格对齐。

## 限制和注意事项

- ✅ **仅支持微调模型**：必须是百炼平台内完成训练且状态为“成功”的自定义模型；
- ❌ **不可逆操作**：压缩后模型**不支持继续微调**，也**不支持二次压缩**，请务必在压缩前确认量化模板与校准数据；
- ⚠️ **地域与数据限制**：仅华北2（北京）可用；校准数据必须来自百炼数据管理中已“发布”的数据集，不支持 OSS 或未发布数据；
- 💰 **计费说明**：压缩任务本身限时免费（截止时间以控制台公告为准）；压缩后模型的部署费用按 MU 规格单独计费，与压缩是否免费无关；
- 📊 **效果验证建议**：免费期内应针对同一源模型尝试多个量化模板，并使用业务测试集验证精度，再择优部署——该实践指南在 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的“常见问题”与“计费说明”章节均有明确推荐。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


