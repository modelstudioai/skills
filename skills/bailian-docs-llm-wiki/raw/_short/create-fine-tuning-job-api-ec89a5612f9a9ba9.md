# 文本生成-创建调优任务

创建一个文本生成的模型微调训练任务。数据集支持通过API上传数据集或OSS挂载。

<a id="适用范围"></a>

<a id="txt-prereq-title"></a>

## 适用范围

-   **适用地域**：本文描述的功能**仅在华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   **开通账号权限**：若使用[阿里云子账号](../model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace)。
-   **配置环境变量**：已成功[获取 API Key](../model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   **准备工作**：已阅读[千问模型调优](../model-user-guide/fine-tuning/fine-tune-text-generation-model.md)，了解支持微调的模型、微调步骤、数据格式以及计费说明。
-   **RL/OPD 训练**：本接口适用于 SFT/CPT/DPO 微调。强化学习（RL）与 OPD 蒸馏训练通过 DashScope SDK/CLI 提交（`dashscope rl run` 或 `AgenticRL().run()`），非 REST API，详见 [强化学习训练配置](../model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md) 与 [OPD 蒸馏训练配置](../model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

<a id="创建微调任务"></a>

<a id="2a2f41392afai"></a>

## 创建微调任务

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

<table><tbody><tr><td><a id="txt-req-header-h4"></a><h3>请求参数</h3><a id="txt-req-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定值：<code>application/json</code></p><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key鉴权，格式为<code>Bearer sk-xxxx</code>。</p><a id="txt-req-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>用于调优的<a href="../model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md">基础模型ID</a>或其他调优任务产出的模型ID（对已经调优了的模型进行再次调优）。</p><p><strong>training_type</strong> <code>string</code> （可选）</p><p>调优方法，可选值：</p><ul><li><code>cpt</code></li><li><code>sft</code></li><li><code>efficient_sft</code></li><li><code>dpo_full</code></li><li><code>dpo_lora</code></li></ul><p><strong>hyper_parameters</strong> <code>object</code> （可选）</p><p><strong>超参数设置</strong>。不同模型支持的参数集合及其默认值不同，请前往<a href="https://bailian.console.aliyun.com/model/tuning/create">控制台</a>选择相同的模型和调优方式查看实际默认值。其中 <code>n_epochs</code>、<code>batch_size</code>、<code>max_length</code> 影响调优费用，<strong>必须填写</strong>。</p><a id="accordion-超参数属性"></a><section><p>超参数属性</p><div><p><strong>n_epochs</strong> <code>int</code> <strong>（必选）</strong></p><p>训练循环次数。模型遍历训练的次数，请根据模型调优实际使用经验进行调整。</p><ul><li>数据量 &lt; 10,000：推荐 3~5 次。</li><li>数据量 &gt; 10,000：推荐 1~2 次。</li></ul><div><div><p><strong>重要</strong>该参数影响<a href="../model-user-guide/test-1/model-training-and-deployment-billing.md">训练计费</a>，循环次数越多，训练时间越长，费用越高。</p></div></div><p><strong>batch_size</strong> <code>int</code> <strong>（必选）</strong></p><p>批次大小。一次性送入模型进行训练的数据条数，参数过小会显著延长训练时间。不同模型的默认值不同，请前往控制台查看。</p><p><strong>max_length</strong> <code>int</code> <strong>（必选）</strong></p><p>序列长度。推荐值：8192。单条训练数据 token 支持的最大长度。如果单条数据 token 长度超过设定值，调优会直接丢弃该条数据，不进行训练。</p><p>字符与 token 之间的关系请参考<a href="https://help.aliyun.com/zh/model-studio/billing-for-model-studio">Token和字符串之间怎么换算</a>。</p><p><strong>learning_rate</strong> <code>float</code> （可选）</p><p>学习率。推荐使用百炼默认值。控制模型修正权重的强度。</p><ul><li>学习率过高，模型参数会剧烈变化，可能导致模型表现变差。</li><li>学习率过低，模型表现不会有太大变化。</li></ul><p><strong>lr_scheduler_type</strong> <code>string</code> （可选）</p><p>学习率调整策略。推荐 <code>linear</code> 或 <code>inverse_sqrt</code>。在模型训练中动态调整学习率的策略。各策略详情请参考<a href="../model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md">学习率调整策略说明</a>。</p><p><strong>split</strong> <code>float</code> （可选）</p><p>训练集在训练文件中的占比。推荐使用百炼默认值。</p><p>未设置 <code>validation_datasets</code> 时，百炼会自动把训练文件中的 80% 作为训练集、20% 作为验证集。设置了 <code>validation_datasets</code> 时该参数无效。</p><p><strong>max_split_val_dataset_sample</strong> <code>int</code> （可选）</p><p>验证集数据最大数量。推荐使用百炼默认值。</p><p>未设置 <code>validation_datasets</code> 时，自动分割的验证集最多 1000 条。设置了 <code>validation_datasets</code> 时该参数无效。</p><p><strong>eval_steps</strong> <code>int</code> （可选）</p><p>验证步数。训练阶段针对模型的验证间隔步长，用于阶段性评估模型训练准确率、训练损失。</p><p>该参数影响模型调优进行时的 Validation Loss 和 Validation Token Accuracy 的显示频率。</p><p><strong>logging_steps</strong> <code>int</code> （可选）</p><p>日志显示步数。调优日志打印的间隔步数。</p><p><strong>warmup_ratio</strong> <code>float</code> （可选）</p><p>学习率预热比例。推荐使用百炼默认值。学习率预热占用总的训练过程的比例。学习率预热是指学习率在训练开始后由一个较小值线性递增至学习率设定值，帮助模型更稳定地训练。</p><ul><li>比例过大：效果与过低的学习率相同，会导致调优后的模型表现不会有太大变化。</li><li>比例过小：效果与过高的学习率相同，可能导致调优后的模型表现不一定更好，甚至变差。</li></ul><blockquote><p>该参数仅对学习率调整策略 <code>Constant</code> 无效。</p></blockquote><p><strong>weight_decay</strong> <code>float</code> （可选）</p><p>权重衰减（L2 正则化强度）。推荐使用百炼默认值。能在一定程度上保持模型的通用能力，数值过大会导致调优效果不明显。</p><p><strong>freeze_vit</strong> <code>boolean</code> （可选）</p><p>是否冻结视觉主干网络。用于冻结视觉主干网络的参数，使其在训练过程中不更新权重。仅适用于千问-VL（视觉理解）模型。</p><blockquote><p>只有 <code>freeze_vit</code> 设置为 <code>true</code> 时，模型才能进行按 Token 用量计费。</p></blockquote><p><strong>lora_rank</strong> <code>int</code> （可选）</p><p>LoRA 秩值。推荐值：64。LoRA 训练中的低秩矩阵的秩大小。秩越大调优效果越好，但训练会略慢。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>dpo_lora</code> 时生效。</p><blockquote><p>当对一个已经高效微调后的模型进行二次高效微调时，<code>lora_rank</code>、<code>lora_alpha</code>、<code>lora_dropout</code> 三个参数必须保持一致。</p></blockquote><p><strong>lora_alpha</strong> <code>int</code> （可选）</p><p>LoRA 缩放系数。推荐使用百炼默认值。用于控制原模型权重与 LoRA 的低秩修正项之间的结合缩放系数。</p><ul><li>较大的 Alpha 值会给予 LoRA 修正项更多权重，使得模型更加依赖于微调任务的特定信息。</li><li>较小的 Alpha 值则会让模型更倾向于保留原始预训练模型的知识。</li></ul><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>dpo_lora</code> 时生效。</p><p><strong>lora_dropout</strong> <code>float</code> （可选）</p><p>LoRA 丢弃率。推荐使用百炼默认值。LoRA 训练中的低秩矩阵值的丢弃率。使用推荐数值能增强模型通用化能力，数值过大会导致模型微调效果不明显。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>dpo_lora</code> 时生效。</p><p><strong>data_augmentation</strong> <code>boolean</code> （可选）</p><p>是否开启混合训练。开启后训练数据将与百炼提供的通用数据集混合，提升训练效果，避免模型能力退化。混合数据计入总训练 Token，按标准计费。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>sft</code> 时生效。</p><p><strong>augmentation_types</strong> <code>string</code> （可选）</p><p>预置数据类型。开启混合训练时，选择预置数据类型，多个类型以逗号分隔。需与 <code>augmentation_ratio</code> 配合使用。示例：<code>&quot;dialogue_cn,general_purpose_cn,nlp&quot;</code>。</p><p>可选值：</p><table><tbody><tr><td><p>取值</p></td><td><p>数据集名称</p></td><td><p>适用模型</p></td></tr><tr><td><p><code>dialogue_cn</code></p></td><td><p>中文-对话</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>math_cn</code></p></td><td><p>中文-数学</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>general_coding_cn</code></p></td><td><p>中文-代码</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>general_purpose_cn</code></p></td><td><p>中文-通用</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>nlp</code></p></td><td><p>NLP 理解</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>dialogue_en</code></p></td><td><p>英文-对话</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>math_en</code></p></td><td><p>英文-数学</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>general_coding_en</code></p></td><td><p>英文-代码</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>general_purpose_en</code></p></td><td><p>英文-通用</p></td><td><p>千问 2 系列</p></td></tr><tr><td><p><code>mix_v2</code></p></td><td><p>通用-V2</p></td><td><p>千问 3 系列</p></td></tr><tr><td><p><code>vl_mix</code></p></td><td><p>通用</p></td><td><p>千问 3 VL 系列</p></td></tr></tbody></table><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>sft</code> 时生效。</p><p><strong>augmentation_ratio</strong> <code>string</code> （可选）</p><p>混合倍率。需与 <code>augmentation_types</code> 完全对应，按训练数据量的比例随机抽取混合。取值范围：0.0~2.0。示例：<code>&quot;0.1,0.05,0.15&quot;</code>。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>sft</code> 时生效。</p><p><strong>save_strategy</strong> <code>string</code> （可选）</p><p>快照存储策略。可设置为 <code>epoch</code> 或 <code>steps</code>。设置为 <code>steps</code> 时，可通过 <code>save_steps</code> 参数调整保存间隔。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>sft</code> 时生效。</p><p><strong>save_steps</strong> <code>int</code> （可选）</p><p>存储步数。设置每训练多少步保存一次模型参数快照（Checkpoint）。建议设置为 <code>eval_steps</code> 的整数倍。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>sft</code> 时生效。</p><p><strong>save_total_limit</strong> <code>int</code> （可选）</p><p>快照存储数量上限。推荐值：10。限制最多保存多少个模型参数快照（Checkpoint）用于发布。</p><p>仅在 <code>training_type</code> 为 <code>efficient_sft</code> 或 <code>sft</code> 时生效。</p></div></section><p><strong>training_datasets</strong> <code>Array of Dataset</code> <strong>（必选）</strong></p><p>训练集文件列表。</p><a id="accordion-dataset-结构"></a><section><p>Dataset 结构</p><div><p><strong>data_source_type</strong> <code>string</code> <strong>（必选）</strong></p><p>数据源类型，可选值：</p><ul><li><code>oss_mount</code>（挂载 OSS 文件）</li><li><code>file_id</code>（由文件管理服务 API 上传的文件）</li></ul><p><strong>mount_storage</strong> <code>object</code> （条件必选）</p><p>数据源类型为 <code>oss_mount</code> 时必填。OSS 挂载信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>region</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS Bucket 所属地域。支持北京（cn-beijing）和新加坡（ap-southeast-1）。</p><p><strong>bucket</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS Bucket 名称。</p><p><strong>file_path</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS 文件路径（object key）。对包含多个文件的数据集，使用其 data.jsonl 的文件路径。与使用 file_id 的方式不同，需要将未经压缩的数据集文件夹整体上传到 OSS，不支持 zip 文件。</p></div></section><p><strong>file_id</strong> <code>string</code> （条件必选）</p><p>数据源类型为 <code>file_id</code> 时必填。文件 ID，由<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 产生。</p></div></section><p><strong>validation_datasets</strong> <code>Array of Dataset</code> （可选）</p><p>测试集文件列表。结构同<code>training_datasets</code>。</p><p><strong>job_name</strong> <code>string</code> （可选）</p><p>调优任务名称。</p><p><strong>model_name</strong> <code>string</code> （可选）</p><p>调优完成后的模型名称。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-使用-file-id-数据集-tab"></a>使用 file_id 数据集<div><a id="code-code-group-使用-file-id-数据集"></a><pre class="language-bash"><code>curl --location --request POST &quot;https://dashscope.aliyuncs.com/api/v1/fine-tunes&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;:&quot;qwen3-14b&quot;,
    &quot;training_datasets&quot;:[
        {
            &quot;data_source_type&quot;:&quot;file_id&quot;,
            &quot;file_id&quot;:&quot;&lt;替换为训练数据集的文件id&gt;&quot;
        }
    ],
    &quot;validation_datasets&quot;:[
        {
            &quot;data_source_type&quot;:&quot;file_id&quot;,
            &quot;file_id&quot;:&quot;&lt;替换为验证数据集的文件id&gt;&quot;
        }
    ],
    &quot;hyper_parameters&quot;:{
        &quot;n_epochs&quot;:1,
        &quot;learning_rate&quot;:&quot;1.6e-5&quot;,
        &quot;batch_size&quot;:32,
        &quot;max_length&quot;:8192,
        &quot;split&quot;:0.8
    },
    &quot;training_type&quot;:&quot;sft&quot;,
    &quot;finetuned_output_suffix&quot;:&quot;suffix&quot;
}'
</code></pre></div><a id="fig-code-group-使用-oss-挂载数据集-tab"></a>使用 OSS 挂载数据集<div><a id="code-code-group-使用-oss-挂载数据集"></a><pre class="language-bash"><code>curl --location --request POST &quot;https://dashscope.aliyuncs.com/api/v1/fine-tunes&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;:&quot;qwen3-14b&quot;,
    &quot;training_datasets&quot;:[
        {
            &quot;data_source_type&quot;:&quot;oss_mount&quot;,
            &quot;mount_storage&quot;:{
                &quot;region&quot;:&quot;cn-beijing&quot;,
                &quot;bucket&quot;:&quot;example_bucket&quot;,
                &quot;file_path&quot;:&quot;dataset/data.jsonl&quot;
            }
        }
    ],
    &quot;validation_datasets&quot;:[
        {
            &quot;data_source_type&quot;:&quot;oss_mount&quot;,
            &quot;mount_storage&quot;:{
                &quot;region&quot;:&quot;cn-beijing&quot;,
                &quot;bucket&quot;:&quot;example_bucket&quot;,
                &quot;file_path&quot;:&quot;dataset/val.jsonl&quot;
            }
        }
    ],
    &quot;hyper_parameters&quot;:{
        &quot;n_epochs&quot;:1,
        &quot;learning_rate&quot;:&quot;1.6e-5&quot;,
        &quot;batch_size&quot;:32,
        &quot;max_length&quot;:8192,
        &quot;split&quot;:0.8
    },
    &quot;training_type&quot;:&quot;sft&quot;,
    &quot;finetuned_output_suffix&quot;:&quot;suffix&quot;
}'
</code></pre></div><a id="fig-code-group-dashscope-cli-tab"></a>dashscope CLI<div><a id="code-code-group-dashscope-cli"></a><pre class="language-bash"><code>export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
# 列出微调任务
dashscope ft list

