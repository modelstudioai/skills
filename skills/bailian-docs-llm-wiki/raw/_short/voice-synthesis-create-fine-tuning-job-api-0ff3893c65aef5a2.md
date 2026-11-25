# 语音合成（CosyVoice）-创建调优任务

创建一个语音合成的模型调优训练任务。数据集支持通过API上传数据集或OSS挂载。

<a id="适用范围"></a>

<a id="voc-prereq-title"></a>

<a id="voc-prereq-section"></a>

## 适用范围

-   **适用地域**：本文描述的功能**仅在华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   **开通账号权限**：若使用[阿里云子账号](../model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](../model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](../model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](../model-api-reference/preparations/get-api-key.md)。
-   **准备工作**：已阅读[CosyVoice模型调优](fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)，了解支持调优的模型、调优步骤、数据格式以及计费说明。

<a id="创建调优任务"></a>

<a id="voc-api-title"></a>

<a id="voc-api-section"></a>

## 创建调优任务

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

<table><tbody><tr><td><a id="voc-req-header-h4"></a><a id="voc-req-section"></a><h3>请求参数</h3><a id="voc-req-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定值：<code>application/json</code></p><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key鉴权，格式为<code>Bearer sk-xxxx</code>。</p><a id="voc-req-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>指定调优所用的基准模型。当前仅支持：</p><ul><li><code>cosyvoice-v3-flash</code></li></ul><p><strong>training_type</strong> <code>string</code> <strong>（必选）</strong></p><p>微调类型，当前仅支持<code>efficient_sft</code>（高效微调）。</p><p><strong>hyper_parameters</strong> <code>object</code> <strong>（必选）</strong></p><p><strong>超参数配置</strong>。CosyVoice 调优涉及两个子网络，两者已解耦、可独立调整：</p><ul><li>LM（Language Model）：将文本转为离散语音 token 的自回归语言模型，对韵律影响较大。超参以 <code>lm_*</code> 前缀区分。</li><li>FM（Flow Matching）：将语音 token 还原为 Mel 谱的流匹配模型，对音色还原度影响较大。超参以 <code>fm_*</code> 前缀区分。</li></ul><a id="accordion-超参数属性"></a><section><p>超参数属性</p><div><p><strong>lm_max_epoch</strong> <code>int</code> <strong>（必选）</strong></p><p>LM 调优轮次（epoch 数）。推荐值：60。取值范围：[1, 2147483647]。</p><p><strong>lm_step</strong> <code>int</code> <strong>（必选）</strong></p><p>LM 保存 checkpoint 的步长（每多少个 epoch 保存一次）。推荐值：5。取值范围：[1, 2147483647]。</p><p><strong>lm_num</strong> <code>int</code> <strong>（必选）</strong></p><p>LM 保留的 checkpoint 数量上限。推荐值：3。取值范围：[1, 2147483647]。</p><p><strong>lm_batch_size</strong> <code>int</code> <strong>（必选）</strong></p><p>LM 批次大小（batch size）。推荐值：1000。取值范围：[1, 2147483647]。</p><p><strong>fm_max_epoch</strong> <code>int</code> <strong>（必选）</strong></p><p>FM 调优轮次（epoch 数）。推荐值：100。取值范围：[1, 2147483647]。</p><p><strong>fm_step</strong> <code>int</code> <strong>（必选）</strong></p><p>FM 保存 checkpoint 的步长（每多少个 epoch 保存一次）。推荐值：10。取值范围：[1, 2147483647]。</p><p><strong>fm_num</strong> <code>int</code> <strong>（必选）</strong></p><p>FM 保留的 checkpoint 数量上限。推荐值：3。取值范围：[1, 2147483647]。</p><p><strong>fm_batch_size</strong> <code>int</code> <strong>（必选）</strong></p><p>FM 批次大小（batch size）。推荐值：2000。取值范围：[1, 2147483647]。</p></div></section><p><strong>training_datasets</strong> <code>Array of Dataset</code> <strong>（条件必选）</strong></p><p>训练集文件列表。与 <code>training_file_ids</code> 二选一，若使用 <code>training_file_ids</code> 则无需传此参数。仅支持挂载一个训练文件。</p><a id="accordion-dataset-结构"></a><section><p>Dataset 结构</p><div><p><strong>data_source_type</strong> <code>string</code> <strong>（必选）</strong></p><p>数据源类型，可选值：</p><ul><li><code>oss_mount</code>（挂载 OSS 文件）</li><li><code>file_id</code>（由文件管理服务 API 上传的文件）</li></ul><p><strong>mount_storage</strong> <code>object</code> （条件必选）</p><p>数据源类型为 <code>oss_mount</code> 时必填。OSS 挂载信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>region</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS Bucket 所属地域。支持北京（cn-beijing）和新加坡（ap-southeast-1）。</p><p><strong>bucket</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS Bucket 名称。</p><p><strong>file_path</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS 文件路径（object key）。对包含多个文件的数据集，使用其 data.jsonl 的文件路径。与使用 file_id 的方式不同，需要将未经压缩的数据集文件夹整体上传到 OSS，不支持 zip 文件。</p></div></section><p><strong>file_id</strong> <code>string</code> （条件必选）</p><p>数据源类型为 <code>file_id</code> 时必填。文件 ID，由<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 产生。</p></div></section><p><strong>validation_datasets</strong> <code>Array of Dataset</code> （可选）</p><p>验证集文件列表。结构同<code>training_datasets</code>。</p><p>与 <code>validation_file_ids</code> 二选一。若两者均不提供，系统会从训练集中自动划分。</p><p><strong>training_file_ids</strong> <code>array[string]</code> <strong>（条件必选）</strong></p><p>训练集文件ID数组，可传入多个ID。与 <code>training_datasets</code> 二选一，若使用 <code>training_datasets</code> 则无需传此参数。文件ID通过<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 获取。</p><p><strong>validation_file_ids</strong> <code>array[string]</code> （可选）</p><p>验证集文件ID数组，可传入多个ID。与 <code>validation_datasets</code> 二选一，若使用 <code>validation_datasets</code> 则无需传此参数。若两者均不提供，系统会从训练集中自动划分。文件ID通过<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 获取。</p><p><strong>job_name</strong> <code>string</code> （可选）</p><p>调优任务名称。</p><p><strong>model_name</strong> <code>string</code> （可选）</p><p>调优完成后的模型名称。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-使用file-id的数据集-tab"></a>使用file_id的数据集<div><a id="code-code-group-使用file-id的数据集"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;cosyvoice-v3-flash&quot;,
    &quot;training_datasets&quot;: [
        {
            &quot;data_source_type&quot;: &quot;file_id&quot;,
            &quot;file_id&quot;: &quot;&lt;替换为训练数据集的file_id&gt;&quot;
        }
    ],
    &quot;hyper_parameters&quot;: {
        &quot;lm_max_epoch&quot;: 60,
        &quot;lm_step&quot;: 5,
        &quot;lm_num&quot;: 3,
        &quot;lm_batch_size&quot;: 1000,
        &quot;fm_max_epoch&quot;: 100,
        &quot;fm_step&quot;: 10,
        &quot;fm_num&quot;: 3,
        &quot;fm_batch_size&quot;: 2000
    },
    &quot;training_type&quot;: &quot;efficient_sft&quot;
}'
</code></pre></div><a id="fig-code-group-使用oss挂载的数据集-tab"></a>使用OSS挂载的数据集<div><a id="code-code-group-使用oss挂载的数据集"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;cosyvoice-v3-flash&quot;,
    &quot;training_datasets&quot;: [
        {
            &quot;data_source_type&quot;: &quot;oss_mount&quot;,
            &quot;mount_storage&quot;: {
                &quot;region&quot;: &quot;cn-beijing&quot;,
                &quot;bucket&quot;: &quot;example_bucket&quot;,
                &quot;file_path&quot;: &quot;dataset/data.jsonl&quot;
            }
        }
    ],
    &quot;hyper_parameters&quot;: {
        &quot;lm_max_epoch&quot;: 60,
        &quot;lm_step&quot;: 5,
        &quot;lm_num&quot;: 3,
        &quot;lm_batch_size&quot;: 1000,
        &quot;fm_max_epoch&quot;: 100,
        &quot;fm_step&quot;: 10,
        &quot;fm_num&quot;: 3,
        &quot;fm_batch_size&quot;: 2000
    },
    &quot;training_type&quot;: &quot;efficient_sft&quot;
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="voc-resp-header-h4"></a><a id="voc-resp-section"></a><h3>响应参数</h3><p><strong>request_id</strong> <code>string</code></p><p>请求的唯一标识符。</p><p><strong>output</strong> <code>object</code></p><p>任务详情。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>job_id</strong> <code>string</code></p><p>模型调优任务唯一标识，用于查询任务详情、日志、取消或删除任务。生成规则：<code>ft-{yyyyMMddHHmm}-{4位uuid}</code>。</p><p><strong>job_name</strong> <code>string</code></p><p>模型调优任务名称。</p><p><strong>model_name</strong> <code>string</code></p><p>调优完成后的模型名称。</p><p><strong>status</strong> <code>string</code></p><p>调优训练任务的状态：</p><ul><li><code>PENDING</code>：训练待开始。</li><li><code>QUEUING</code>：训练正在排队（同一时间只能运行一个调优任务）。</li><li><code>RUNNING</code>：训练正在进行中。</li><li><code>SUCCEEDED</code>：训练成功。</li><li><code>FAILED</code>：训练失败。</li><li><code>CANCELED</code>：训练已取消。</li><li><code>CANCELING</code>：训练正在取消中。</li></ul><p><strong>finetuned_output</strong> <code>string</code></p><p>调优后产出的新模型ID，部署和调用时需要用到。任务状态为 SUCCEEDED 时返回。</p><p><strong>model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>base_model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>training_file_ids</strong> <code>array</code></p><p>兼容旧版字段，新任务始终返回空数组，请使用 <code>training_datasets</code>。</p><p><strong>training_datasets</strong> <code>Array of Dataset</code></p><p>训练数据集列表。</p><p><strong>validation_file_ids</strong> <code>array</code></p><p>兼容旧版字段，新任务始终返回空数组，请使用 <code>validation_datasets</code>。</p><p><strong>validation_datasets</strong> <code>Array of Dataset</code></p><p>验证数据集列表。若未指定验证集，为空数组。</p><p><strong>hyper_parameters</strong> <code>object</code></p><p>实际使用的超参数。</p><p><strong>training_type</strong> <code>string</code></p><p>模型调优的训练方式。</p><p><strong>output_cnt</strong> <code>integer</code></p><p>当前任务已产出的 Checkpoint 数量。Checkpoint 详细列表可通过<a href="../model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md">Checkpoint 管理</a>接口获取。</p><p><strong>max_output_cnt</strong> <code>integer</code></p><p>单次任务可产出的 Checkpoint 数量上限。<code>output_cnt</code> 超出上限的部分会按调优充分度截断。</p><p><strong>charge_type</strong> <code>string</code></p><p>计费类型。CosyVoice 模型为 token。</p><p><strong>create_time</strong> <code>string</code></p><p>任务创建时间。</p><p><strong>end_time</strong> <code>string</code></p><p>任务结束时间。任务状态为 SUCCEEDED、FAILED 或 CANCELED 时返回。</p><p><strong>usage</strong> <code>integer</code></p><p>调优任务消耗的 Token 数。任务状态为 SUCCEEDED 或 CANCELED 时返回。</p><p><strong>workspace_id</strong> <code>string</code></p><p>阿里云百炼API Key所属的业务空间ID。请参见<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md">获取Workspace ID</a>。</p><p><strong>user_identity</strong> <code>string</code></p><p>用户标识，阿里云账号ID。</p><p><strong>creator</strong> <code>string</code></p><p>创建人的阿里云账号ID。</p><p><strong>modifier</strong> <code>string</code></p><p>修改人的阿里云账号ID。</p><p><strong>group</strong> <code>string</code></p><p>模型调优任务分组。</p></div></section><p><strong>code</strong> <code>string</code></p><p>错误码。调用失败时返回。请参见下方错误码表。</p><p><strong>message</strong> <code>string</code></p><p>错误详情描述。调用失败时返回。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应示例"></a><section><a id="成功响应示例-h4"></a><h4>成功响应示例</h4><p>重点关注：<code>output.job_id</code>（任务ID）、<code>output.finetuned_output</code>（调优后产出的新模型名称）。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;0eb05b0c-02ba-414a-9d0c-xxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;job_id&quot;: &quot;ft-202511111122-xxxx&quot;,
        &quot;job_name&quot;: &quot;ft-202511111122-xxxx&quot;,
        &quot;status&quot;: &quot;PENDING&quot;,
        &quot;finetuned_output&quot;: &quot;cosyvoice-v3-flash-ft-202511111122-xxxx&quot;,
        &quot;model&quot;: &quot;cosyvoice-v3-flash&quot;,
        &quot;base_model&quot;: &quot;cosyvoice-v3-flash&quot;,
        &quot;training_file_ids&quot;: [],
        &quot;training_datasets&quot;: [
            {
                &quot;data_source_type&quot;: &quot;file_id&quot;,
                &quot;file_id&quot;: &quot;xxxxxxxxxxxx&quot;
            }
        ],
        &quot;validation_file_ids&quot;: [],
        &quot;validation_datasets&quot;: [],
        &quot;hyper_parameters&quot;: {
            &quot;lm_max_epoch&quot;: 60,
            &quot;lm_step&quot;: 5,
            &quot;lm_num&quot;: 3,
            &quot;lm_batch_size&quot;: 1000,
            &quot;fm_max_epoch&quot;: 100,
            &quot;fm_step&quot;: 10,
            &quot;fm_num&quot;: 3,
            &quot;fm_batch_size&quot;: 2000
        },
        &quot;training_type&quot;: &quot;efficient_sft&quot;,
        &quot;model_name&quot;: &quot;ft-202511111122-xxxx&quot;,
        &quot;output_cnt&quot;: 0,
        &quot;max_output_cnt&quot;: 10,
        &quot;charge_type&quot;: &quot;token&quot;,
        &quot;create_time&quot;: &quot;2025-11-11 11:22:22&quot;
    }
}
</code></pre></section><a id="错误响应示例"></a><section><a id="错误响应示例-h4"></a><h4>错误响应示例</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;request_id&quot;: &quot;BE213CDD-8A5C-59EE-9A67-055EAB0CB59B&quot;,
    &quot;message&quot;: &quot;The model cosyvoice-v3-flash does not support training_type: full_sft&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="voc-err-h2"></a>

<a id="voc-err-section"></a>

## 错误码

如果调用失败并返回报错信息，请参见下表进行排查。

| HTTP 状态码 | 错误码 | 解决方案 |
| --- | --- | --- |
| 400 | InvalidParameter | 参数错误，缺少参数或者参数格式问题等。根据错误信息修正您的参数。 |
| 400 | UnsupportedOperation | 当资源处于特定状态时，无法对其进行操作。待要操作的资源到达可操作状态时再进行操作。 |
| 404 | NotFound | 要查询/操作的资源不存在。检查资源ID是否错误。 |
| 409 | Conflict | 已存在同名部署实例，需要指定后缀进行区分。 |
| 429 | Throttling | 资源的创建触发平台限制。删除不再使用的模型。如您确实需要提高调优任务的并发量或保留更多调优成功的模型，请联系商务经理。 |
| 500 | InternalError | 内部错误。记录 request\_id，通过工单联系阿里云工程师进行排查。 |

<a id="下一步"></a>

<a id="voc-ft-next-h2"></a>

<a id="voc-ft-next"></a>

## 下一步

调优为异步操作，调用本接口后可通过[查询和管理调优任务](../model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)接口查询调优任务状态。
