# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失前提下显著降低推理部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型（custom fine-tuned models）**，不支持基础模型、第三方模型或 OSS 直接上传模型。  
- 当前仅在**华北2（北京）地域**可用；新加坡等其他地域暂未开放（见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“支持压缩的模型”表格）。  
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “功能概述”章节）。  
- 量化模板以 MU 规格命名（如 `MU5`、`MU8`），编号越大表示部署资源越小、成本越低，但潜在精度损失可能越高。

> **注意**：原始文档中“支持压缩的模型”表格在“新加坡”区域显示全空（`-`），而控制台实际可能已逐步开放。请以最新控制台展示为准，避免依赖文档静态表格——该信息已过时，详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式、版本号（如 `qwen35-flash-mu8-v1`） |
| **选择源模型** | 是 | 仅显示当前工作空间内状态为 `SUCCEEDED` 的微调模型；切换源模型会清空已选量化模板 |
| **量化产出模型名后缀** | 是 | 仅限小写字母+数字，≤8 位；将拼接至源模型名后（如源模型 `my-qwen-ft` + 后缀 `mu8` → `my-qwen-ft-mu8`） |
| **量化模板** | 是 | 模板卡片按 MU 规格分组；必须先选定源模型才可加载对应模板列表 |
| **校准数据** | 条件选填 | 仅当所选模板需校准输入时出现；最多选 5 个已发布数据集（不支持 OSS 挂载），推荐语义贴近目标场景的数据 |

## 使用方式

1. **前提**：确保已完成微调训练，且源模型状态为 `SUCCEEDED`（参见 [模型调优](../../raw/model-user-guide/fine-tuning.md)）。  
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**。  
3. 填写全部必填参数，确认无误后单击 **开始压缩**（按钮仅在所有必填项合法时启用）。  
4. 任务提交后不可修改配置；可通过任务列表页或详情页查看状态与日志（支持下载全量日志、ERROR 级别高亮等）。  
5. 任务成功（`SUCCEEDED`）后，压缩模型自动出现在模型中心，可直接用于部署（部署计费独立于压缩任务，详见 [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)）。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用；其他地域暂不支持。  
- ✅ **模型来源限制**：仅支持百炼平台内微调产出的自定义模型；基础模型（如 `qwen3.5-flash-2026-02-23`）本身不可压缩，仅其微调变体可压缩。  
- ❌ **不可逆性**：压缩后模型**不支持继续微调**，也不支持**二次压缩**（见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示）。  
- ⚠️ **免费策略**：压缩任务当前限时免费（截止时间以控制台公告为准），但**部署阶段始终按 MU 规格计费**；建议在免费期内对比多个量化模板效果后再正式上线。  
- ⚠️ **校准数据要求**：必须为已在百炼「数据管理」中创建并发布的数据集；OSS 挂载数据集不可用。  

> **注意**：文档中提及“压缩任务本身限时免费”，但未明确免费期是否延续或已结束。实际计费策略请以控制台实时公告为准，避免依赖过时说明——该信息存在时效风险，详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “计费说明”章节。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


