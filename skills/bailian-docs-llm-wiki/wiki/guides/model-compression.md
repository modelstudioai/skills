# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失前提下显著降低推理部署所需的 MU 规格与成本。该功能属于模型生产链路中的可选环节，位于[模型调优](raw/model-user-guide/fine-tuning.md)之后、[模型部署](raw/model-user-guide/model-deployment-index.md)之前。**压缩不可逆**，产出模型不支持继续微调或二次压缩。

## 支持的模型与功能

- **仅支持通过百炼平台完成的微调模型**（即 `fine-tuned` 状态的自定义模型），不支持基础模型、第三方模型或未完成训练的中间检查点。  
- **当前仅华北2（北京）地域可用**，新加坡等其他地域暂未开放（见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中“使用限制”章节）。  
- 功能特指**后训练量化（PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩技术；校准数据仅用于提升量化精度，非必需但推荐使用（详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “创建压缩任务”部分）。  
- 支持的模型系列以控制台实时展示为准，当前明确支持 `qwen3.5-flash-2026-02-23` 和 `qwen3.6-plus-2026-04-02` 等 Qwen 系列微调模型（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 表格）。

## 关键参数

| 参数 | 是否必填 | 说明 |
|------|----------|------|
| **任务名称** | 是 | ≤50 字符，建议含模型简称、量化方式和版本号，便于追踪 |
| **量化产出模型名后缀** | 是 | 仅小写字母+数字，≤8 位；将拼接至源模型名后生成新模型 ID（如 `my-qwen-ft-quant`） |
| **量化模板** | 是 | 卡片式选择，名称中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加；**切换源模型会自动清空已选模板**（见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)） |
| **校准数据** | 条件选填 | 仅当所选模板需校准输入时显示；最多选 5 个已发布数据集（不支持 OSS 挂载），应与目标推理场景语义一致 |

> **注意**：文档中“支持压缩的模型”表格在新加坡地域显示为空，但未说明是否未来支持或为长期限制。请以控制台实际可用模型列表为准，避免依赖静态表格。

## 使用方式

1. **前提**：确保工作空间中存在状态为 `SUCCEEDED` 的微调模型（参见 [模型调优](raw/model-user-guide/fine-tuning.md)）；  
2. 控制台路径：左侧导航栏 → **模型压缩** → **创建压缩任务**；  
3. 填写必填参数，特别注意：  
   - 源模型选择后，量化模板列表才动态加载；  
   - 所有必填项完成后，“开始压缩”按钮方可点击；  
   - **任务创建后不可修改配置**，请确认再提交；  
4. 任务提交后，可在任务列表页查看状态（7 种状态，含 `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等），详情页提供配置快照与实时日志；  
5. 成功后，压缩模型自动出现在模型中心，可直接用于部署（部署计费按 MU 规格单独计算，与压缩任务免费期无关）。

## 限制和注意事项

- ✅ **地域限制**：仅华北2（北京）可用；  
- ✅ **模型来源限制**：仅支持百炼平台内微调产出的模型；  
- ❌ **不可逆性**：压缩后模型**不支持继续微调、不支持二次压缩**（见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “重要”提示）；  
- ⚠️ **失败排查**：优先查看详情页错误信息，再搜索日志中 `ERROR` 级别条目；下载全量日志有助于定位深层问题；  
- 💡 **免费策略**：压缩任务本身限时免费（截止时间以控制台公告为准），但**部署阶段始终按 MU 规格计费**；建议在免费期内对比多个量化模板效果，再确定上线方案（参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) “计费说明”与“常见问题”）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


