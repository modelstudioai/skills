# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失下显著降低推理部署所需的 MU 规格与成本。该功能为模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型（Custom Fine-tuned Models）**，不支持基础模型、第三方模型或 OSS 导入模型。  
- 当前仅在**华北2（北京）地域**可用；新加坡等其他地域暂未开放（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。  
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。  
- 支持的模型系列以控制台实时展示为准，当前明确支持 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02` 等 Qwen 系列微调模型，具体压缩前后部署规格需参考控制台配置（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式、版本号（如 `qwen35-flash-w8a8-mu5`） |
| **量化产出模型名后缀** | 是 | 仅小写字母+数字，≤8 位；将拼接至源模型名后（如源模型 `my-qwen-ft-v1` + 后缀 `w8a8` → 输出 `my-qwen-ft-v1-w8a8`） |
| **量化模板** | 是 | 卡片式选择；模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能越高 |
| **校准数据** | 条件选填 | 仅当所选模板要求校准时显示；最多选 5 个已发布数据集（不支持 OSS 挂载），建议语义贴近目标推理场景 |

> **注意**：切换源模型会自动清空已选量化模板——因不同微调模型支持的模板列表不同，此行为已在 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中明确说明。

## 使用方式

1. **前提**：确保工作空间中存在状态为「成功」的微调模型（参见 [模型调优](raw/model-user-guide/fine-tuning.md)）；  
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**；  
3. 填写全部必填参数（任务名称、后缀、源模型、量化模板），校准数据按需补充；  
4. 单击 **开始压缩**（按钮仅在所有必填项合法时启用）；  
5. 任务创建后不可修改配置，需在提交前确认量化模板选择；  
6. 任务成功（`SUCCEEDED`）后，压缩模型自动出现在模型中心，可直接用于部署。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用；  
- ✅ **模型来源限制**：仅支持百炼平台内完成的微调模型；  
- ❌ **不可逆性**：压缩后模型**不支持继续微调、不支持二次压缩**（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）；  
- ❌ **任务不可编辑**：创建后无法修改任何配置（包括量化模板、校准数据等）；  
- ⚠️ **免费期策略**：压缩任务本身限时免费（截止时间以控制台公告为准），但**部署阶段始终按 MU 规格计费**；建议在免费期内对比多个模板效果，再确定最终部署方案；  
- ⚠️ **失败排查**：优先查看详情页错误信息 → 日志页搜索 `ERROR` → 下载全量日志分析；若仍无法解决，请提交工单并附任务 ID 与日志文件。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


