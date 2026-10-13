# 决策模型微调最佳实践

百炼决策模型微调最佳实践——微调、部署与部署后调用全流程

本文帮助您完成决策模型的微调、部署与部署后调用。百炼决策模型以模型名 `decision-model-preview-2026-09-24` 提供服务，支持直接调用与微调；它不生成文本，一次前向输出分类、评分、是非判断及其概率，适合工单分流、内容审核、智能体路由与结果校验等高频决策场景。

微调全流程：**环境准备 → 数据准备 → 训练提交 → 模型部署 → 部署后调用**。

**场景**

**选择**

**典型用例**

需生成文本（对话、代码、写作、推理）

通用大模型

写文案、写代码、问答

封闭集合上的高频决策（分类、评分、是非判断），无需定制

直接用决策模型（零样本调用）

通用工单分流、内容审核

封闭集合决策，但有专属业务规则或领域数据

微调决策模型（本文）

特定业务工单分流、专属评分标准

百炼支持以下模型微调：

**模型名**

**说明**

**微调计费**

`decision-model-preview-2026-09-24`

决策模型，支持微调与调用

限时 0 元/千 token

调用前需完成：

-   **API Key**：从[百炼控制台 API-KEY 页](https://bailian.console.aliyun.com/?tab=app#/api-key)获取 API Key
-   **授权**：请联系商务经理开通
-   **环境变量**：`export DASHSCOPE_API_KEY="你的百炼 API Key"`

## 数据准备

下载[训练数据示例包](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/files/6a4b3c2d1e0f92e3.zip)（含示例数据 `tickets.train.jsonl` / `tickets.development.jsonl`、问题配置 `workload.json`、数据脚本 `gen_data.py` / `split_data.py`）。示例数据已切分好可直接用；自备数据时用脚本合成或切分（见示例包 `README.md`）。

> `gen_data.py` 调用百炼大模型自动标注，会产生用量费用。

每条 JSONL 记录包含输入 `state` 与问题表 `questions`，每个问题携带类型定义、`label`（硬标签）与可选 `target`（软标签）：

```
{
  "state": {"content": "发票抬头写错了，请帮忙重新开票。产品功能正常，也没有其他异常。"},
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "应该由哪个团队处理？",
      "criteria": {"billing": "支付、退款和账单问题", "technical": "产品故障和集成问题"},
      "label": "billing",
      "target": {"billing": 0.96, "technical": 0.04}
    },
    "escalate": {"type": "noul", "instructions": "是否需要立即通知值班人员？", "label": false},
    "severity": {
      "type": "score", "instructions": "这个问题有多严重？",
      "criteria": ["轻微问题，不影响功能", "部分功能受影响，但存在替代方案", "核心功能不可用，没有替代方案", "造成严重业务或安全影响"],
      "label": 0
    }
  }
}
```

`label` 与 `target` 填写规则：

**类型**

**criteria**

**必填 label**

**可选 target**

`choice`

选项名 → 含义的对象

选项名，如 `"billing"`

各选项概率，如 `{"billing": 0.96, "technical": 0.04}`

`noul`

无需填写

布尔值 `true` / `false`

如 `{"true": 0.9, "false": 0.1}`

`score`

从低到高的档位含义数组

从 0 开始的整数下标

以字符串下标为键，如 `{"0": 1.0, "1": 0.0, "2": 0.0, "3": 0.0}`

`target` 应包含全部选项，概率在 0–1 之间且合计为 1；同一任务的训练、评估与线上请求须保持问题 ID、类型、`instructions`、`criteria` 一致，修改选项后同步修改标签与概率键。

## 训练提交

数据集通过百炼 OpenAPI 上传（JSONL 格式），获得 `file_id` 后在微调请求中引用。中国站地址 `https://dashscope.aliyuncs.com`，新加坡站 `https://dashscope-intl.aliyuncs.com`，API Key 与站点对应：

```
curl --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
  --header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
  --form 'files=@"/path/to/train.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="decision-model-preview training dataset"'
```

返回 `file_id`（如 `976bd01a-...`），填入下方微调请求。详见[训练集与评估集](training-set-and-evaluation-set.md)与[调优数据上传规则](text-generation-tuning-data-upload-rules)。

> 数据集上传与微调请求走百炼 OpenAPI，鉴权用 `Authorization: Bearer <API-Key>`。

通过 API 提交微调任务：

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "model": "decision-model-preview-2026-09-24",
    "training_datasets": [
      {"data_source_type": "file_id", "file_id": "your-file-id"}
    ],
    "validation_datasets": [
      {"data_source_type": "file_id", "file_id": "your-file-id"}
    ],
    "hyper_parameters": {
      "n_epochs": 2,
      "learning_rate": "2e-5",
      "batch_size": 1,
      "save_strategy": "epoch",
      "save_total_limit": 1
    },
    "training_type": "efficient_sft",
    "finetuned_output_suffix": "mytune"
  }'
