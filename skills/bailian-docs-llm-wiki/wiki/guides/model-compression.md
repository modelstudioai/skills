# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在保障推理效果的前提下显著降低部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型（custom fine-tuned models）**，不支持基础模型、第三方模型或 OSS 直接上传模型。  
- 当前仅在**华北2（北京）地域**可用；新加坡等其他地域暂未开放（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。  
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。  
- 支持的模型系列以控制台实时展示为准，当前明确列出的有 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02`，对应压缩后部署规格为 MU5/MU8/MU9 等（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。

> **注意**：原始文档中“支持压缩的模型”表格在新加坡地域显示为全空（`-`），但未说明是否为临时缺失或长期不支持。建议开发者优先在华北2（北京）创建任务，并以控制台实际可选模型为准。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式、版本号（如 `qwen35-flash-w4a4-v1`） |
| **量化产出模型名后缀** | 是 | 仅小写字母+数字，≤8 位；将拼接到源模型名后（如源模型 `my-qwen-ft-001` + 后缀 `w4a4` → `my-qwen-ft-001-w4a4`） |
| **量化模板** | 是 | 卡片式选择；模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加 |
| **校准数据** | 条件选填 | 仅当所选模板需校准输入时出现；最多选 5 个已发布数据集（不支持 OSS 挂载） |

## 使用方式

1. **前提**：确保工作空间中已存在状态为「成功」的微调模型（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）；  
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**；  
3. 配置参数（注意：切换源模型会自动清空已选量化模板）；  
4. 单击**开始压缩**（所有必填项完成后按钮才可点击）；  
5. 任务创建后不可修改配置，需在提交前确认量化模板与校准数据选择。

任务状态共 7 种：`PENDING` → `QUEUING` → `RUNNING` → `SUCCEEDED`/`FAILED`/`CANCELING`/`CANCELED`。失败时应优先查看详情页错误信息及日志页中 `ERROR` 级别条目。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用；  
- ✅ **模型来源限制**：仅支持百炼平台内完成的微调模型；  
- ❌ **不可逆性**：压缩后模型**不支持继续微调、不支持二次压缩**（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）；  
- ❌ **无重试机制**：任务创建后无法修改配置，失败需新建任务；  
- 💡 **免费期策略**：压缩任务本身限时免费（截止时间以控制台公告为准），但部署阶段仍按 MU 规格正常计费；  
- ⚠️ **精度权衡**：量化模板 MU 编号越高，部署成本越低，但需业务测试集验证精度是否达标；建议在免费期内对比多个模板效果后再正式部署。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


