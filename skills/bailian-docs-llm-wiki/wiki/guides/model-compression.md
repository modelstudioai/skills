# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在保障推理效果的前提下显著降低部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成微调训练的自定义模型**，不支持基础模型（如原始 Qwen）、第三方模型或 OSS 托管模型。
- 当前仅华北2（北京）地域可用；新加坡等其他地域暂未开放（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“支持压缩的模型”表格）。
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “功能概述”章节）。
- 支持的模型系列以控制台实时展示为准，当前明确列出的有 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02`，其压缩前后部署规格差异显著（例如前者从 MU1\*2 降至 MU5/MU8/MU9），具体请参考 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中的规格对照表。

> **注意**：原始文档中“新加坡”地域表格为空，且未说明上线计划；若控制台已显示新加坡支持，请以控制台实时状态为准，该信息可能已过时。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式、版本号（如 `qwen35-flash-w4a4-v1`） |
| **量化产出模型名后缀** | 是 | 仅小写字母+数字，≤8 位；将拼接至源模型名后（如源模型 `my-qwen-ft` + 后缀 `w4a4` → `my-qwen-ft-w4a4`） |
| **量化模板** | 是 | 卡片式选择；模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “量化模板怎么选？”） |
| **校准数据** | 条件必填 | 仅当所选模板需校准输入时出现；最多选 5 个已发布数据集（不支持 OSS 挂载）；推荐语义贴近目标场景的数据（如客服场景用对话数据集） |

## 使用方式

1. **前提**：确保工作空间中存在状态为“成功”的百炼微调模型（参见 [模型调优](raw/model-user-guide/fine-tuning.md)）；
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**；
3. 配置参数（注意：切换源模型会自动清空已选量化模板）；
4. 点击 **开始压缩**（所有必填项完成后按钮才可点击）；
5. 任务创建后不可修改配置，失败需重新创建；
6. 通过任务列表页查看状态（7 种状态，含 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等），详情页查看配置与错误信息，日志页下载全量日志排查问题。

## 限制和注意事项

- ✅ **仅限华北2（北京）地域**；其他地域暂不支持。
- ✅ **仅支持百炼微调产出的自定义模型**；基础模型、OSS 模型、API 直接上传模型均不可压缩。
- ❌ **不可逆操作**：压缩后模型不支持继续微调、不支持二次压缩（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示）。
- ⚠️ **免费期策略**：压缩任务本身限时免费（截止时间以控制台公告为准），但压缩后模型的部署费用始终按 MU 规格计费，不受免费期影响。
- ⚠️ **校准数据限制**：仅支持在百炼「数据管理」中创建并发布的数据集，不支持外部路径或未发布数据集。
- ⚠️ **失败处理**：任务失败后，需下载全量日志并结合 ERROR 日志定位；若无法解决，请提交工单并附带任务 ID 和日志文件（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “失败排查”）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