```

输入参数：

**字段**

**必选**

**描述**

`training_datasets`

是

训练数据集列表

`validation_datasets`

否

测试数据集列表

`model`

是

基础模型 ID（支持 `decision-model-preview`，或其他微调任务产出的模型 ID）

`hyper_parameters`

否

超参数，见下表

`training_type`

是

微调方法，选择 `efficient_sft`（LoRA 高效微调）

`job_name`

否

微调任务名称

超参数：

**参数名称**

**默认值**

**类型**

**作用**

`n_epochs`

2

Integer

正整数，完整训练轮数

`learning_rate`

2e-5

Float

正数，学习率

`batch_size`

1

Integer

正整数，每个训练批次的样本数

返回示例（节选）：

```
{
  "request_id": "your-request-id",
  "output": {
    "job_id": "ft-xxxxxxxx",
    "status": "PENDING",
    "finetuned_output": "decision-model-preview-2026-09-24-ft-xxxxxxxx",
    "model": "decision-model-preview-2026-09-24",
    "training_type": "efficient_sft"
  }
}
```

`finetuned_output` 为微调产出的模型名，部署后通过决策调用接口调用（model 字段传该模型名）。

### 训练指标

任务提交后，可在[百炼控制台模型调优](https://bailian.console.aliyun.com/cn-beijing/model/training)查看训练进展与产物。指标页分三组：

**组**

**指标**

**含义**

**方向**

Train

`loss`

训练损失

—

Train

`epoch`

训练轮次

—

Eval

`acc`

准确率

越高越好

Eval

`brier`

Brier 分数，预测概率与真值的均方误差

越低越好

Eval

`ece`

校准误差

越低越好

Eval

`nll`

负对数似然

越低越好

Eval

`temperature`

校准温度

—

Eval

`n_questions`

评估问题数

—

Calibration

`acc` `_after`/`_before`

微调后/前准确率

after 升为好

Calibration

`brier` `_after`/`_before`

微调后/前 Brier 分数

after 降为好

Calibration

`ece` `_after`/`_before`

微调后/前校准误差

after 降为好

Calibration

`temperature`

校准温度

—

Calibration 组看 `_after` 是否相对 `_before` 改善（`acc` 升、`brier`/`ece` 降）即微调提升了校准。

## 模型部署

训练完成后最后一个 Checkpoint 自动发布至[我的模型](https://bailian.console.aliyun.com/cn-beijing/model/custom)。如需发布中间 Checkpoint，前往[模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)产出页手动操作。

在”我的模型”页面部署训练返回的 `finetuned_output`（如 `decision-model-preview-2026-09-24-ft-xxxxxxxx`），部署规格为 MU5×1，部署完成后即可通过决策调用接口调用。部署方式与 MU 单价详见[模型部署](model-deployment-introduction.md)与[模型调优计费](model-training-and-deployment-billing)。

## 部署后调用

部署后通过决策调用接口调用微调产物，`model` 字段传训练返回的 `finetuned_output`（如 `decision-model-preview-2026-09-24-ft-xxxxxxxx`），其余参数与调用 `decision-model-preview` 时相同：

#### curl

```
curl -sS -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/systemone \
  -H "Authorization: $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "decision-model-preview-2026-09-24-ft-xxxxxxxx",
    "state": {"content": "订单支付后超过 24 小时仍未到账，要求立即处理。"},
    "questions": {
      "department": {"type": "choice", "instructions": "应该由哪个团队处理？",
                     "criteria": {"billing": "支付、退款和账单问题", "technical": "产品故障和集成问题"}}
    }
  }'
