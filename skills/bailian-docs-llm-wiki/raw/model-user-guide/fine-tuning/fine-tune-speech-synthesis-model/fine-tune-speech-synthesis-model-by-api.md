# CosyVoice模型调优

本文档介绍如何对阿里云百炼提供的 CosyVoice 语音合成模型进行 SFT（`efficient_sft`）调优。**当前调优任务仅支持通过 API（HTTP）方式发起，控制台暂不支持。**

## **适用范围**

CosyVoice 模型调优面向**同一发音人**多条录音的高还原度专属音色定制：当单条音频的[声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)仍达不到目标还原度，且能够准备同一发音人的多条 / 数小时录音时，可通过调优 API 训练独立部署的专属音色模型。

### **适用场景**

-   **品牌 / IP 形象的高还原度音色定制**：已积累同一发音人（品牌代言人、虚拟主播、IP 形象等）的多条 / 数小时高质量录音，希望在单条音频复刻的基础上进一步抬高对该发音人的还原度上限。
    
-   **长篇有声内容的稳定音色生产**：有声书、播客、纪录片解说、企业培训课件等场景，需要在数十小时合成中保持音色、语气与节奏稳定，且对该发音人已有充足的录音素材。
    

**说明**

**训练数据应为同一发音人**：CosyVoice 调优产出的是单音色模型，训练数据混合多个发音人会导致音色还原度下降。

### **调优规格**

-   **支持的调优方式**：SFT 高效微调（`efficient_sft`），暂不支持 CPT、DPO 等其他训练方式。
    
-   **支持调优的模型**：`cosyvoice-v3-flash`。
    
-   **支持的地域**：CosyVoice 模型调优服务仅支持**华北2（北京）**地域。
    

### **调优产物**

调优产物是一个独立部署的新模型，而不是基础模型下的音色 ID；该模型仅承载训练习得的单一音色，调用时 `voice` 参数必须固定为 `default`，无法切换至其他音色。

### **能力边界**

以下能力由基础模型 `cosyvoice-v3-flash` 决定，无法通过调优新增、扩展或改变：

-   **语种支持**：训练数据语种必须为基础模型已支持的语种。使用基础模型不支持的语种（例如保加利亚语）训练，模型仍无法合成该语种的语音。
    
-   **请求级控制接口**：调优产物支持 [SSML 与 LaTeX](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)（请求中精细控制语速、语调、停顿、音量、发音等）与 LaTeX（数学公式朗读），**不支持指令控制功能**，调用时不可传入 `instruction` 参数。
    
