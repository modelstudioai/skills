# 图像生成-创建调优任务

创建一个图像生成的模型微调训练任务。数据集支持通过API上传数据集或OSS挂载。

<a id="适用范围"></a>

<a id="img-prereq-title"></a>

<a id="img-prereq-section"></a>

## 适用范围

-   **适用地域**：本文描述的功能**仅在华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   **开通账号权限**：若使用[阿里云子账号](../model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](../model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](../model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](../model-api-reference/preparations/get-api-key.md)。
-   **准备工作**：已阅读[图像生成模型调优](../model-user-guide/model-training/fine-tuning/wan-image-generation-finetune-guide.md)，了解支持微调的模型、微调步骤、数据格式以及计费说明。

<a id="创建微调任务"></a>

<a id="img-api-h2"></a>

<a id="img-api-section"></a>

## 创建微调任务

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

<table><tbody><tr><td><a id="img-req-header-h4"></a><a id="img-req-section"></a><h3>请求参数</h3><a id="img-req-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定值：<code>application/json</code></p><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key鉴权，格式为<code>Bearer sk-xxxx</code>。</p><a id="img-req-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>指定微调所用的基准模型。</p><ul><li><code>wan2.7-image-pro</code>：推荐用于文生图/图生图微调。</li><li><code>wan2.7-image</code></li><li><code>qwen-image-2.0</code>：千问图像生成模型。支持的超参数与万相不同，请参见下方<strong>超参数属性（qwen-image-2.0、qwen-image-2.0-pro）</strong>。</li><li><code>qwen-image-2.0-pro</code>：千问图像生成模型。超参数与 qwen-image-2.0 完全一致，请参见下方<strong>超参数属性（qwen-image-2.0、qwen-image-2.0-pro）</strong>。</li></ul><p><strong>training_file_ids</strong> <code>array[string]</code> <strong>（条件必选）</strong></p><p>训练集文件ID数组，可传入多个ID。与 <code>training_datasets</code> 二选一，若使用 <code>training_datasets</code> 则无需传此参数。文件ID通过<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 获取。</p><p><strong>validation_file_ids</strong> <code>array[string]</code> （可选）</p><p>验证集文件ID数组，可传入多个ID。与 <code>validation_datasets</code> 二选一，若使用 <code>validation_datasets</code> 则无需传此参数。若两者均不提供，系统会从训练集中自动划分。文件ID通过<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 获取。</p><p><strong>training_type</strong> <code>string</code> <strong>（必选）</strong></p><p>微调类型，当前仅支持<code>efficient_sft</code>（LoRA高效微调）。</p><p><strong>hyper_parameters</strong> <code>object</code> （可选）</p><p><strong>超参数配置</strong>。初次训练时，推荐使用默认的超参数。若模型效果不佳或训练不收敛，可以尝试调整训练量（万相为 max_steps，qwen-image-2.0、qwen-image-2.0-pro 为 n_epochs）或 learning_rate 等参数。不同基准模型支持的超参数不同，请参见下方对应的超参数属性。</p><a id="accordion-超参数属性-wan2-7-image-pro-wan2-7-image"></a><section><p>超参数属性（wan2.7-image-pro、wan2.7-image）</p><div><p><strong>max_steps</strong> <code>int</code> <strong>（必选）</strong></p><p>训练总步数。控制训练时长的核心参数。推荐值：800。</p><p>max_steps 决定训练迭代次数，max_token_length 决定每步处理的数据量。</p><p>建议不少于 500 步以确保模型充分收敛；大数据集可适当增加步数。</p><div><div><p><strong>重要</strong>该参数影响<a href="../model-user-guide/test-1/model-training-and-deployment-billing.md">训练计费</a>，请合理设置。</p></div></div><p><strong>eval_steps</strong> <code>int</code> <strong>（必选）</strong></p><p>验证间隔。推荐值：200。取值需≥0。训练期间每隔多少个 steps 进行一次验证评估，用于阶段性评估模型训练效果。同时保存当前 step 的模型文件。</p><p><strong>learning_rate</strong> <code>float</code> <strong>（必选）</strong></p><p>学习率。推荐值：3e-5。控制模型权重更新的幅度。过高可能导致模型变差，过低则变化不明显。</p><p><strong>generation_type</strong> <code>string</code> <strong>（必选）</strong></p><p>生成模式。决定训练数据格式和推理方式。可选值：</p><ul><li><code>t2i</code>：文生图模式。</li><li><code>i2i</code>：图生图模式。</li></ul><p><strong>max_pixels</strong> <code>string</code> <strong>（必选）</strong></p><p>训练图片的最大分辨率。设置训练集中图片分辨率的像素总数（宽×高）上限，系统仅对超过该值的图片进行缩放处理，未超限的图片保持原样。建议三个分辨率参数（max_pixels、max_token_length、val_img_size）保持一致。</p><ul><li><code>1k</code>：即 1024×1024。</li><li><code>2k</code>：即 2048×2048。</li></ul><p>推荐值：文生图 2k，图生图 1k。</p><p><strong>val_img_size</strong> <code>string</code> <strong>（必选）</strong></p><p>验证图生成分辨率。训练过程中验证评估时生成图片的目标分辨率。可选值同 max_pixels。推荐值：文生图 2k，图生图 1k。</p><p><strong>max_token_length</strong> <code>string</code> <strong>（必选）</strong></p><p>每步训练的最大 Token 长度，影响单步计算量与计费。与 max_steps 共同控制训练过程：max_steps 决定迭代次数，max_token_length 决定每步处理的数据量。可选值：</p><ul><li><code>1k</code>：推荐图生图场景使用。</li><li><code>2k</code>：推荐文生图场景使用。</li></ul><p>max_token_length 与计费 Lmax 的对应关系：</p><table><thead><tr><th><p><strong>generation_type</strong></p></th><th><p><strong>max_token_length</strong></p></th><th><p><strong>L</strong><strong>max</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>t2i（文生图）</p></td><td><p>1k</p></td><td><p>12,800</p></td></tr><tr><td><p>2k</p></td><td><p>23,220</p></td></tr><tr><td rowspan="2"><p>i2i（图生图）</p></td><td><p>1k</p></td><td><p>23,220</p></td></tr><tr><td><p>2k</p></td><td><p>32,000</p></td></tr></tbody></table><p><strong>gradient_clip</strong> <code>float</code> <strong>（必选）</strong></p><p>梯度裁剪。推荐值：0.5。对所有可训练参数做全局梯度范数裁剪的阈值，防止梯度爆炸。设为 -1 表示不裁剪。</p><p><strong>weight_decay</strong> <code>float</code> <strong>（必选）</strong></p><p>权重衰减。推荐值：0.02。AdamW 解耦式权重衰减系数，对所有可训练参数生效，用于正则化防止过拟合。</p><p><strong>lora_rank</strong> <code>int</code> <strong>（必选）</strong></p><p>LoRA 低秩矩阵的维数。推荐值：32。该值决定了微调参数量的大小。数值越大，模型拟合能力越强，但训练速度会变慢。取值必须为2n（如 16、32、64）。</p><p><strong>save_total_limit</strong> <code>int</code> （可选）</p><p>Checkpoint 保存数量上限。推荐值：10。限制最多保存的模型数量。系统将始终只保存训练生成的最后 N 个 Checkpoint。</p><p><strong>split</strong> <code>float</code> （可选）</p><p>训练集划分比例。推荐值：0.9。取值范围为 (0, 1)。仅在未指定<code>validation_file_ids</code>或<code>validation_datasets</code>时生效。此参数用于从训练集中自动按比例拆分出验证集。例如，0.9表示90%训练集，10%验证集。</p></div></section><a id="accordion-超参数属性-qwen-image-2-0-qwen-image-2-0-pro"></a><section><p>超参数属性（qwen-image-2.0、qwen-image-2.0-pro）</p><div><p>qwen-image-2.0、qwen-image-2.0-pro 按<strong>训练轮数</strong>（n_epochs）控制训练过程，不支持 max_steps、eval_steps 和 max_token_length 参数。两者的超参数一致，仅推荐学习率不同：qwen-image-2.0 为 5e-5，qwen-image-2.0-pro 为 1e-4。</p><p><strong>n_epochs</strong> <code>int</code> <strong>（必选）</strong></p><p>训练轮数。模型在训练集上完整迭代的次数。推荐值：10。取值范围：[1, 10000]。轮数越多模型拟合越充分，但过多可能导致过拟合。</p><div><div><p><strong>重要</strong>该参数影响<a href="../model-user-guide/test-1/model-training-and-deployment-billing.md">训练计费</a>，请合理设置。</p></div></div><p><strong>eval_epochs</strong> <code>int</code> <strong>（必选）</strong></p><p>验证间隔轮数。推荐值：10。取值范围：[1, 1000]。训练期间每隔多少轮进行一次验证评估，用于阶段性评估模型训练效果。同时保存当前轮次的模型文件。</p><p><strong>batch_size</strong> <code>int</code> （可选）</p><p>批次大小。每次参数更新使用的样本数。推荐值：8。取值范围：[1, 2048]。该参数不参与计费，不影响训练Token总量。</p><p><strong>learning_rate</strong> <code>float</code> <strong>（必选）</strong></p><p>学习率。推荐值：qwen-image-2.0 为 5e-5，qwen-image-2.0-pro 为 1e-4。控制模型权重更新的幅度。过高可能导致模型变差，过低则变化不明显。</p><p><strong>generation_type</strong> <code>string</code> <strong>（必选）</strong></p><p>生成模式。决定训练数据格式和推理方式。可选值：</p><ul><li><code>t2i</code>：文生图模式。</li><li><code>i2i</code>：图生图模式。</li></ul><p>推荐值：i2i。</p><p><strong>max_pixels</strong> <code>string</code> <strong>（必选）</strong></p><p>训练图片的最大分辨率。取值为字符串档位，设置训练集中图片分辨率的像素总数（宽×高）上限，系统仅对超过该值的图片进行缩放处理，未超限的图片保持原样。可选值：</p><ul><li><code>1k</code>：即 1024×1024。</li><li><code>2k</code>：即 2048×2048。</li></ul><p>推荐值：2k。建议与 val_img_size 保持一致。</p><div><div><p><strong>重要</strong>该参数影响<a href="../model-user-guide/test-1/model-training-and-deployment-billing.md">训练计费</a>，请合理设置。</p></div></div><p><strong>val_img_size</strong> <code>string</code> <strong>（必选）</strong></p><p>验证图生成分辨率。训练过程中验证评估时生成图片的目标分辨率。可选值同 max_pixels。推荐值：2k。</p><p><strong>gradient_clip</strong> <code>float</code> <strong>（必选）</strong></p><p>梯度裁剪。推荐值：0.5。取值范围：[0, 10.0]。对所有可训练参数做全局梯度范数裁剪的阈值，防止梯度爆炸。</p><p><strong>weight_decay</strong> <code>float</code> <strong>（必选）</strong></p><p>权重衰减。推荐值：0.02。取值范围：[0, 1.0]。AdamW 解耦式权重衰减系数，对所有可训练参数生效，用于正则化防止过拟合。</p><p><strong>lora_rank</strong> <code>int</code> <strong>（必选）</strong></p><p>LoRA 低秩矩阵的维数。推荐值：32。取值范围：[8, 128]。该值决定了微调参数量的大小。数值越大，模型拟合能力越强，但训练速度会变慢。</p><p><strong>save_total_limit</strong> <code>int</code> （可选）</p><p>Checkpoint 保存数量上限。推荐值：20。取值范围：[1, 40]。限制最多保存的模型数量。系统将始终只保存训练生成的最后 N 个 Checkpoint。</p><p><strong>split</strong> <code>float</code> （可选）</p><p>训练集划分比例。推荐值：0.9。取值范围：[0, 1]。仅在未指定<code>validation_file_ids</code>或<code>validation_datasets</code>时生效。此参数用于从训练集中自动按比例拆分出验证集。例如，0.9表示90%训练集，10%验证集。</p></div></section><p><strong>training_datasets</strong> <code>Array of Dataset</code> <strong>（条件必选）</strong></p><p>训练集文件列表。与 <code>training_file_ids</code> 二选一，若使用 <code>training_file_ids</code> 则无需传此参数。</p><a id="accordion-dataset-结构"></a><section><p>Dataset 结构</p><div><p><strong>data_source_type</strong> <code>string</code> <strong>（必选）</strong></p><p>数据源类型，可选值：</p><ul><li><code>oss_mount</code>（挂载 OSS 文件）</li><li><code>file_id</code>（由文件管理服务 API 上传的文件）</li></ul><p><strong>mount_storage</strong> <code>object</code> （条件必选）</p><p>数据源类型为 <code>oss_mount</code> 时必填。OSS 挂载信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>region</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS Bucket 所属地域。支持北京（cn-beijing）和新加坡（ap-southeast-1）。</p><p><strong>bucket</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS Bucket 名称。</p><p><strong>file_path</strong> <code>string</code> <strong>（必选）</strong></p><p>要挂载的 OSS 文件路径（object key）。对包含多个文件的数据集，使用其 data.jsonl 的文件路径。与使用 file_id 的方式不同，需要将未经压缩的数据集文件夹整体上传到 OSS，不支持 zip 文件。</p></div></section><p><strong>file_id</strong> <code>string</code> （条件必选）</p><p>数据源类型为 <code>file_id</code> 时必填。文件 ID，由<a href="../model-api-reference/file-management-api/upload-file-api.md">上传文件 API</a> 产生。</p></div></section><p><strong>validation_datasets</strong> <code>Array of Dataset</code> （可选）</p><p>验证集文件列表。结构同<code>training_datasets</code>。</p><p>与 <code>validation_file_ids</code> 二选一。若两者均不提供，系统会从训练集中自动划分。</p><p><strong>job_name</strong> <code>string</code> （可选）</p><p>调优任务名称。</p><p><strong>model_name</strong> <code>string</code> （可选）</p><p>调优完成后的模型名称。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-文生图-wan2-7-image-pro-tab"></a>文生图（wan2.7-image-pro）<div><a id="code-code-group-文生图-wan2-7-image-pro"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;training_file_ids&quot;: [
        &quot;&lt;替换为训练数据集的文件id&gt;&quot;
    ],
    &quot;training_type&quot;: &quot;efficient_sft&quot;,
    &quot;hyper_parameters&quot;: {
        &quot;learning_rate&quot;: 3e-5,
        &quot;max_steps&quot;: 800,
        &quot;eval_steps&quot;: 200,
        &quot;max_token_length&quot;: &quot;2k&quot;,
        &quot;gradient_clip&quot;: 0.5,
        &quot;weight_decay&quot;: 0.02,
        &quot;max_pixels&quot;: &quot;2k&quot;,
        &quot;val_img_size&quot;: &quot;2k&quot;,
        &quot;generation_type&quot;: &quot;t2i&quot;,
        &quot;lora_rank&quot;: 32,
        &quot;save_total_limit&quot;: 10
    }
}'
</code></pre></div><a id="fig-code-group-图生图-wan2-7-image-tab"></a>图生图（wan2.7-image）<div><a id="code-code-group-图生图-wan2-7-image"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wan2.7-image&quot;,
    &quot;training_file_ids&quot;: [
        &quot;&lt;替换为训练数据集的文件id&gt;&quot;
    ],
    &quot;training_type&quot;: &quot;efficient_sft&quot;,
    &quot;hyper_parameters&quot;: {
        &quot;learning_rate&quot;: 3e-5,
        &quot;max_steps&quot;: 800,
        &quot;eval_steps&quot;: 200,
        &quot;max_token_length&quot;: &quot;1k&quot;,
        &quot;gradient_clip&quot;: 0.5,
        &quot;weight_decay&quot;: 0.02,
        &quot;max_pixels&quot;: &quot;1k&quot;,
        &quot;val_img_size&quot;: &quot;1k&quot;,
        &quot;generation_type&quot;: &quot;i2i&quot;,
        &quot;lora_rank&quot;: 32,
        &quot;save_total_limit&quot;: 10
    }
}'
</code></pre></div><a id="fig-code-group-千问-qwen-image-2-0-tab"></a>千问（qwen-image-2.0）<div><a id="code-code-group-千问-qwen-image-2-0"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen-image-2.0&quot;,
    &quot;training_file_ids&quot;: [
        &quot;&lt;替换为训练数据集的文件id&gt;&quot;
    ],
    &quot;training_type&quot;: &quot;efficient_sft&quot;,
    &quot;hyper_parameters&quot;: {
        &quot;learning_rate&quot;: 5e-5,
        &quot;n_epochs&quot;: 10,
        &quot;eval_epochs&quot;: 10,
        &quot;batch_size&quot;: 8,
        &quot;gradient_clip&quot;: 0.5,
        &quot;weight_decay&quot;: 0.02,
        &quot;max_pixels&quot;: &quot;2k&quot;,
        &quot;val_img_size&quot;: &quot;2k&quot;,
        &quot;generation_type&quot;: &quot;t2i&quot;,
        &quot;lora_rank&quot;: 32,
        &quot;save_total_limit&quot;: 20
    }
}'
</code></pre></div><a id="fig-code-group-千问-qwen-image-2-0-pro-tab"></a>千问（qwen-image-2.0-pro）<div><a id="code-code-group-千问-qwen-image-2-0-pro"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen-image-2.0-pro&quot;,
    &quot;training_file_ids&quot;: [
        &quot;&lt;替换为训练数据集的文件id&gt;&quot;
    ],
    &quot;training_type&quot;: &quot;efficient_sft&quot;,
    &quot;hyper_parameters&quot;: {
        &quot;learning_rate&quot;: 1e-4,
        &quot;n_epochs&quot;: 10,
        &quot;eval_epochs&quot;: 10,
        &quot;batch_size&quot;: 8,
        &quot;gradient_clip&quot;: 0.5,
        &quot;weight_decay&quot;: 0.02,
        &quot;max_pixels&quot;: &quot;2k&quot;,
        &quot;val_img_size&quot;: &quot;2k&quot;,
        &quot;generation_type&quot;: &quot;t2i&quot;,
        &quot;lora_rank&quot;: 32,
        &quot;save_total_limit&quot;: 20
    }
}'
</code></pre></div><a id="fig-code-group-使用oss挂载的数据集-tab"></a>使用OSS挂载的数据集<div><a id="code-code-group-使用oss挂载的数据集"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
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
    &quot;training_type&quot;: &quot;efficient_sft&quot;,
    &quot;hyper_parameters&quot;: {
        &quot;learning_rate&quot;: 3e-5,
        &quot;max_steps&quot;: 800,
        &quot;eval_steps&quot;: 200,
        &quot;max_token_length&quot;: &quot;2k&quot;,
        &quot;gradient_clip&quot;: 0.5,
        &quot;weight_decay&quot;: 0.02,
        &quot;max_pixels&quot;: &quot;2k&quot;,
        &quot;val_img_size&quot;: &quot;2k&quot;,
        &quot;generation_type&quot;: &quot;t2i&quot;,
        &quot;lora_rank&quot;: 32,
        &quot;save_total_limit&quot;: 10
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="img-resp-header-h4"></a><a id="img-resp-section"></a><h3>响应参数</h3><p><strong>request_id</strong> <code>string</code></p><p>请求的唯一标识符。</p><p><strong>output</strong> <code>object</code></p><p>任务详情。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>job_id</strong> <code>string</code></p><p>模型微调任务唯一标识，用于查询任务详情、日志、取消或删除任务。生成规则：<code>ft-{yyyyMMddHHmm}-{4位uuid}</code>。</p><p><strong>job_name</strong> <code>string</code></p><p>模型微调任务名称。</p><p><strong>status</strong> <code>string</code></p><p>微调训练任务的状态：</p><ul><li><code>PENDING</code>：训练待开始。</li><li><code>QUEUING</code>：训练正在排队（同一时间只能运行一个微调任务）。</li><li><code>RUNNING</code>：训练正在进行中。</li><li><code>SUCCEEDED</code>：训练成功。</li><li><code>FAILED</code>：训练失败。</li><li><code>CANCELED</code>：训练已取消。</li><li><code>CANCELING</code>：训练正在取消中。</li></ul><p><strong>finetuned_output</strong> <code>string</code></p><p>微调后产出的新模型ID，部署和调用时需要用到。任务状态为 SUCCEEDED 时返回。</p><p><strong>model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>base_model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>training_file_ids</strong> <code>array</code></p><p>兼容旧版字段，新任务始终返回空数组，请使用 <code>training_datasets</code>。</p><p><strong>training_datasets</strong> <code>Array of Dataset</code></p><p>训练数据集列表。</p><p><strong>validation_file_ids</strong> <code>array</code></p><p>兼容旧版字段，新任务始终返回空数组，请使用 <code>validation_datasets</code>。</p><p><strong>validation_datasets</strong> <code>Array of Dataset</code></p><p>验证数据集列表。若未指定验证集，为空数组。</p><p><strong>hyper_parameters</strong> <code>object</code></p><p>实际使用的超参数。</p><p><strong>training_type</strong> <code>string</code></p><p>模型微调的训练方式。</p><p><strong>create_time</strong> <code>string</code></p><p>任务创建时间。</p><p><strong>end_time</strong> <code>string</code></p><p>任务结束时间。任务状态为 SUCCEEDED、FAILED 或 CANCELED 时返回。</p><p><strong>usage</strong> <code>integer</code></p><p>微调任务消耗的 Token 数。任务状态为 SUCCEEDED 或 CANCELED 时返回。</p><p><strong>workspace_id</strong> <code>string</code></p><p>阿里云百炼API Key所属的业务空间ID。请参见<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md">获取Workspace ID</a>。</p><p><strong>user_identity</strong> <code>string</code></p><p>用户标识，阿里云账号ID。</p><p><strong>creator</strong> <code>string</code></p><p>创建人的阿里云账号ID。</p><p><strong>modifier</strong> <code>string</code></p><p>修改人的阿里云账号ID。</p><p><strong>group</strong> <code>string</code></p><p>模型微调任务分组。</p><p><strong>max_output_cnt</strong> <code>integer</code></p><p>训练期间最多保存的 checkpoint 数量。等同于超参数 save_total_limit 的值。</p></div></section><p><strong>code</strong> <code>string</code></p><p>错误码。调用失败时返回。请参见下方错误码表。</p><p><strong>message</strong> <code>string</code></p><p>错误详情描述。调用失败时返回。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应示例"></a><section><a id="成功响应示例-h4"></a><h4>成功响应示例</h4><p>重点关注：<code>output.job_id</code>（任务ID）、<code>output.finetuned_output</code>（微调后产出的新模型名称）。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;0eb05b0c-02ba-414a-9d0c-xxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;job_id&quot;: &quot;ft-202606030110-xxxx&quot;,
        &quot;job_name&quot;: &quot;ft-202606030110-xxxx&quot;,
        &quot;status&quot;: &quot;PENDING&quot;,
        &quot;finetuned_output&quot;: &quot;wan2.7-image-pro-ft-202606030110-xxxx&quot;,
        &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
        &quot;base_model&quot;: &quot;wan2.7-image-pro&quot;,
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
            &quot;max_steps&quot;: 800,
            &quot;learning_rate&quot;: 3.0E-5,
            &quot;eval_steps&quot;: 200,
            &quot;max_token_length&quot;: &quot;2k&quot;,
            &quot;max_pixels&quot;: &quot;2k&quot;,
            &quot;val_img_size&quot;: &quot;2k&quot;,
            &quot;generation_type&quot;: &quot;t2i&quot;,
            &quot;lora_rank&quot;: 32
        },
        &quot;training_type&quot;: &quot;efficient_sft&quot;,
        &quot;create_time&quot;: &quot;2026-06-03 01:10:47&quot;
    }
}
</code></pre></section><a id="错误响应示例"></a><section><a id="错误响应示例-h4"></a><h4>错误响应示例</h4><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;request_id&quot;: &quot;BE213CDD-8A5C-59EE-9A67-055EAB0CB59B&quot;,
    &quot;message&quot;: &quot;The model wan2.7-image-pro does not support training_type: full_sft&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="img-err-h2"></a>

<a id="img-err-section"></a>

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

<a id="img-ft-next-h2"></a>

<a id="img-ft-next"></a>

## 下一步

调优为异步操作，调用本接口后可通过[查询和管理调优任务](../model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)接口查询调优任务状态。
