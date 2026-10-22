# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失下显著降低推理部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型（custom fine-tuned models）**，不支持基础模型、第三方模型或未完成训练的中间态模型。  
- 当前仅在**华北2（北京）地域**可用；新加坡等其他地域暂未开放（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“支持压缩的模型”表格）。  
- 功能严格限定为**后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “功能概述”章节）。  
- 量化模板以 MU 规格命名（如 `MU5`、`MU8`），编号越大表示部署资源越小、成本越低，但潜在精度损失可能增加。

## 关键参数

创建压缩任务时需配置以下必填参数（均不可修改）：

| 参数 | 说明 |
|------|------|
| **任务名称** | ≤50 字符，建议含模型简称、量化方式和版本号（如 `qwen35-flash-w4a4-mu8`） |
| **量化产出模型名后缀** | ≤8 位小写字母/数字，将拼接至源模型名后（如源模型 `my-qwen-ft-001` + 后缀 `w4a4` → 输出 `my-qwen-ft-001-w4a4`） |
| **量化模板** | 卡片式选择，依赖所选源模型动态加载；模板名中 MU 编号直接对应部署规格（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “创建压缩任务”章节） |
| **校准数据（条件必填）** | 仅当所选模板要求校准时显示；最多 5 个已发布数据集（不支持 OSS 挂载），建议语义贴近目标推理场景 |

> **注意**：切换源模型会自动清空已选量化模板——不同微调模型支持的模板列表不同，此行为已在 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 明确说明，开发者需注意配置顺序。

## 使用方式

1. **前提**：确保工作空间中存在状态为 `SUCCEEDED` 的微调模型（参见 [模型调优](raw/model-user-guide/fine-tuning.md) 文档）；  
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**；  
3. 填写全部必填参数，确认无误后单击 **开始压缩**（按钮仅在所有必填项合法时启用）；  
4. 任务提交后不可修改配置，可通过任务列表页查看状态（7 种状态详见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “任务状态”小节）；  
5. 成功后，压缩模型自动出现在模型中心，可直接用于部署（部署计费按 MU 规格单独计算，与压缩任务本身无关）。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用；  
- ✅ **模型来源限制**：仅支持百炼平台内完成的微调模型；  
- ❌ **不可逆性**：压缩后模型**不支持继续微调、不支持二次压缩**（见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示）；  
- ❌ **校准数据限制**：不支持 OSS 挂载数据集，仅限控制台「数据管理」中已创建并发布的数据集；  
- ⚠️ **免费期说明**：压缩任务当前限时免费（截止时间以控制台公告为准），但**部署阶段始终按 MU 规格计费**，与免费期无关；  
- ⚠️ **精度验证建议**：强烈建议在免费期内对同一源模型尝试多个量化模板，并使用业务测试集验证推理效果，再择优部署（参见 [原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “如何利用免费期确定最佳压缩方案”）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