-   **声音复刻 / 声音设计**：调优产物为单音色独立模型（`voice="default"` 锁死），不再提供声音复刻、声音设计能力。如需创建新的音色 ID，请使用基础模型的[声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)或[声音设计](https://help.aliyun.com/zh/model-studio/voice-design-user-guide)。
    

## **是否需要调优？**

模型调优需要准备数据集、等待训练完成、部署模型并承担相应费用，工程量与成本均高于基础模型直接调用。

**下列场景应优先使用对应的独立功能，而不是模型调优**：

**目标**

**推荐使用的能力**

**说明**

仅有单条音频可用，需要快速克隆某个发音人

[声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)

声音复刻是基础模型已支持的独立功能，输入一段音频即可创建专属音色 ID。

在无录音素材的情况下生成全新音色（仅有文字描述）

[声音设计](https://help.aliyun.com/zh/model-studio/voice-design-user-guide)

声音设计直接根据文字描述生成新音色 ID。

在请求级动态调整朗读风格（语速、语调、停顿、情绪、音量等）

指令控制 或 SSML

CosyVoice 提供两种请求级控制机制，均无需训练新模型：**指令控制**用自然语言描述目标，可覆盖语速、情绪、风格，详见[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)；**SSML** 在文本中嵌入标签，精细控制语速、语调、停顿、音量、发音等（**不涉及情绪 / 风格**），详见[SSML 与 LaTeX](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)。

让模型支持基础模型不具备的语种

**调优无法实现，请勿使用**

调优不会扩展基础模型的语种支持范围。详见[能力边界](#cv-scope-title)中**语种支持**条目。

## **计费说明**

CosyVoice 模型调优涉及两部分费用：**训练费用**（按训练消耗的 Token 数）与**部署费用**（按模型单元的使用时长）。

### **训练费用**

按训练消耗的 Token 数计费，单价为 **0.2 元 / 千 Tokens**。

单次任务的 Token 消耗按下式估算：

消耗 Tokens\=(lm\_max\_epoch+fm\_max\_epoch)×25×训练集总时长(秒)

其中 `lm_max_epoch` 与 `fm_max_epoch` 为[超参数](#cv-create-hp-title)中设置的 LM 与 FM 训练轮次；训练集总时长为[调优数据集](#cv-dataset-title)中全部音频文件的总秒数。提高任一轮次或扩大训练集均会线性增加 Token 消耗。

### **部署费用**

调优后的模型部署后按**模型单元的使用时长**计费，公式为：费用\=使用时长（小时）×模型单元数量×模型单元单价。

其中，模型单元数量\=单副本模型单元×部署副本数，可选的模版及对应的模型单元类型参见[部署模版](#cv-deploy-sub-template-t)；各模型单元类型的单价、计费起止时刻请参见[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

## **前提条件**

-   已阅读[模型调优简介](https://help.aliyun.com/zh/model-studio/model-training-overview)，了解模型调优的基本概念、流程及数据格式要求。
    
-   已开通服务并获得 API-KEY，请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   如果使用[阿里云子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)（[RAM 用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），请为该子账号授予调用、训练和部署所需的[权限](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。
    

**说明**

本文档中所有 curl 示例均使用 macOS / Linux 环境变量语法 `${DASHSCOPE_API_KEY}`。Windows CMD 请替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`。

## **操作流程**

**术语约定**：本文中“模型调优”特指对基础模型 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），下文不再区分“调优 / 微调 / SFT”。“调优产物 / 调优后模型 / Checkpoint”指训练完成后的模型工件，“部署实例”指基于这些工件创建的、可调用的 `deployed_model`。

1.  **准备调优数据集**：按指定目录结构准备训练音频（`.wav`）与样本文件（`data.jsonl`），打包为 `.zip`。
    
2.  **上传调优文件**：将 `.zip` 上传到阿里云百炼，获取文件 ID（`file_id`）。
    
3.  **创建调优任务**：基于 `file_id` 启动训练，获取任务 ID（`job_id`）与调优后模型 ID（`finetuned_output`）。
    
4.  **查询任务状态与日志**：等待训练完成（状态变为 `SUCCEEDED`），如需排查可拉取训练日志。
    
5.  **部署并调用调优后的模型**：将调优成功的模型 ID 部署为可调用的服务，然后像调用基础模型一样使用它。
    

实测耗时与费用样本（最小化超参 vs 推荐超参）见[超参数说明](#cv-create-hp-title)末尾的对比表。

## **准备调优数据集**

**语种约束（适用于本节所有规格）**：训练数据涉及三类语种约束，下文表格不再重复展开：

-   **音频语种**必须为基础模型 `cosyvoice-v3-flash` 已支持的语种。
    
-   **文本语种**（`data.jsonl` 中 `text` 字段）必须与对应音频的语种保持一致。单条样本包含多语种混读时的处理方式见下方**允许多语种混合**条目。
    
-   **不可扩展**：基础模型不支持的语种无法通过调优新增，例如使用保加利亚语音频训练，模型仍无法合成保加利亚语。
    
-   **允许多语种混合**：同一训练集中的不同样本可以分属不同语种（如部分中文、部分英文），不影响单语种的合成质量。单条样本内出现多语种混读（如"Hello 世界"）时，`text` 字段应按实际读音转写对应文字。
    
-   **辅助语种音素覆盖**：当训练集以一种语种为主、辅以少量其他语种时（如中文为主 + 少量英文），辅助语种的训练样本应尽量覆盖该语种的全部音素（以美式英语为例，需覆盖 20 个元音和 24 个辅音），以保证辅助语种的音色还原度。
    

### **音频规格要求**

**规格项**

**要求**

音频格式

`.wav`

采样率

不低于 16 kHz。

单条音频时长

推荐 2 秒 ~ 30 秒；最低不少于 1 秒。

语种

详见本节首段「语种约束」。

文本语种

详见本节首段「语种约束」。

录音环境与内容

建议在录音棚或低噪环境录制以减少背景噪声。训练音频中的副语言内容（笑声、叹气、咳嗽、呼吸声、长停顿等）会被调优学习，模型推理时将根据上下文自动在合适位置产出同类声音；如需产出更纯净的语音，建议在数据准备阶段预先清洗这些内容。

**重要**

-   **训练数据特征直接影响调优产物**：调优本质是拟合训练数据集的声学特征，训练音频中发音人的语速、情感倾向与停顿节奏等统计特性会直接反映在调优产物的默认合成风格上。例如训练数据以慢速平静朗读为主，产物推理时默认语速和情感倾向也会偏慢偏平。请根据目标合成场景选择风格一致的训练音频。
    
-   **警惕训练音频中的错读**：若训练数据中存在非标准读音（如将"捕捉"读成 pǔ zhuō），调优产物可能复现该读音，且出现次数越多越容易被学习。建议在标注阶段人工复核音频中的字词读音准确性。
    

### **目录结构**

将训练样本组织为以下目录结构，并将整个目录打包为 `.zip` 压缩包后上传：

```
user_data/
├── data.jsonl           # 训练样本列表（必需）
└── train/               # 训练音频目录（所有训练 wav 放在这里）
    ├── 100001.wav
    ├── 100002.wav
    └── ...
```

### **data.jsonl 格式**

`data.jsonl` 文件每行一个训练样本：

```
{"wav_fn": "train/100001.wav", "text": "你好。"}
{"wav_fn": "train/100002.wav", "text": "我明白了。"}
```

**字段说明**

**字段**

**必填**

**说明**

`wav_fn`

是

训练音频的相对路径，**必须以** `**train/**` **为前缀**（与目录结构一致），例如 `train/100001.wav`。系统加载时拼接为 `{data_dir}/{wav_fn}`，其中 `{data_dir}` 为 zip 解压后的根目录（即 `user_data/`）。

`text`

是

对应的文本。当前版本必填，ASR 自动补齐功能未开放。

**文本写法建议**：

-   **无需归一化**：数字、英文 / 中文混排、标点符号等无需做特殊归一化处理，按音频中的自然念法书写即可。
    
-   **去除特殊符号**：建议提前去除文本中不发音的特殊符号（如 emoji、装饰符号、控制字符等），仅保留与音频实际发音对应的内容。
    
-   **禁止包含标记语言**：`text` 字段必须为**纯文本**，不得包含 SSML 标签、LaTeX 公式、指令控制语句或情感标注；调优阶段不解析这些标记，写入只会作为字符序列被错误地学进文本到语音的映射。请求级标记语言（SSML / LaTeX）应在调用调优产物时使用；调优产物对各请求级控制接口的支持范围详见[能力边界](#cv-scope-title)中的**请求级控制接口**条目。
    

### **数据量建议**

-   **推荐数据量**：训练音频总时长在 **1~10 小时** 之间即可获得较好效果，超过 10 小时收益不明显。
    
-   **样本条数**：建议训练音频不少于 **150 条**，以保证调优效果稳定；算法侧与平台侧对 `data.jsonl` 内的样本条数均无明确上限，可按总时长目标自由组织。
    

**说明**

训练数据总时长直接影响 Token 消耗与训练时长，计费公式见[计费说明](#cv-billing-title)。

## **上传调优文件**

将打包好的 `train_data.zip` 通过 multipart/form-data 上传到阿里云百炼平台。关键字段：`files`（本地 zip 路径）、`purpose`（固定填 `fine-tune`）、`descriptions`（可选）。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/files' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--form 'files=@"train_data.zip"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="训练语音包"'
```

**说明**

请保存响应中的 `file_id`，这是上传数据集的唯一标识，下一步创建调优任务时需要使用。完整请求/响应字段说明请参见 [上传文件](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service#d031ae7105c1g)。

## **创建调优任务**

使用上一步获取的 `file_id` 启动训练任务。

**调优平台同一时刻仅运行一个训练任务**。提交时如已有任务在运行，新任务将进入排队状态（`QUEUING`）直至前序任务结束；规划任务时序时请预留排队时间。

**说明**

**以下示例使用最小化超参**（`lm_max_epoch=4`、`fm_max_epoch=4` 等），**仅用于快速跑通验证流程，不可直接用于生产调优**。生产场景请使用[超参数说明](#cv-create-hp-title)中给出的推荐值（`lm_max_epoch=60`、`fm_max_epoch=100` 等），按推荐超参训练 Token 消耗与训练耗时约为本示例的 **20 倍**。

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json' \
--data '{
    "model": "cosyvoice-v3-flash",
    "training_file_ids": [
        "<替换为训练数据集的file_id>"
    ],
    "hyper_parameters": {
        "lm_max_epoch": 4,
        "lm_step": 1,
        "lm_num": 2,
        "fm_max_epoch": 4,
        "fm_step": 2,
        "fm_num": 2,
        "lm_batch_size": 1000,
        "fm_batch_size": 2000
    },
    "training_type": "efficient_sft"
}'
```

关键请求字段：`model` 固定为 `cosyvoice-v3-flash`，`training_type` 固定为 `efficient_sft`，`training_file_ids` 仅支持挂载一个训练文件 ID，`hyper_parameters` 内 8 个 LM / FM 子字段全部必填。每个字段的取值范围、类型、传参方式请参见 [创建调优任务](https://help.aliyun.com/zh/model-studio/create-fine-tuning-job-api)。

**说明**

请求成功后，请保存响应中的两个关键字段：`output.job_id`（任务 ID，下一步查询任务状态与日志时使用）与 `output.finetuned_output`（调优后模型 ID，训练完成后用于部署模型）。任务创建后 `status` 初始为 `PENDING`，将随训练进度变化。响应字段的完整说明请参见[创建调优任务](https://help.aliyun.com/zh/model-studio/create-fine-tuning-job-api)中的返回参数。

### **超参数说明**

CosyVoice 调优涉及两个子网络：**LM**（Language Model，将文本转为离散语音 token 的自回归语言模型，**对韵律影响较大**）与 **FM**（Flow Matching，将语音 token 还原为 Mel 谱的流匹配模型，**对音色还原度影响较大**），两者已解耦、可独立调整，训练超参分别以 `lm_*` 与 `fm_*` 前缀区分。超参数决定训练轮次与 Checkpoint 保存策略，直接影响调优耗时、Token 消耗与最终模型效果。

**建议先用以下推荐值跑通一次完整流程，根据效果再决定是否调整：**

-   **LM 网络**：`lm_max_epoch=60`，`lm_step=5`，`lm_num=3`，`lm_batch_size=1000`。
    
-   **FM 网络**：`fm_max_epoch=100`，`fm_step=10`，`fm_num=3`，`fm_batch_size=2000`。
    

其中 `*_max_epoch` 为训练总轮次，`*_step` 为保存 Checkpoint 的步长，`*_num` 为最多保留的 Checkpoint 个数，`*_batch_size` 为训练批次大小。各字段的完整取值范围请参见 [CosyVoice 语音合成模型 hyper\_parameters](https://help.aliyun.com/zh/model-studio/create-fine-tuning-job-api#m04a5iuadpoqq)。

**说明**

提高 `lm_max_epoch` 或 `fm_max_epoch` 会按计费公式线性增加 Token 消耗与训练时长（详见[训练费用](#cv-billing-train-title)）。同时，**训练轮次越高，基础模型原有能力的"遗忘"越严重**，可能导致长文本稳定性、多音字准确率等方面退化。推荐值（`lm_max_epoch=60`、`fm_max_epoch=100`）为兼顾音色还原度与基础能力保留的经验值。

**实测对照**：以下为一次实操样本数据，便于您在开工前对耗时与费用建立预期，**实际数值随数据量、超参与队列等待时间不同而变化**。

**项目**

**实测值**

训练样本量

99 条音频（数据集压缩包约 37 MB）

超参取值

`lm_max_epoch=4 / lm_step=1 / lm_num=2 / lm_batch_size=1000`；`fm_max_epoch=4 / fm_step=2 / fm_num=2 / fm_batch_size=2000`

训练总耗时

约 37 分钟（从 `PENDING` 进入 `SUCCEEDED`）

消耗 Token 数

约 99,406 Tokens

费用估算

约 19.88 元（按 0.2 元 / 千 Tokens 计）

**说明**

本表数字基于最小化超参实测，按推荐超参训练 Token 消耗、费用与耗时约为本表的 **20 倍**，**请勿直接据此预估生产成本**。

### **模型产出（Checkpoint）**

单次调优任务可能产出多个 Checkpoint（候选模型，可通过[列举 Checkpoint](https://help.aliyun.com/zh/model-studio/list-checkpoints-api)接口查看），具体数量与排序由超参数中的 `lm_num`、`fm_num` 与 `*_step` 共同决定。

1.  **选模型**：分别从 LM、FM 的最大轮次往回数，每隔 `*_step` 选一个，共选 `*_num` 个。
    
2.  **组合**：LM 与 FM 的选择做全排列，候选 Checkpoint 数量 = `lm_num × fm_num`。
    
3.  **排序**：按 `LM 轮次 × FM 轮次` 从大到小排序（乘积越大代表双端训练越充分，越靠前）。
    
4.  **截断**：在上一步**降序排序**结果上从前往后截取，最多保留 **10** 个；候选不足 10 个时全部输出。
    
5.  **命名**：`checkpoint-{LM 轮次 4 位补零}{FM 轮次 4 位补零}`，例如 LM 4 / FM 4 输出为 `checkpoint-00040004`。
    

**示例**：以参数 `lm_max_epoch=4, lm_step=1, lm_num=2, fm_max_epoch=4, fm_step=2, fm_num=2` 为例：

-   LM 选出：4、3（从 4 开始，每次减 `lm_step=1`，共 `lm_num=2` 个）。
    
-   FM 选出：4、2（从 4 开始，每次减 `fm_step=2`，共 `fm_num=2` 个）。
    
-   全排列得到 4 个候选，按乘积降序输出：
    

**排序**

**LM / FM 轮次**

**乘积**

**Checkpoint 名称**

1

LM 4 / FM 4

16

`checkpoint-00040004`

2

LM 3 / FM 4

12

`checkpoint-00030004`

3

LM 4 / FM 2

8

`checkpoint-00040002`

4

LM 3 / FM 2

6

`checkpoint-00030002`

## **查询任务状态与日志**

创建调优任务后，训练过程通常持续数十分钟到数小时（取决于训练超参与数据集大小）。可使用以下两个接口跟踪进度：通过**查询任务详情**掌握当前所处阶段，通过**获取训练日志**排查异常或确认训练进展。

### **查询任务详情**

使用创建任务时返回的 `job_id` 查询任务状态。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

响应中 `output.status` 字段表示当前阶段：`PENDING`（待开始）→ `QUEUING`（排队中，平台同一时刻仅运行一个训练任务）→ `RUNNING`（训练进行中）→ `SUCCEEDED`（训练成功）。异常终止状态包括 `FAILED`（训练失败）、`CANCELING`（取消中）与 `CANCELED`（已取消）。状态字段的完整定义请参见[查询调优任务详情](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api)。

**说明**

任务状态变为 `SUCCEEDED` 后，可使用上一步保存的 `finetuned_output` 进入下一步部署模型。

### **获取训练日志**

当任务长时间停留在某一状态、或进入 `FAILED` 状态时，可拉取训练日志辅助排查。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/logs?offset=0&line=1000' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

通过 `offset` 控制起始位置，`line` 控制最多返回的行数（示例每次拉取 1000 行）。响应字段说明请参见[查询调优日志](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-logs-api)。

## **部署模型**

任务状态变为 `SUCCEEDED` 后，调优产物 `finetuned_output`（**调优后模型的唯一 ID**，对应[模型产出](#cv-create-ckpt-title)中排序最靠前的 Checkpoint）即可投入部署。

### **部署模版**

**模型单元（Model Unit，MU）**是阿里云百炼平台衡量推理算力的最小单位，不同**模型单元类型**对应不同的算力与单价；**单副本模型单元**则表示部署一个副本所占用的模型单元个数。部署费用直接由实际占用的模型单元数量决定。

**部署模版**：预置了一组部署规格（包括**模型单元类型**与**单副本模型单元**），定义了单个副本所占用的算力资源；选择不同模版，意味着选择不同的推理性能与单位成本组合。下表**模型单元类型**列中的 V/II 为模型单元规格的罗马数字标识，对应 API 响应中 `model_unit_spec` 字段的 `MU5`/`MU2`。CosyVoice 调优模型当前提供以下两种部署模版：

**模版名称**

**模型单元类型**

**单副本模型单元**

**适用场景**

单机部署

V 型模型单元

1

高性价比部署方案，在保证合理推理性能的同时优化单位成本，适合预算敏感但需稳定服务的中低负载场景。

单机部署-旗舰级复杂推理

II 型模型单元

8

面向高复杂负载场景（如超大模型 + 长上下文），单位副本提供更强的推理能力。

**计费方式**：部署费用与模型单元数量（即**总模型单元**）直接相关，按以下公式计算：模型单元数量\=单副本模型单元×部署副本数。

因此**选择不同模版、设置不同副本数都会直接改变计费金额**，请在部署前结合业务负载与预算评估。完整费用公式与各模型单元类型的单价，请参见[部署费用](#cv-billing-deploy-title)。

**部署方式**：选定部署模版后，根据使用场景从以下任一方式完成部署：

### **方式一：通过控制台部署（推荐日常使用）**

**操作入口**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)的**我的模型**页面，找到调优成功的模型并提交部署。完整操作步骤请参见[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

**关键参数**：仅需选择以下两项，其余字段由模版与副本数自动决定：

-   **部署模版**：从 **单机部署**、**单机部署-旗舰级复杂推理** 中二选一，二者区别见[部署模版](#cv-deploy-sub-template-t)。
    
-   **部署副本数**：实例个数，按业务并发吞吐需求设置（≥ 1 的整数）。
    

**完成后状态**：控制台展示部署实例 ID 及状态变化（`PENDING` → `DEPLOYING` → `RUNNING`），状态变为 `RUNNING` 即可调用。

### **方式二：通过 API 部署（推荐自动化集成）**

API 部署需按以下顺序调用三个接口；各字段完整的取值约束请参见[模型部署](https://help.aliyun.com/zh/model-studio/deployments-api/)。

1.  **查询可部署的模型**（`GET /api/v1/deployments/models`）：获取后续创建部署所需的 `model_name`、`template_id` 与 `capacity_unit_per_instance`：
    
    ```
    curl 'https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom' \
        --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
        --header 'Content-Type: application/json'
    ```
    
    **响应样例**（节选关键字段）：
    
    ```
    {
      "output": {
        "models": [
          {
            "model_name": "cosyvoice-v3-flash-ft-202605271743-dd2a",
            "plans": [
              {
                "plan": "mu",
                "templates": [
                  {
                    "template_name": "单机部署",
                    "template_id": "dps-20260521172224-1vabse",
                    "template_desc": "高性价比部署方案，...",
                    "roles": {
                      "unified": {
                        "model_unit_spec": "MU5",
                        "capacity_unit_per_instance": 1
                      }
                    }
                  },
                  {
                    "template_name": "单机部署-旗舰级复杂推理",
                    "template_id": "MU2",
                    "template_desc": "高复杂负载，超大模型 + 长上下文。",
                    "roles": {
                      "unified": {
                        "model_unit_spec": "MU2",
                        "capacity_unit_per_instance": 8
                      }
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    }
    ```
    
    **定位本次要部署的模型**：响应中 `output.models` 为所有可部署模型的列表，从中找到 `model_name` 等于[创建调优任务](#cv-create-title)返回的 `finetuned_output` 的那条记录，其下的 `plans[].templates` 即该模型可用的部署模版列表。
    
2.  **创建部署任务**（`POST /api/v1/deployments`）：使用上一步获取的参数提交部署请求。下方示例选用 **单机部署** 模版，部署 1 个副本：
    
    ```
    curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
    --header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
    --header 'Content-Type: application/json' \
    --data '{
        "model_name": "<MODEL_NAME>",
        "plan": "mu",
        "deploy_spec": "<TEMPLATE_ID>",
        "capacity": 1,
        "billing_method": "POST_PAY"
    }'
    ```
    
    **请求结果**：响应中 `output.deployed_model` 即为部署实例 ID，**后续调用模型时需将其作为** `**model**` **参数传入**。
    
    **关键参数**（占位符 `<MODEL_NAME>`、`<TEMPLATE_ID>` 均取自上一步响应）：
    
    -   `model_name`：填写上一步响应中匹配 `finetuned_output` 的那条记录的 `model_name`。
        
    -   `plan`：当前固定为 `"mu"`（按模型单元的使用时长计费）。
        
    -   `deploy_spec`：填写上一步响应中所选模版的 `template_id`，例如 **单机部署** 当前为 `dps-20260521172224-1vabse`、**单机部署-旗舰级复杂推理** 为 `MU2`。请**始终以上一步的实时返回值为准**，不要硬编码。
        
    -   `capacity`：本次部署占用的**总模型单元数量，与计费直接挂钩**。取值必须是上一步中 `capacity_unit_per_instance` 的整数倍；实际部署的副本数\=capacity\_unit\_per\_instancecapacity​。
        
        **取值示例**：
        
        -   **单机部署**（`capacity_unit_per_instance = 1`）：`capacity=1` → 1 个副本；`capacity=4` → 4 个副本。
            
        -   **单机部署-旗舰级复杂推理**（`capacity_unit_per_instance = 8`）：`capacity=8` → 1 个副本；`capacity=16` → 2 个副本；`capacity=1` 会被拒绝（不是 8 的整数倍）。
            
    -   `billing_method`：当前支持 `"POST_PAY"`（后付费）。
        
    
    **API 字段与控制台部署页面的对应关系**：
    
    **API 字段**
    
    **控制台对应**
    
    `model_name`
    
    在**我的模型**页面选定的调优模型
    
    `deploy_spec`
    
    在 **部署模版** 处选择 **单机部署** 或 **单机部署-旗舰级复杂推理**
    
    `capacity`
    
    **总模型单元**（控制台按总模型单元\=单副本模型单元×部署副本数自动计算并展示）
    
    `plan`、`billing_method` 在控制台无对应字段（控制台部署默认即按模型单元用时计费的后付费方式）。
    
    **重要**
    
    `capacity` **不是**部署副本数，而是总模型单元数量；提交前请按上方公式与示例核对。
    
3.  **查询部署状态**（`GET /api/v1/deployments/<deployed_model>`）：部署任务将经历 `PENDING` → `DEPLOYING` → `RUNNING` 多个阶段，可调用以下接口轮询状态：
    
    ```
    curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为 deployed_model 字段值>' \
    --header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
    --header 'Content-Type: application/json'
    ```
    
    当响应中 `status` 字段值为 `RUNNING` 时，表示该模型已可供调用。更多模型部署相关的操作（如扩缩容、下线等）请参见[模型部署](https://help.aliyun.com/zh/model-studio/deployments-api/)。
    

## **调用模型**

当模型部署状态为 `RUNNING` 时，调优后的模型即可投入业务调用。调用方式（含 endpoint、请求体字段、典型响应与音频取回方式）与其他 CosyVoice 模型一致，完整说明请参见用户指南 [语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。相比基础模型 `cosyvoice-v3-flash` 的调用方式，**仅需调整以下两个请求参数**，其他字段（`text`、`format`、`sample_rate` 等）保持一致：

-   `model`：设置为部署任务成功后的实例 ID，即部署响应中 `output.deployed_model` 字段的值。
    
-   `voice`：必须固定为 `"default"`，代表训练数据所对应的专属音色；传入预置音色名或音色复刻 ID 会请求失败。
    

完整调用示例如下，根据业务场景选择**非实时（HTTP）**或**实时（WebSocket）**方式：

## **非实时（HTTP）**

单次合成完整文本，响应中包含合成音频的 URL，有效期为 24 小时。

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "<替换为部署响应中的 deployed_model 字段值>",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "default",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

## **实时（Python WebSocket）**

通过 DashScope Python SDK 接入 WebSocket 合成接口，依赖 `dashscope` 包。**WebSocket 接口本身支持边合成边推送的流式回调**，为方便快速验证，**本示例改用同步调用** `**synthesizer.call(text)**` **一次性返回完整音频**；如需流式回调（边合成边播放）的完整写法，请参见[用户指南](https://help.aliyun.com/zh/model-studio/tts-model/)中的流式合成完整示例。

```
# coding=utf-8
import os
import dashscope
from dashscope.audio.tts_v2 import *

dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'

# 替换为部署响应中的 deployed_model 字段值；voice 固定为 "default"
model = "<替换为部署响应中的 deployed_model 字段值>"
voice = "default"

synthesizer = SpeechSynthesizer(model=model, voice=voice)
audio = synthesizer.call("我家的后面有一个很大的花园。")

print('[Metric] requestId 为：{}，首包延迟为：{} 毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

with open('output.mp3', 'wb') as f:
    f.write(audio)
```

### **调用观测与问题定位**

每一次调用都建议落入业务日志，以便事后追溯异常请求与诊断性能问题。重点采集以下三类信息：

-   **请求 ID**（`request_id`）：WebSocket SDK 通过 `synthesizer.get_last_request_id()` 获取（参见前文 [实时（Python WebSocket）](#cv-deploy-sub-call-demo-ws-t) 示例）；HTTP 调用方式下的获取位置请参考[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。排查异常或回溯问题时请始终保留该 ID。
    
-   **首包延迟**：WebSocket SDK 通过 `synthesizer.get_first_package_delay()` 获取首个音频包到达时延（毫秒），是衡量实时合成体感的核心指标，前文 [实时（Python WebSocket）](#cv-deploy-sub-call-demo-ws-t) 示例代码已演示其打印用法。
    
-   **错误码与错误信息**：错误响应中的 `code`、`message` 字段用于区分鉴权失败、配额耗尽、模型未就绪、文本超限等不同失败原因，建议按错误码分别设置告警与排查路径。
    

**采集字段对照**（建议入库的最小集合）：

**观测项**

**HTTP 响应字段**

**WebSocket SDK 方法**

**建议日志键名**

请求 ID

`request_id`

`synthesizer.get_last_request_id()`

`tts_request_id`

首包延迟

不适用（HTTP 一次性返回）

`synthesizer.get_first_package_delay()`

`tts_first_package_ms`

错误码与错误信息

`code` / `message`

错误回调中的 `code` / `message`

`tts_error_code` / `tts_error_msg`

建议在业务日志中将 `request_id` 与业务侧请求 ID 关联存储，并保留至少与 SLA 一致的时间窗口，以便后续核查。

## **应用于生产环境**

调优模型部署进入 `RUNNING` 状态后并不意味着工作结束。在正式承载业务流量前后，请关注以下 4 项调优特有的部署运维实践，以提升上线质量、控制成本并降低后续运维风险（调用层面的观测与日志规范见[调用观测与问题定位](#cv-prod-observe-t)）。

**说明**

**正式上线前建议小范围验证基础能力**：调优产物的非音色能力（多音字与专有名词读音、长文本稳定性等）继承自基础模型 `cosyvoice-v3-flash`，但可能受训练数据质量和训练轮次影响（详见[音频规格要求](#cv-dataset-audio-title)与[超参数说明](#cv-create-hp-title)），建议在您的目标使用场景上抽样实测后再放量。

### **选用更优的 Checkpoint**

默认部署的 `finetuned_output` 仅对应[模型产出（Checkpoint）](#cv-create-ckpt-title)中排序最靠前的 Checkpoint，**但该 Checkpoint 不一定是主观听感最佳**。正式上线前建议人工评测排序前 2~3 名的 Checkpoint，从中挑选最贴近目标音色的版本。

**切换部署到其他 Checkpoint 的步骤**：

1.  通过 `GET /api/v1/fine-tunes/{job_id}/checkpoints` 拉取本次任务全部 Checkpoint，从响应 `output[*].model_name` 字段获取每个 Checkpoint 对应的模型 ID（**仅在** `**status=SUCCEEDED**` **时返回**）。完整字段说明请参见[查询调优任务 Checkpoint 列表](https://help.aliyun.com/zh/model-studio/model-training-api-reference#cv-cp-h2)。
    
2.  将选中的 `model_name` 作为[方式二：通过 API 部署（推荐自动化集成）](#cv-deploy-sub-api-t)中“创建部署任务”步骤的入参，得到独立的 `deployed_model`。**不同 Checkpoint 必须使用各自独立的部署实例**，无法在已有部署上原地切换底层模型。
    
3.  同一时间存在多个评测部署会按各自占用的模型单元数量累加计费，请参考[部署费用](#cv-billing-deploy-title)预估并发评测成本，对比完成后及时下线落选实例（参见[及时下线不再使用的部署](#cv-prod-offline-t)）。
    

### **及时下线不再使用的部署**

在以下场景中，部署实例不再承载业务流量，应立即下线以停止计费：完成多 Checkpoint 评测后落选的实例、被新版本替换的旧实例、临时压测或验证使用的实例、创建失败需要重建的实例等。

**下线方法**：调用 `DELETE /api/v1/deployments/{deployed_model}`，响应中 `output.status` 变为 `DELETING` 即表示受理。完整字段说明请参见[删除部署](https://help.aliyun.com/zh/model-studio/delete-deployment-api)。

**重要**

部署费用按**模型单元的使用时长**计费，部署运行期间持续按时长扣费，**即使无调用流量也照常计费**。多 Checkpoint 评测期与版本切换期实例数量较多，尤其需要在评测/切换完成后立即清理不再使用的实例。计费公式与起止时刻请参见[部署费用](#cv-billing-deploy-title)。

### **副本数规划与扩缩容**

当业务并发上量、整体吞吐不足或活动期需要弹性扩容时，需要调整部署的副本数。不同部署模版（**单机部署** 与 **单机部署-旗舰级复杂推理**）对应的单副本算力与适用场景不同，详见[部署模版](#cv-deploy-sub-template-t)，请结合业务并发反推副本数。

**扩缩容方法**：调用 `PUT /api/v1/deployments/{deployed_model}/scale`，请求体传入新的 `capacity`。注意 `capacity` 是**总模型单元数量**而非副本数，且必须为该模版 `capacity_unit_per_instance` 的整数倍，取值示例参见[取值示例](#cv-deploy-api-step2-field-li-cap-examples-p)。完整字段说明请参见[部署扩缩容](https://help.aliyun.com/zh/model-studio/scale-deployment-api)。

副本数线性影响计费金额，扩容前请按[部署费用](#cv-billing-deploy-title)的公式估算成本变化。

### **重新调优后的版本切换**

当补充新数据或调整超参时，**推荐始终从基础模型** `**cosyvoice-v3-flash**` **重新训练**，不建议在已调优产物上做增量训练。重新调优产出的是新的 `finetuned_output`，**不是同一模型的新版本**，必须创建新的部署实例，无法在旧 `deployed_model` 上原地替换底层模型。

**推荐切换流程**：

1.  用新模型 `model_name` 走[方式二：通过 API 部署（推荐自动化集成）](#cv-deploy-sub-api-t)，创建独立部署，得到新的 `deployed_model`。**不要直接对旧实例做扩缩容或修改设置**，这两种操作都不会更换其底层模型。
    
2.  业务侧通过灰度或影子流量并行调用新旧两个 `deployed_model`，对比音质、首包延迟与错误率。
    
3.  验证通过后切流量到新部署，再下线旧部署（参见[及时下线不再使用的部署](#cv-prod-offline-t)），完成版本替换。
    

**重要**

**调优产物冻结在训练时的基础模型版本**：当基础模型 `cosyvoice-v3-flash` 后续升级（如新增语种、扩展 SSML 标签等）时，已部署的调优产物**不会**自动获得升级带来的能力增强，其能力始终锁定在调优时的基础模型版本。如需使用新版本基础模型的能力，须基于新版本重新调优并部署。

## **API 参考**

下表汇总本指南涉及的全部 API：**文中位置**列指向具体使用步骤，**详细参考**列指向接口字段定义文档。

**API 名称**

**方法 / 路径**

**用途**

**文中位置**

**详细参考**

上传调优文件

`POST /api/v1/files`

上传训练数据集 zip

[上传调优文件](#cv-upload-title)

[上传文件](https://help.aliyun.com/zh/model-studio/upload-file-api)

创建调优任务

`POST /api/v1/fine-tunes`

启动训练任务

[创建调优任务](#cv-create-title)

[创建调优任务](https://help.aliyun.com/zh/model-studio/create-fine-tuning-job-api)

查询任务详情

`GET /api/v1/fine-tunes/{job_id}`

跟踪训练进度

[查询任务详情](#cv-query-sub-detail-t)

[查询调优任务详情](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-api)

获取训练日志

`GET /api/v1/fine-tunes/{job_id}/logs`

拉取训练日志辅助排查

[获取训练日志](#cv-query-sub-logs-t)

[查询调优日志](https://help.aliyun.com/zh/model-studio/get-fine-tuning-job-logs-api)

查询 Checkpoint 列表

`GET /api/v1/fine-tunes/{job_id}/checkpoints`

枚举多 Checkpoint 候选并选用更优版本部署

[选用更优的 Checkpoint](#cv-prod-ckpt-t)

[列举 Checkpoint](https://help.aliyun.com/zh/model-studio/list-checkpoints-api)

查询可部署的模型

`GET /api/v1/deployments/models`

获取部署模版与规格

[方式二·步骤 1](#cv-deploy-api-step1-li)

[列举可部署模型](https://help.aliyun.com/zh/model-studio/list-deployable-models-api)

创建部署任务

`POST /api/v1/deployments`

部署调优后模型

[方式二·步骤 2](#cv-deploy-api-step2-li)

[创建部署](https://help.aliyun.com/zh/model-studio/create-deployment-api)

查询部署状态

`GET /api/v1/deployments/{deployed_model}`

轮询部署状态

[方式二·步骤 3](#cv-deploy-api-step3-li)

[查询部署详情](https://help.aliyun.com/zh/model-studio/get-deployment-api)

扩缩容部署

`PUT /api/v1/deployments/{deployed_model}/scale`

调整部署的总模型单元数量

[副本数规划与扩缩容](#cv-prod-capacity-t)

[部署扩缩容](https://help.aliyun.com/zh/model-studio/scale-deployment-api)

下线部署

`DELETE /api/v1/deployments/{deployed_model}`

删除不再使用的部署，停止计费

[及时下线不再使用的部署](#cv-prod-offline-t)

[删除部署](https://help.aliyun.com/zh/model-studio/delete-deployment-api)

语音合成（HTTP）

`POST /api/v1/services/audio/tts/SpeechSynthesizer`

单次合成完整文本

[调用模型](#cv-deploy-sub-call-t)

[非实时语音合成-CosyVoice API参考](https://help.aliyun.com/zh/model-studio/non-realtime-cosyvoice-api/)

语音合成（WebSocket）

`wss://dashscope.aliyuncs.com/api-ws/v1/inference`

流式合成

[调用模型](#cv-deploy-sub-call-t)

[实时语音合成-CosyVoice API参考](https://help.aliyun.com/zh/model-studio/cosyvoice-large-model-for-speech-synthesis/)