```

#### Python

```
import os, requests

resp = requests.post(
    "https://dashscope.aliyuncs.com/compatible-mode/v1/systemone",
    headers={"Authorization": os.environ["DASHSCOPE_API_KEY"], "Content-Type": "application/json"},
    json={"model": "decision-model-preview-2026-09-24-ft-xxxxxxxx",
          "state": {"content": "订单支付后超过 24 小时仍未到账，要求立即处理。"},
          "questions": {"department": {"type": "choice", "instructions": "应该由哪个团队处理？",
                       "criteria": {"billing": "支付、退款和账单问题", "technical": "产品故障和集成问题"}}}},
    timeout=60,
)
print(resp.json()["answers"]["department"])
```

## 最佳实践

### 软标签：让模型学会校准

训练数据除 `label`（答案）外，`target` 带[示例包](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/files/6a4b3c2d1e0f92e3.zip)中 `gen_data.py` 调百炼大模型（默认 `qwen3.8-max`）自动标注的概率分布，不只告诉模型答案，还告诉模型有多确定，输出概率更校准。`--target-temp` 调软硬（默认 1.5，越大越平滑、越保留不确定性）；续跑可复用已保存标注只调温度，不再调用 API、不产生费用。

### 遇到无法判断的输入

有些输入信息不足、无法判断（如只说"帮我看下我的工单"没给内容）。用 `--unknowable N` 生成这类样本，`target` 设均匀分布，不参与准确率评估，专门降低模型在信息不足时的过度自信——缺少这类样本时模型仍倾向高置信错答。

### 问题定义要保持一致

微调学的是"输入 + 问题定义 → 答案"的映射（问题定义即 ID、类型、`instructions`、`criteria`）。改了问题定义即分布漂移，准确率下降、校准失效；必须改时用新定义重新准备数据并重训。

## 常见问题

### 数据相关

**Q：微调数据格式和调用格式一样吗？**

不完全一样。训练数据每条多了 `label`（硬标签）和可选 `target`（软标签），调用时不带这两个字段。

**Q：微调数据文件多大限制？**

单个文件最大 300MB，所有有效文件总量配额 100GB，文件数量上限 10000 个。

**Q：微调数据必须是 JSONL 吗？**

是，训练数据必须是 JSONL 格式（每行一个 JSON 对象）。

**Q：label 和 target 都要填吗？**

`label` 必填（硬标签），`target` 可选（软标签）。有 `target` 时须覆盖全部选项、概率 0–1 合计为 1。

**Q：微调数据可以用 gen\_data.py 合成吗？**

可以。示例包含 `gen_data.py`，调用百炼大模型自动标注生成数据（会产生用量费用）。

**Q：微调支持中英文混合数据吗？**

支持。`workload.json` 的 `language` 字段指定语言，可生成中英文数据。

**Q：微调支持从 OSS 导入吗？**

不支持。当前只能通过百炼 OpenAPI 上传数据集（前端上传暂不支持）。

**Q：数据里有 unknowable 会影响准确率吗？**

不会。unknowable 样本不参与准确率评估，只用于降低模型在信息不足时的过度自信。

### 训练相关

**Q：微调需要自己准备 GPU 吗？**

不需要。百炼托管训练，你只需通过 API 提交数据和超参。

**Q：微调支持继续训练吗？**

支持。`model` 参数可传其他微调任务产出的模型 ID，基于微调产物再微调。

**Q：微调后效果一定比基座好吗？**

不一定。效果取决于数据质量和数量，数据质量差可能不如零样本调用。建议先用示例数据验证链路。

### 产物相关

**Q：微调后还能用基座模型吗？**

可以。基座模型 `decision-model-preview` 和微调产物独立，可同时调用。

**Q：微调产物不支持什么？**

同基座，不支持上下文缓存、Function Calling、联网搜索、批量推理、system message、temperature/top\_p/max\_tokens 等采样参数。

**Q：微调产物上下文长度变了吗？**

没变，同基座，最大输入 65535 token。

**Q：微调产物限流和基座一样吗？**

一样，RPM 1200 / TPM 200万（北京与新加坡一致）。

**Q：微调后 confidence 一定变高吗？**

不一定。confidence 是分布集中度统计，微调后是否改善取决于数据。看指标页 Calibration 的 after/before 对比。

**Q：微调产物 model name 怎么命名？**

`finetuned_output_suffix` 字段自定义后缀（最多 8 字符），产物名格式为 `decision-model-preview-2026-09-24-ft-{后缀}`。

**Q：微调支持 choice/noul/score 三种问题吗？**

都支持。三种问题类型都可微调。

### 调用相关

**Q：微调产物调用 endpoint 和基座一样吗？**

一样，都是 `https://dashscope.aliyuncs.com/compatible-mode/v1/systemone`（新加坡站 `dashscope-intl.aliyuncs.com`）。

