# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失下显著降低推理部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型（custom fine-tuned models）**，不支持基础模型、第三方模型或未完成训练的中间态模型。  
- 当前仅在**华北2（北京）地域**可用；新加坡等其他地域暂未开放（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“支持压缩的模型”表格）。  
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的“功能概述”章节）。  
- 支持按需选择量化模板（如 `MU5`/`MU8`/`MU9`），模板名称中的 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加。

> **注意**：原始文档中“支持压缩的模型”表格在“新加坡”区域显示全空（`-`），而控制台实际可能已逐步开放。若在新加坡地域未见可用模型，请以控制台实时展示为准，并参考 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的地域限制说明。

## 关键参数

创建压缩任务时需配置以下必填参数：

- **任务名称**：最长 50 字符，建议含模型简称、量化方式和版本号（如 `qwen35-flash-w4a4-mu8`）。  
- **量化产出模型名后缀**：仅限小写字母与数字，最长 8 位（如 `w4a4`），将自动拼接至源模型名后形成新模型 ID。  
- **量化模板**：必须先选择源模型，再从动态加载的卡片网格中选取；不同模型支持的模板不同，切换源模型会清空已选模板。  
- **校准数据（条件选填）**：仅当所选模板要求校准时出现；最多选 5 个已在[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)中发布（非仅创建）的数据集，不支持 OSS 挂载数据。

## 使用方式

1. **前提**：确保工作空间中存在状态为 `SUCCEEDED` 的微调模型（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 的“前提条件”）。  
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**。  
3. 填写参数后单击**开始压缩**（按钮仅在所有必填项合法时启用）。  
4. 任务提交后不可修改配置；可通过任务列表页查看状态（7 种状态，含 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等）、日志（支持下载全量日志、ERROR 级别高亮）及失败排查指引。  
5. 任务成功后，压缩模型自动出现在模型中心，可直接用于部署（部署计费按 MU 规格单独计算）。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用。  
- ✅ **模型来源限制**：仅支持百炼平台内完成的微调模型；基础模型（如 `qwen3.5-flash-2026-02-23`）本身不可直接压缩。  
- ❌ **不可逆性**：压缩后模型**不支持继续微调、不支持二次压缩**（明确强调于 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示及 FAQ）。  
- ⚠️ **免费期策略**：压缩任务当前限时免费（截止时间以控制台公告为准），但**部署阶段始终按 MU 规格计费**；建议在免费期内对比多个模板效果后再正式上线。  
- ⚠️ **校准数据要求**：必须为已发布（Published）的数据集，且语义应贴近目标推理场景（如客服问答场景优先选用对话类校准数据）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


