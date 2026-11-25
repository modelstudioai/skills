# 图像生成-部署模型

将训练好的图像生成模型发布为在线 API 服务。

<a id="适用范围"></a>

<a id="img-dep-prereq-title"></a>

<a id="img-dep-prereq-section"></a>

## 适用范围

-   **适用地域**：当前模型部署 API **仅在华北2（北京）地域**开放。如您使用其他地域，请通过该地域的百炼控制台完成模型部署操作。
-   **开通账号权限**：若使用[阿里云子账号](../model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](../model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](../model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](../model-api-reference/preparations/get-api-key.md)。
-   **前提条件**：已完成模型微调训练。请先调用[查询调优任务](create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口，确认任务状态 `status` 为 **SUCCEEDED** 后再进行部署。

<a id="部署模型"></a>

<a id="img-dep-main-h2"></a>

<a id="img-dep-main-section"></a>

## 部署模型

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/deployments`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

<table><tbody><tr><td><a id="img-dep-req-header-h4"></a><a id="img-dep-req-section"></a><h3>请求参数</h3><a id="img-dep-req-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定值：<code>application/json</code></p><p><strong>Authorization</strong> <code>string</code> <strong>（必选）</strong></p><p>API Key鉴权，格式为<code>Bearer sk-xxxx</code>。</p><a id="img-dep-req-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model_name</strong> <code>string</code> <strong>（必选）</strong></p><p>待部署的模型ID（非基础模型名称，而是微调或导出后生成的模型标识）。获取方式：</p><ul><li>微调产出的模型：使用<a href="create-fine-tuning-job-api-ec89a5612f9a9ba9.md">创建调优任务</a>响应中 <code>output.finetuned_output</code> 的值。</li><li>导出的模型：使用<a href="create-fine-tuning-job-api-ec89a5612f9a9ba9.md">查询导出的模型详情</a>响应中 <code>output[].model_name</code> 的值。</li></ul><p><strong>capacity</strong> <code>integer</code> <strong>（必选）</strong></p><p>部署的模型实例数量。推荐设置为1。</p><p><strong>plan</strong> <code>string</code> <strong>（必选）</strong></p><p>部署方式。LoRA高效微调推荐为<code>lora</code>。</p></td><td><a id="sec-tabs-2"></a><section><a id="部署模型-2"></a><section><a id="部署模型-2-h4"></a><h4>部署模型</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model_name&quot;: &quot;&lt;替换为模型名称model_name&gt;&quot;,
    &quot;capacity&quot;: 1,
    &quot;plan&quot;: &quot;lora&quot;
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="img-dep-resp-header-h4"></a><a id="img-dep-resp-section"></a><h3>响应参数</h3><p><strong>request_id</strong> <code>string</code></p><p>请求的唯一标识符。</p><p><strong>output</strong> <code>object</code></p><p>任务详情。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>deployed_model</strong> <code>string</code></p><p>部署模型的唯一标识。用于查询模型部署状态和调用模型。</p><p><strong>model_name</strong> <code>string</code></p><p>模型标识名。</p><p><strong>status</strong> <code>string</code></p><p>部署状态：</p><ul><li><code>PENDING</code>：部署中。</li><li><code>RUNNING</code>：运行中。</li><li><code>FAILED</code>：部署失败。</li></ul><p><strong>base_model</strong> <code>string</code></p><p>使用的基准模型。</p><p><strong>gmt_create</strong> <code>string</code></p><p>部署任务创建时间。</p><p><strong>gmt_modified</strong> <code>string</code></p><p>部署任务更新时间。</p><p><strong>workspace_id</strong> <code>string</code></p><p>阿里云百炼API Key所属的业务空间ID。请参见<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md">获取Workspace ID</a>。</p><p><strong>charge_type</strong> <code>string</code></p><p>付费模式。post_paid表示后付费。</p><p><strong>creator</strong> <code>string</code></p><p>创建人的阿里云账号ID。</p><p><strong>modifier</strong> <code>string</code></p><p>修改人的阿里云账号ID。</p><p><strong>plan</strong> <code>string</code></p><p>部署方式。</p></div></section><p><strong>code</strong> <code>string</code></p><p>错误码。调用失败时返回。</p><p><strong>message</strong> <code>string</code></p><p>错误详情描述。调用失败时返回。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应示例"></a><section><a id="成功响应示例-h4"></a><h4>成功响应示例</h4><p>重点关注：<code>output.deployed_model</code>（部署模型的唯一标识）、<code>output.status</code>（部署状态）。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;96020b2e-9072-4c8a-9981-xxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;deployed_model&quot;: &quot;wan2.7-image-pro-ft-202507011122-xxxx&quot;,
        &quot;gmt_create&quot;: &quot;2025-07-01T10:30:00.000&quot;,
        &quot;gmt_modified&quot;: &quot;2025-07-01T10:30:00.000&quot;,
        &quot;status&quot;: &quot;PENDING&quot;,
        &quot;model_name&quot;: &quot;wan2.7-image-pro-ft-202507011122-xxxx&quot;,
        &quot;base_model&quot;: &quot;wan2.7-image-pro&quot;,
        &quot;workspace_id&quot;: &quot;llm-xxxxxxxxx&quot;,
        &quot;charge_type&quot;: &quot;post_paid&quot;,
        &quot;creator&quot;: &quot;12xxxxxxx&quot;,
        &quot;modifier&quot;: &quot;12xxxxxxx&quot;,
        &quot;plan&quot;: &quot;lora&quot;
    }
}
</code></pre></section><a id="错误响应示例"></a><section><a id="错误响应示例-h4"></a><h4>错误响应示例</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;request_id&quot;: &quot;BE213CDD-8A5C-59EE-9A67-055EAB0CB59B&quot;,
    &quot;message&quot;: &quot;The model xxx does not exist or is not deployable&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="下一步"></a>

<a id="img-dep-next-h2"></a>

<a id="img-dep-next"></a>

## 下一步

部署为异步操作，调用本接口后可通过[查询和管理部署](../model-api-reference/model-production/deployments-api/get-deployment-api.md)接口查询部署状态。