**Q：微调产物鉴权和基座一样吗？**

不完全一样。微调请求走百炼 OpenAPI 用 `Bearer` 鉴权；推理调用决策调用接口网关不加 `Bearer` 前缀。

### 部署相关

**Q：微调部署规格？**

MU5×1。后付费 21 元/小时（最小计费分钟），预付费 10139 元/月（最小计费天）。

### 其他

**Q：微调收费吗？**

当前限时 0 元/千 token。

**Q：微调支持什么地域？**

北京（`dashscope.aliyuncs.com`）和新加坡（`dashscope-intl.aliyuncs.com`），API Key 与站点对应。

**Q：微调后能改问题定义吗？**

不能直接改。问题定义（ID/类型/instructions/criteria）变了会分布漂移，需重新准备数据重训。

**Q：decision-model-preview 后续会变化吗？**

为预览版，团队持续迭代。对稳定性要求高的业务建议待正式版发布后再接入。

**Q：微调要多少数据起步？**

训练和验证数据集分开上传时要求两个数据集数量不小于微调时的 batch\_size；只上传训练数据集时不少于 batch\_size × 10。推荐数据量：上百条。

**Q：微调一个任务大概多久？**

百炼未给具体时长（高效训练收敛快）；Kev 开源参考单 H100 约 40min（4B 模型，10k 条，2 epoch），百炼决策模型量级接近。

**Q：n\_epochs 设多少合适？**

数据量 <10k 建议 3–5，>10k 建议 1–2；百炼决策模型默认 2（已跑通）。

**Q：微调产物可以删除吗？**

可以。训练完成后可通过 `DELETE /api/v1/fine-tunes/<job_id>` 删除调优任务（训练中不可删），微调产物在"我的模型"页面管理。

## 后续步骤

-   [模型部署](model-deployment-introduction.md)：部署方式与规格
-   [模型调优计费](model-training-and-deployment-billing)：微调与部署计费
-   [在控制台进行模型调优](model-training-on-console)：控制台查看产出与发布
-   [调优数据上传规则](text-generation-tuning-data-upload-rules)：打包规则、大小与数量限制
