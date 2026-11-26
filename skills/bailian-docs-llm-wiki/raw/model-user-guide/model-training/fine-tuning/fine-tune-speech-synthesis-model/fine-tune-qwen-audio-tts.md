# Qwen-Audio-TTS模型调优

使用同一说话人的录音和对应的转写文本，通过阿里云百炼 API 对 Qwen-Audio-3.0-TTS-Flash 进行监督微调（SFT），生成定制音色的语音合成模型。

> **说明**
>
> Qwen-Audio-3.0-TTS-Flash 模型调优属于邀测功能，如需申请开通请联系商务经理。

<a id="适用场景"></a>

<a id="when-to-fine-tune"></a>

## 适用场景

需要还原特定说话人的声音时，可以先用一段参考录音进行[声音复刻](../../../model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md)并试听。如果音色还原度或长篇朗读的稳定性仍达不到要求，且能提供该说话人的多段录音和转写文本，可以考虑调优。

-   **品牌或虚拟角色**：用目标说话人的录音定制专属音色，使角色在不同内容中保持声音辨识度。
-   **有声书等长篇旁白**：用同一位讲述者的朗读录音训练，使不同章节的语气和节奏保持一致。

> **说明**
>
> 如果只有对目标音色的文字描述，可以使用[声音设计](../../../model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-design-user-guide.md)。已有合适的音色，只需调整语速或情绪时，可在合成请求中使用[指令控制](../../../model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#12884a10929p9)。

<a id="前提条件"></a>

<a id="prerequisites"></a>

## 前提条件

-   **支持模型**：Qwen-Audio-3.0-TTS-Flash（模型 ID：qwen-audio-3.0-tts-flash）。
-   **调优方式**：通过 HTTP API 发起监督微调，`training_type` 填写 `sft`。
-   **适用地域**：仅支持华北2（北京）地域。
-   **账号与 API Key**：使用已开通邀测权限的账号，[获取 API Key](../../../../model-api-reference/preparations/get-api-key.md) 并[配置环境变量](../../../../model-api-reference/preparations/get-api-key.md#20b17d4430qvt) `DASHSCOPE_API_KEY`。如使用阿里云子账号（RAM 用户），需先授予模型调用和训练所需[权限](../../../security-and-compliance/permission-management-overview.md)。

<a id="准备数据"></a>

<a id="prepare-data"></a>

## 准备数据

<a id="训练数据"></a>

<a id="training-data"></a>

### 训练数据

每个任务仅支持**一位说话人**。请准备该说话人的 WAV 录音和逐条转写文本，录音总时长**必须超过 30 分钟**。

-   **录音规格与数据量**：建议使用 16 kHz 或更高采样率，按完整语句切分，每段以 2～30 秒为宜，避免短于 1 秒的片段。建议准备 1～10 小时、至少 150 段录音，覆盖实际要合成的词汇、句式和语调。
-   **录音质量与风格**：在安静的环境中录音，选取符合目标场景的语速、情绪和停顿。例如，为有声书定制音色时，优先选择朗读录音。剔除背景音乐、他人说话声、错读和不需要的咳嗽声或长停顿。
-   **语种与转写**：选用基础模型支持的语种，按录音中的实际发音填写 `text`。中英文混读时保留实际说出的两种语言；省略未读出的符号，把风格指令单独填入 `tts_instruction`。

<a id="目录结构"></a>

<a id="training-data-structure"></a>

#### 目录结构

按以下目录结构组织训练数据：

<a id="code-block"></a>

```text
user_data/
├── data.jsonl           # 训练样本列表（必选）
├── speakers.jsonl       # 说话人配置（可选；单说话人场景可省略）
├── speaker/             # 说话人参考音频目录（使用 speakers.jsonl 时需要）
│   ├── ref_audio_1.wav
│   └── ref_audio_2.wav
└── train/               # 训练音频目录（存放所有训练用 WAV 音频）
    ├── train_001.wav
    └── train_002.wav
```

由于 Qwen-Audio-3.0-TTS-Flash 仅允许单个说话人，`speakers.jsonl` 与 `speaker/` 目录均可省略（仅保留 `data.jsonl` 与 `train/`）。如需显式提供说话人参考音频和默认语种，则按上述完整目录准备。

<a id="data-jsonl"></a>

<a id="training-data-jsonl"></a>

#### data.jsonl

必选文件，每行一条 JSON 记录，描述单条训练音频及其转写文本。

-   配合 `speakers.jsonl` 使用时，每条记录填写相同的 `speaker`：
    
    <a id="code-block-2"></a>
    
    ```jsonl
    {"wav_fn": "train/train_001.wav", "text": "这是测试文本。", "speaker": "Paimon1", "tts_instruction": "happy", "language": "chinese"}
    {"wav_fn": "train/train_002.wav", "text": "另一条测试。", "speaker": "Paimon1"}
    ```
    
-   省略 `speakers.jsonl` 使用默认说话人时，所有记录均省略 `speaker`：
    
    <a id="code-block-3"></a>
    
    ```jsonl
    {"wav_fn": "train/train_001.wav", "text": "请在提示音结束后留言。"}
    {"wav_fn": "train/train_002.wav", "text": "您的留言已保存。", "language": "chinese"}
    ```
    

| 字段 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| `wav_fn` | 是 | string | 训练音频相对于 `data.jsonl` 所在目录的路径（例如 `train/train_001.wav`）。 |
| `text` | 是 | string | 录音中实际说出的转写文本。 |
| `speaker` | 否 | string | 说话人名称。须在所有记录中统一提供（且与 `speakers.jsonl` 一致），或全部省略（视为同一个默认说话人），不可部分填写。 |
| `tts_instruction` | 否 | string | 音频对应的风格或情感指令（例如 `happy`）。 |
| `language` | 否 | string | 音频语种（例如 `chinese`、`english`），默认 `chinese`。同时配置 `speakers.jsonl` 时，以 `data.jsonl` 中的 `language` 为准。 |

<a id="speakers-jsonl"></a>

<a id="training-speakers-jsonl"></a>

#### speakers.jsonl

可选文件，仅在需要显式配置说话人参考音频时提供（单说话人场景仅写一行）：

<a id="code-block-4"></a>

```jsonl
{"speaker": "Paimon1", "ref_audios": ["speaker/ref_audio_1.wav", "speaker/ref_audio_2.wav"], "language": "chinese"}
```

| 字段 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| `speaker` | 是 | string | 说话人名称，须与 `data.jsonl` 中的 `speaker` 保持一致。 |
| `ref_audios` | 是 | array\[string\] | 参考音频路径列表，路径相对于 `data.jsonl` 所在目录（例如 `speaker/ref_audio_1.wav`）。 |
| `language` | 否 | string | 说话人默认语种，默认为 `chinese`。 |

<a id="打包与上传"></a>

<a id="training-data-packaging"></a>

#### 打包与上传

按后续创建任务时选用的数据接入方式准备文件：

-   **通过文件 API 上传**：在 `user_data/` 的上一级目录执行以下命令，使 ZIP 包内保留 `user_data/` 目录（单文件大小及配额限制见[上传文件](../../../../model-api-reference/file-management-api/upload-file-api.md)）：
    
    <a id="code-block-5"></a>
    
    ```bash
    zip -r train.zip user_data/
    ```
    
-   **通过 OSS 挂载**：将未经压缩的 `user_data/` 目录上传至 OSS Bucket。首次挂载时，在百炼控制台的**模型调优**页面单击**创建训练任务**，在**数据配置**中选择**数据集挂载**并按提示完成授权。授权后，确认可以看到目标 Bucket 中的文件。
    

> **说明**
>
> 目前仅支持挂载华北6（乌兰察布）的 OSS Bucket。如需挂载其他地域的 Bucket，请联系商务经理。

<a id="评测数据"></a>

<a id="evaluation-data"></a>

### 评测数据

平台默认运行内置评测。通过 OSS 挂载创建训练任务时，可在 `evaluation_datasets` 中指定自定义评测集。训练日志会分别列出内置评测集和自定义评测集的指标。

将评测样本写入 `eval_data/data.jsonl`，每行一个 JSON 对象。`text` 填写待合成的文本，`language` 填写文本语种。以下是两条中文样本。

<a id="code-block-6"></a>

```jsonl
{"text": "您的包裹已送达，请在前台领取。", "language": "chinese"}
{"text": "今天下午三点，我们一起去图书馆。", "language": "chinese"}
```

评测集最多包含 100 条样本，每条文本超过 500 字符的部分会被截断。将该文件上传至 OSS，并将对象路径填入 `evaluation_datasets` 的 `mount_storage.file_path`。

<a id="创建任务"></a>

<a id="create-job"></a>

## 创建任务

根据数据体积和是否需要自定义评测集，选择以下任一方式创建调优任务：

-   **方式一（文件 API 上传）**：上传训练集 ZIP 包后传入 `training_file_ids`，适合中小规模训练集。
-   **方式二（OSS 挂载）**：直接挂载 OSS 中未经压缩的数据集目录，适合大体积训练集或需要配置自定义评测集（`evaluation_datasets`）的场景。

<a id="sec-tabs"></a>

<a id="方式一-文件-api-上传"></a>

<a id="方式一-文件-api-上传-h4"></a>

#### 方式一：文件 API 上传

1.  调用[上传文件](../../../../model-api-reference/file-management-api/upload-file-api.md)接口上传 `train.zip`，从响应的 `data.uploaded_files[0].file_id` 复制文件 ID：
    
    <a id="code-block-7"></a>
    
    ```bash
    curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
      --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
      --form 'files=@"train.zip"' \
      --form 'purpose="fine-tune"' \
      --form 'descriptions="Qwen-Audio 3.0 TTS fine-tune dataset"'
    ```
    
2.  将下方 `<YOUR_FILE_ID>` 替换为上一步返回的文件 ID，调用创建调优任务接口：
    
    <a id="code-block-8"></a>
    
    ```bash
    curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
      --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
      --header "Content-Type: application/json" \
      --data '{
        "model": "qwen-audio-3.0-tts-flash",
        "training_type": "sft",
        "training_file_ids": [
          "<YOUR_FILE_ID>"
        ],
        "hyper_parameters": {}
      }'
    ```
    

<a id="方式二-oss-挂载"></a>

<a id="方式二-oss-挂载-h4"></a>

#### 方式二：OSS 挂载

确保已完成控制台**数据集挂载**授权，并将未经压缩的训练集目录（及可选评测集目录）上传至 OSS Bucket。将下方占位符替换为实际的 Bucket 名称与 `data.jsonl` 路径；如无需自定义评测集，可省略 `evaluation_datasets` 字段。

<a id="code-block-9"></a>

```bash
curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen-audio-3.0-tts-flash",
    "training_type": "sft",
    "training_file_ids": [],
    "training_datasets": [
      {
        "data_source_type": "oss_mount",
        "mount_storage": {
          "region": "cn-wulanchabu",
          "bucket": "<YOUR_BUCKET_NAME>",
          "file_path": "user_data/data.jsonl"
        }
      }
    ],
    "evaluation_datasets": [
      {
        "data_source_type": "oss_mount",
        "mount_storage": {
          "region": "cn-wulanchabu",
          "bucket": "<YOUR_BUCKET_NAME>",
          "file_path": "eval_data/data.jsonl"
        }
      }
    ],
    "hyper_parameters": {"lm_epoch": 6}
  }'
```

任务创建成功后，请保存响应中的 `output.job_id`（任务 ID）与 `output.finetuned_output`（调优后的模型 ID）。

<a id="请求参数"></a>

<a id="request-parameters"></a>

### 请求参数

| 参数 | 必选 | 说明 |
| --- | --- | --- |
| `model` | 是 | 基础模型 ID，固定填写 qwen-audio-3.0-tts-flash。 |
| `training_type` | 是 | 训练方式，填写 `sft`。 |
| `training_file_ids` | 条件必选 | 适用于方式一。通过文件 API 上传获得的训练文件 ID 列表，仅支持传入 1 个文件 ID。使用方式二时传入空数组 `[]` 或省略。 |
| `training_datasets` | 条件必选 | 适用于方式二。OSS 挂载训练集列表，仅支持挂载 1 个训练文件路径。`data_source_type` 固定为 `oss_mount`；`mount_storage` 填写 Bucket 所属地域（`region`）、Bucket 名称（`bucket`）及 `data.jsonl` 的对象路径（`file_path`）。 |
| `evaluation_datasets` | 否 | 仅适用于方式二。OSS 挂载评测集列表，结构与 `training_datasets` 相同，仅支持挂载 1 个评测文件路径。 |
| `hyper_parameters` | 是 | 超参数配置对象。`lm_epoch` 指定语言模型的训练轮数，可填 5 到 15 的整数（含两端），默认值为 5。传 `{}` 使用默认值。`fm_epoch` 固定为 50，暂不支持修改。 |

<a id="查看结果"></a>

<a id="monitor-job"></a>

## 查看结果

<a id="任务状态"></a>

<a id="query-status"></a>

### 任务状态

将 `<YOUR_JOB_ID>` 替换为创建任务时返回的 `output.job_id`，查询任务当前状态：

<a id="code-block-10"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<YOUR_JOB_ID>" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

-   `output.status` 反映任务阶段：`PENDING`（待开始）→ `QUEUING`（排队中）→ `RUNNING`（训练中）→ `SUCCEEDED`（训练成功）；异常终止状态为 `FAILED` 或 `CANCELED`。完整响应字段说明请参见[查询调优任务状态](../../../../model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md#faa99e295ckyg)。
-   当 `output.status` 为 `SUCCEEDED` 时，`output.finetuned_output` 即为调优后的模型 ID，`output.usage` 为本次训练消耗的 Token 数。
-   可调用[查询 Checkpoint 列表](../../../../model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)（`GET /api/v1/fine-tunes/{job_id}/checkpoints`）查看训练产出的检查点信息。

<a id="日志与指标"></a>

<a id="query-logs"></a>

### 日志与指标

可通过日志接口查看训练进度、自动评测指标以及失败原因：

<a id="code-block-11"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<YOUR_JOB_ID>/logs?offset=0&line=100" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

通过 `offset` 与 `line` 分页拉取日志，完整接口说明请参见[查询调优任务日志](../../../../model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md#e76df8eaa2vbs)。训练完成后，日志中会输出以下评测指标：

| 评测指标 | 说明 |
| --- | --- |
| **WER**（词/字错误率） | 使用语音识别模型将合成音频转写并与参考文本比对计算，数值越低表示发音准确度越高。 |
| **Speaker similarity**（说话人相似度） | 计算目标说话人音频向量与合成音频向量（Audio Embedding）之间的相似度，数值越接近 1 表示音色还原度越高。 |
| **MOS**（语音自然度评分） | 基于语音质量评测模型（P.808 MOS）对合成音频的听感自然度打分，分值越高表示音质与自然度越好。 |

<a id="模型部署"></a>

<a id="deploy-model"></a>

## 模型部署

Qwen-Audio-3.0-TTS-Flash 调优后部署请联系商务经理。

<a id="计费说明"></a>

<a id="billing"></a>

## 计费说明

Qwen-Audio-3.0-TTS-Flash 的训练单价为 **0.1 元 / 千 Tokens**。创建任务的接口不返回预估费用。可在提交前按训练录音的总时长和训练轮数估算。

-   预计训练 Token 数 = (`lm_epoch` + `fm_epoch`) × 25 × 训练录音总时长（秒）
-   预计训练费用（元）= 预计训练 Token 数 ÷ 1,000 × 0.1

例如，使用 1 小时（3,600 秒）的训练录音，`lm_epoch` 取默认值 5，`fm_epoch` 固定为 50，预计消耗 (5 + 50) × 25 × 3,600 = 4,950,000 Tokens，训练费用约为 **495 元**。

任务完成后，可在 `output.usage` 查看实际消耗的 Token 数，最终费用以账单为准。

<a id="常见问题"></a>

<a id="faq"></a>

## 常见问题

<a id="accordion-创建任务报错-403-accessdenied-feature-unavailable"></a>

创建任务报错 403 AccessDenied（Feature unavailable）

当前账号或业务空间未开通 Qwen-Audio-3.0-TTS-Flash 调优邀测权限。请联系商务经理申请开通，并确认所使用的 API Key 属于已开通权限的账号。

<a id="accordion-创建任务报错-400-invalidparameter-unsupported-model"></a>

创建任务报错 400 InvalidParameter（unsupported model）

请检查请求中的模型 ID 和训练方式。`model` 填写 `qwen-audio-3.0-tts-flash`，`training_type` 填写 `sft`。

<a id="accordion-训练任务失败-日志出现-speaker-audio-duration-below-0-5h"></a>

训练任务失败，日志出现 speaker\_audio\_duration\_below\_0\_5h

同一说话人的 WAV 训练录音累计总时长不足 0.5 小时（30 分钟）。请补充同一说话人的录音使总时长超过 30 分钟，重新打包上传（或更新 OSS 目录）后创建新任务。
