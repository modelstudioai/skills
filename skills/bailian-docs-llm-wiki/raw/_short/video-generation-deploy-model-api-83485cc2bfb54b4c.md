# 视频生成-部署模型

将训练好的模型发布为在线 API 服务。

<a id="适用范围"></a>

<a id="dep-prereq-title"></a>

<a id="dep-prereq-section"></a>

## 适用范围

-   **适用地域**：当前模型部署 API **仅在华北2（北京）地域**开放。如您使用其他地域，请通过该地域的百炼控制台完成模型部署操作。
-   **开通账号权限**：若使用[阿里云子账号](../model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](../model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](../model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](../model-api-reference/preparations/get-api-key.md)。
-   **前提条件**：已完成模型微调训练。请先调用[查询调优任务](create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口，确认任务状态 `status` 为 **SUCCEEDED** 后再进行部署。

<a id="部署模型"></a>

<a id="dep-main-h2"></a>

<a id="dep-main-section"></a>

## 部署模型

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/deployments`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

<table><tbody><tr><td><a id="dep-req-header-h4"></a><a id="dep-req-section"></a><h3>请求参数</h3><a id="dep-req-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定值：<code>application/json</code></p><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key鉴权，格式为<code>Bearer sk-xxxx</code>。</p><a id="dep-req-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model_name</strong> <code>string</code> <strong>（必选）</strong></p><p>待部署的模型ID（非基础模型名称，而是微调或导出后生成的模型标识）。获取方式：</p><ul><li>微调产出的模型：使用<a href="video-generation-create-fine-tuning-job-api-2357b2afaa3e843c.md">创建调优任务</a>响应中 <code>output.finetuned_output</code> 的值，格式如 <code>wan2.5-i2v-preview-ft-202511111122-xxxx</code>。</li><li>导出的模型：使用<a href="create-fine-tuning-job-api-ec89a5612f9a9ba9.md">查询导出的模型详情</a>响应中 <code>output[].model_name</code> 的值。</li></ul><p><strong>capacity</strong> <code>integer</code> <strong>（必选）</strong></p><p>部署的模型实例数量。推荐设置为1。</p><p><strong>plan</strong> <code>string</code> <strong>（必选）</strong></p><p>部署方式。LoRA高效微调推荐为<code>lora</code>。</p><p><strong>aigc_config</strong> <code>object</code> <strong>（必选）</strong></p><p>提示词配置。</p><a id="accordion-aigc-config-属性"></a><section><p>aigc_config 属性</p><div><p><strong>use_input_prompt</strong> <code>boolean</code> <strong>（必选）</strong></p><p>控制调用已部署模型生成视频时的提示词来源。</p><ul><li><code>false</code>（默认值）：自动生成模式。调用视频生成接口时，系统忽略传入的 prompt，强制使用 <code>aigc_config.prompt</code> 和 <code>aigc_config.lora_prompt_default</code> 配置的模板自动生成提示词。</li><li><code>true</code>：手动传入模式。调用视频生成接口时，系统直接使用传入的 prompt，上述两个参数将全部失效。</li></ul><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>预设的Prompt模板。仅在<code>use_input_prompt=false</code>时生效。</p><p>调用已部署模型生成视频时，系统会分析输入图像，将画面内容填入该模板，自动生成带特效指令的完整描述。</p><p>注意：此参数会<strong>覆盖</strong>视频生成接口中传入的 prompt 参数。</p><p><strong>lora_prompt_default</strong> <code>string</code> <strong>（必选）</strong></p><p>备用Prompt模板。仅在<code>use_input_prompt=false</code>时生效。</p><p>当使用<code>aigc_config.prompt</code>生成失败时，系统将使用此参数作为兜底提示词来生成视频。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="图生视频-基于首帧"></a><section><a id="图生视频-基于首帧-h4"></a><h4>图生视频-基于首帧</h4><p>以下示例以金钱雨特效为例，上传一张人物图片，系统自动生成带有特效的视频。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model_name&quot;: &quot;&lt;替换为模型名称model_name&gt;&quot;,
    &quot;aigc_config&quot;: {
        &quot;use_input_prompt&quot;: false,
        &quot;prompt&quot;: &quot;根据图像内容提供视频描述，描述必须包含&quot;然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中&quot;。\n输出模板:\n视频开头展示了[主体描述]。[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。\n示例:\n视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。&quot;,
        &quot;lora_prompt_default&quot;: &quot;然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕主角。钞票持续落下，同时镜头缓缓拉进，主角双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。&quot;
    },
    &quot;capacity&quot;: 1,
    &quot;plan&quot;: &quot;lora&quot;
}'
</code></pre></section><a id="图生视频-基于首尾帧"></a><section><a id="图生视频-基于首尾帧-h4"></a><h4>图生视频-基于首尾帧</h4><p>以下示例以时尚杂志换装特效为例，上传首帧和尾帧图片，系统自动生成人物换装变身的过渡视频。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model_name&quot;: &quot;&lt;替换为模型名称model_name&gt;&quot;,
    &quot;aigc_config&quot;: {
        &quot;use_input_prompt&quot;: false,
        &quot;prompt&quot;: &quot;根据图像内容提供视频描述，描述必须包含&quot;然后她开始了s86b5p变身。&quot;\n输出模板:\n视频开头展示了[主体描述]。[环境描述]。然后她开始了s86b5p变身。\n示例:\n视频开头展示了一位年轻女性在户外的场景。她有着短而卷曲的深棕色头发，面带微笑，显得非常亲切。她穿着一件黑色的Polo衫，上面有彩色的花卉刺绣图案，背景是绿色的植被和远处的山脉。然后她开始了s86b5p变身。&quot;,
        &quot;lora_prompt_default&quot;: &quot;然后她开始了s86b5p变身。&quot;
    },
    &quot;capacity&quot;: 1,
    &quot;plan&quot;: &quot;lora&quot;
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="dep-resp-header-h4"></a><a id="dep-resp-section"></a><h3>响应参数</h3><p><strong>request_id</strong> <code>string</code></p><p>请求的唯一标识符。</p><p><strong>output</strong> <code>object</code></p><p>任务详情。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>deployed_model</strong> <code>string</code></p><p>部署模型的唯一标识。用于查询模型部署状态和调用模型。</p><p><strong>model_name</strong> <code>string</code></p><p>模型标识名。</p><p><strong>status</strong> <code>string</code></p><p>部署状态：</p><ul><li><code>PENDING</code>：部署中。</li><li><code>RUNNING</code>：运行中。</li><li><code>FAILED</code>：部署失败。</li></ul><p><strong>base_model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>gmt_create</strong> <code>string</code></p><p>部署任务创建时间。</p><p><strong>gmt_modified</strong> <code>string</code></p><p>部署任务更新时间。</p><p><strong>workspace_id</strong> <code>string</code></p><p>阿里云百炼API Key所属的业务空间ID。请参见<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md">获取Workspace ID</a>。</p><p><strong>charge_type</strong> <code>string</code></p><p>付费模式。post_paid表示后付费。</p><p><strong>creator</strong> <code>string</code></p><p>创建人的阿里云账号ID。</p><p><strong>modifier</strong> <code>string</code></p><p>修改人的阿里云账号ID。</p><p><strong>plan</strong> <code>string</code></p><p>部署方式。</p></div></section><p><strong>code</strong> <code>string</code></p><p>错误码。调用失败时返回。请参见下方错误码表。</p><p><strong>message</strong> <code>string</code></p><p>错误详情描述。调用失败时返回。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应示例"></a><section><a id="成功响应示例-h4"></a><h4>成功响应示例</h4><p>重点关注：<code>output.deployed_model</code>（部署模型的唯一标识）、<code>output.status</code>（部署状态）。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;96020b2e-9072-4c8a-9981-xxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;deployed_model&quot;: &quot;wan2.5-i2v-preview-ft-202511111122-xxxx&quot;,
        &quot;gmt_create&quot;: &quot;2025-11-11T17:46:53.294&quot;,
        &quot;gmt_modified&quot;: &quot;2025-11-11T17:46:53.294&quot;,
        &quot;status&quot;: &quot;PENDING&quot;,
        &quot;model_name&quot;: &quot;wan2.5-i2v-preview-ft-202511111122-xxxx&quot;,
        &quot;base_model&quot;: &quot;wan2.5-i2v-preview&quot;,
        &quot;workspace_id&quot;: &quot;llm-xxxxxxxxx&quot;,
        &quot;charge_type&quot;: &quot;post_paid&quot;,
        &quot;creator&quot;: &quot;12xxxxxxx&quot;,
        &quot;modifier&quot;: &quot;12xxxxxxx&quot;,
        &quot;plan&quot;: &quot;lora&quot;
    }
}
</code></pre></section><a id="错误响应示例"></a><section><a id="错误响应示例-h4"></a><h4>错误响应示例</h4><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;request_id&quot;: &quot;BE213CDD-8A5C-59EE-9A67-055EAB0CB59B&quot;,
    &quot;message&quot;: &quot;The model xxx does not exist or is not deployable&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="prompt-模板配置"></a>

<a id="dep-aigc-note-h2"></a>

<a id="dep-aigc-note-section"></a>

## Prompt 模板配置

以下说明如何配置 `aigc_config.prompt` 参数。

-   **为什么要设置这个参数**？
    
    如果不设置此参数，每次调用已部署模型都需要手动编写完整 Prompt；设置后，调用微调模型生成视频时，只需上传图片，系统会根据此参数自动补全特效指令，无需手动输入 Prompt。
    
-   **如何设置？** **Prompt = 任务指令（告诉模型要做什么）+ 输出模板（规范输出格式）+ 示例（让模型学习示例结构）。**

<a id="code-block-5"></a>

```text
根据图像内容提供视频描述，描述必须包含"然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中"。
输出模版:
视频开头展示了[主体描述]。[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
示例:
视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
```

> 关于"输出模板"描述，请参见[视频标注：为视频编写Prompt](../model-user-guide/model-training/fine-tuning/wan-video-generation-finetune-guide.md#102ebee9f3dtq)。

<a id="下一步"></a>

<a id="dep-next-h2"></a>

<a id="dep-next"></a>

## 下一步

部署为异步操作，调用本接口后可通过[查询和管理部署](../model-api-reference/model-production/deployments-api/get-deployment-api.md)接口查询部署状态。