# 创建微调任务
dashscope ft create -t &lt;file-id&gt; -m qwen3-4b-instruct-2507 -e 1 -b 8
</code></pre></div></div><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../model-api-reference/preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="txt-resp-header-h4"></a><h3>返回参数</h3><p><strong>request_id</strong> <code>string</code></p><p>本次请求的ID。</p><p><strong>output</strong> <code>object</code></p><p>任务详情。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>job_id</strong> <code>string</code></p><p>模型微调任务唯一标识，用于查询任务详情、日志、取消或删除任务。生成规则：<code>ft-{yyyyMMddHHmm}-{4位uuid}</code>。</p><p><strong>job_name</strong> <code>string</code></p><p>模型微调任务名称。</p><p><strong>status</strong> <code>string</code></p><p>微调训练任务的状态：</p><ul><li><code>PENDING</code>：训练待开始。</li><li><code>QUEUING</code>：训练正在排队（同一时间只能运行一个微调任务）。</li><li><code>RUNNING</code>：训练正在进行中。</li><li><code>SUCCEEDED</code>：训练成功。</li><li><code>FAILED</code>：训练失败。</li><li><code>CANCELED</code>：训练已取消。</li><li><code>CANCELING</code>：训练正在取消中。</li></ul><p><strong>finetuned_output</strong> <code>string</code></p><p>微调后产出的新模型ID。任务状态为 SUCCEEDED 时返回。</p><p><strong>model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>base_model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>training_file_ids</strong> <code>array</code></p><p>兼容旧版字段，新任务始终返回空数组，请使用 <code>training_datasets</code>。</p><p><strong>training_datasets</strong> <code>Array of Dataset</code></p><p>训练数据集列表。</p><p><strong>validation_file_ids</strong> <code>array</code></p><p>兼容旧版字段，新任务始终返回空数组，请使用 <code>validation_datasets</code>。</p><p><strong>validation_datasets</strong> <code>Array of Dataset</code></p><p>验证数据集列表。若未指定验证集，为空数组。</p><p><strong>hyper_parameters</strong> <code>object</code></p><p>实际使用的超参数。</p><p><strong>training_type</strong> <code>string</code></p><p>模型微调的训练方式。</p><p><strong>create_time</strong> <code>string</code></p><p>任务创建时间。</p><p><strong>end_time</strong> <code>string</code></p><p>任务结束时间。任务状态为 SUCCEEDED、FAILED 或 CANCELED 时返回。</p><p><strong>usage</strong> <code>integer</code></p><p>微调任务消耗的 Token 数。扣费计算公式请参考：<a href="https://help.aliyun.com/zh/model-studio/billing-for-model-studio">计费说明</a>。任务状态为 SUCCEEDED 或 CANCELED 时返回。</p><p><strong>workspace_id</strong> <code>string</code></p><p>调优任务所属的业务空间ID。</p><p><strong>user_identity</strong> <code>string</code></p><p>用户标识，阿里云账号ID。</p><p><strong>creator</strong> <code>string</code></p><p>创建人的阿里云账号ID。</p><p><strong>modifier</strong> <code>string</code></p><p>修改人的阿里云账号ID。</p><p><strong>group</strong> <code>string</code></p><p>模型微调任务分组。</p></div></section><p><strong>code</strong> <code>string</code></p><p>错误码。调用失败时返回。请参见下方错误码表。</p><p><strong>message</strong> <code>string</code></p><p>错误详情描述。调用失败时返回。</p></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-成功响应示例-tab"></a>成功响应示例<div><a id="code-code-group-2-成功响应示例"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;9654e55a-d74b-4113-aee1-fa19c9384fcc&quot;,
    &quot;output&quot;: {
        &quot;job_id&quot;: &quot;ft-202410291653-1c7f&quot;,
        &quot;job_name&quot;: &quot;ft-202410291653-1c7f&quot;,
        &quot;status&quot;: &quot;PENDING&quot;,
        &quot;model&quot;: &quot;qwen3-14b&quot;,
        &quot;base_model&quot;: &quot;qwen3-14b&quot;,
        &quot;training_file_ids&quot;: [],
        &quot;training_datasets&quot;: [
            {
                &quot;data_source_type&quot;: &quot;file_id&quot;,
                &quot;file_id&quot;: &quot;976bd01a-f30b-4414-86fd-50c54486e3ef&quot;
            }
        ],
        &quot;validation_file_ids&quot;: [],
        &quot;validation_datasets&quot;: [],
        &quot;hyper_parameters&quot;: {
            &quot;n_epochs&quot;: 3,
            &quot;batch_size&quot;: 32,
            &quot;max_length&quot;: 8192,
            &quot;learning_rate&quot;: &quot;1.6e-5&quot;,
            &quot;lr_scheduler_type&quot;: &quot;linear&quot;,
            &quot;split&quot;: 0.9
        },
        &quot;training_type&quot;: &quot;sft&quot;,
        &quot;create_time&quot;: &quot;2024-10-29 16:53:53&quot;,
        &quot;workspace_id&quot;:&quot;llm-v71tlv***&quot;,
        &quot;user_identity&quot;: &quot;1396993924585947&quot;,
        &quot;modifier&quot;: &quot;1396993924585947&quot;,
        &quot;creator&quot;: &quot;1396993924585947&quot;,
        &quot;group&quot;: &quot;llm&quot;
    }
}
</code></pre></div><a id="fig-code-group-2-错误响应示例-tab"></a>错误响应示例<div><a id="code-code-group-2-错误响应示例"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;request_id&quot;: &quot;BE213CDD-8A5C-59EE-9A67-055EAB0CB59B&quot;,
    &quot;message&quot;: &quot;Missing training files&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="错误码"></a>

<a id="txt-err-h2"></a>

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

<a id="txt-ft-next-h2"></a>

## 下一步

调优为异步操作，调用本接口后可通过[查询和管理调优任务](../model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)接口查询调优任务状态。
