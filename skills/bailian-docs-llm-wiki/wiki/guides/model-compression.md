# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失前提下显著降低推理部署所需的 MU 规格与成本。该功能为模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)之前。压缩操作不可逆，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型**（即 `fine-tuned` 状态的自定义模型），不支持基础模型、第三方模型或未发布模型。  
- **当前仅华北2（北京）地域可用**；新加坡等其他地域暂未开放，控制台中对应区域表格为空（见[原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。  
- **功能限定为后训练量化（Post-Training Quantization, PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术（详见[原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。  
- 支持为不同模型系列（如 Qwen）配置多种量化模板，模板名称中 MU 编号（如 MU5/MU8）直接对应压缩后部署规格，编号越大，资源占用越小、成本越低，但潜在精度损失可能增加。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符；建议含模型简称、量化方式和版本号（如 `qwen35-flash-w4a4-v1`） |
| **量化产出模型名后缀** | 是 | 仅限小写字母+数字，≤8 位；将拼接至源模型名后生成新模型 ID（如源模型 `ft-qwen35-20260223` + 后缀 `w4a4` → `ft-qwen35-20260223-w4a4`） |
| **量化模板** | 是 | 依赖所选源模型动态加载；MU 编号反映部署规格，需权衡精度与成本（参见[原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)中“量化模板怎么选”说明） |
| **校准数据** | 条件必填 | 仅当所选模板要求校准时显示；最多选 5 个已发布数据集（不支持 OSS 挂载），建议语义贴近目标推理场景 |

> **注意**：切换源模型会自动清空已选量化模板——因不同模型支持的模板列表不同，此行为在[原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)中明确说明，开发者需重新选择。

## 使用方式

1. **前提**：确保工作空间中存在状态为 `SUCCEEDED` 的微调模型（参见[模型调优](raw/model-user-guide/fine-tuning.md)）；  
2. 控制台导航至 **模型压缩 → 创建压缩任务**；  
3. 填写任务名称、后缀、选择源模型（弹窗仅展示可压缩模型）、量化模板及（如有）校准数据；  
4. 单击 **开始压缩** —— 所有必填项校验通过后按钮才可点击，且**创建后不可修改配置**；  
5. 在任务列表页跟踪状态（7 种状态，含 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等），失败时优先查看详情页错误信息与日志页 `ERROR` 级别条目；  
6. 任务成功后，压缩后模型可在模型中心查看并部署，部署计费按实际 MU 规格计算（非压缩任务本身计费）。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用；  
- ✅ **模型来源限制**：仅支持百炼平台内微调产出的模型，不支持导入模型、基础模型或 API 直接上传模型；  
- ❌ **不可逆性**：压缩后模型**不支持继续微调**，也不支持**二次压缩**（见[原文标题](../../raw/model-user-guide/model-compression/model-compression-introduction.md)“重要”提示）；  
- ⚠️ **免费策略**：压缩任务当前限时免费（截止时间以控制台公告为准），但**部署阶段始终按 MU 规格计费**；建议在免费期内对比多个模板效果，再选定最优方案上线；  
- ⚠️ **校准数据要求**：必须为已在百炼「数据管理」中创建并发布的数据集，OSS 挂载数据集不被接受；  
- ⚠️ **失败恢复**：任务失败后无法重试，需新建任务；若需调整，应基于同一源模型更换模板或补充校准数据后重试。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


