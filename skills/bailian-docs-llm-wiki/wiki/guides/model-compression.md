# model compression

模型压缩是百炼平台提供的量化能力，用于将全精度微调模型转换为低精度版本，在可控精度损失下显著降低部署所需的 MU 规格与推理成本。该功能属于模型生产链路中的可选环节，必须在完成[模型调优](raw/model-user-guide/fine-tuning.md)后执行，且压缩结果不可逆。详细背景和设计边界请参见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。

## 支持的模型与功能

- **支持范围**：仅限通过百炼平台完成微调训练的自定义模型（即“微调产出模型”），不支持基础模型、第三方模型或未完成微调的中间检查点。  
- **技术范畴**：当前仅实现**后训练量化（PTQ）**，不包含结构剪枝、知识蒸馏等其他压缩范式；具体能力边界详见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)。  
- **地域限制**：仅华北2（北京）地域可用。  
- **典型收益**：以 `qwen3.5-flash-2026-02-23` 微调模型为例，压缩后部署规格可从 MU1×2 降至 MU8×1，成本节省约 56%（数据来源：[模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。

## 关键参数

创建压缩任务时需配置以下必填参数：

| 参数 | 说明 |
|------|------|
| **任务名称** | 最长 50 字符，建议含模型简称、量化方式与版本号（如 `qwen35-ft-awq-v1`）。 |
| **量化产出模型名后缀** | 仅小写字母与数字，最长 8 位；将拼接至源模型名后生成新模型 ID（如源模型为 `my-qwen-ft`，后缀为 `awq` → 产出 `my-qwen-ft-awq`）。 |
| **量化模板** | 卡片式选择，模板名中 MU 编号越大，部署规格越小、成本越低，但潜在精度损失可能增加；**切换源模型会自动清空已选模板**（因模板与模型强绑定）。 |
| **校准数据（条件选填）** | 仅当所选模板要求校准时出现；最多选 5 个已在[数据管理](https://help.aliyun.com/zh/model-studio/manage-data)中发布完成的数据集；不支持 OSS 挂载数据集。 |

> **注意**：所有参数在任务创建后不可修改，请在单击**开始压缩**前严格核对——该约束在 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中被明确强调为“重要”。

## 使用方式

1. **前提**：确保工作空间中存在状态为 `SUCCEEDED` 的微调模型（参见 [模型调优](raw/model-user-guide/fine-tuning.md)）；若无可选模型，请先完成训练。
2. **入口**：控制台左侧导航栏 → **模型压缩** → **创建压缩任务**。
3. **配置**：依次填写任务名称、后缀、选择源模型（触发模板加载）、选择量化模板、按需添加校准数据。
4. **提交**：全部必填项合法后，点击**开始压缩**；成功后跳转至任务列表页。
5. **监控**：在任务详情页的**日志**页签中，可设置显示行数、开启自动刷新、下载全量日志；失败时优先查看 ERROR 级日志及详情页错误信息（排查流程见 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。

## 限制和注意事项

- **不可逆性**：压缩后的模型**不支持继续微调**，也**不支持二次压缩**；如需调整，必须回退至上游全精度微调模型重新发起任务（该限制在 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中多次强调）。
- **状态管理**：
  - 仅 `PENDING` / `RUNNING` 状态可**停止**（停止后不可恢复）；
  - 仅终态（`SUCCEEDED` / `FAILED` / `CANCELED`）可**删除**；删除任务记录不影响已产出模型。
- **计费**：压缩任务本身限时免费（截止时间以控制台公告为准）；压缩后模型的部署费用按 MU 规格单独计费，与压缩免费期无关。
- **精度验证**：量化必然引入精度损失，强烈建议在免费期内对同一微调模型尝试多个量化模板，并使用业务测试集验证效果后再正式部署（实践建议出自 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)


