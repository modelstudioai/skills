# 批处理接口API详情

<a id="模型概览"></a>

<a id="d2fcb2eda3q2w"></a>

## 模型概览

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>数据类型</strong></p></th><th><p><strong>向量维度</strong></p></th><th><p><strong>单次请求文本最大行数</strong></p></th><th><p><strong>单行最大输入Token</strong></p></th><th><p><strong>支持语种</strong></p></th></tr></thead><tbody><tr><td><p>text-embedding-async-v2</p></td><td rowspan="2"><p>float（32位）</p></td><td rowspan="2"><p>1,536</p></td><td rowspan="2"><p>100,000</p></td><td rowspan="2"><p>2,048</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语</p></td></tr><tr><td><p>text-embedding-async-v1</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语</p></td></tr></tbody></table>

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>单价</strong></p><p><strong>（每千输入Token）</strong></p></th><th rowspan="2"><p><strong>免费额度（</strong><a href="../../../model-user-guide/test-1/new-free-quota.md#977b13081ab56"><strong>注</strong></a><strong>）</strong></p></th><th colspan="2"><p><strong>限流条件（超出任一数值时触发限流）</strong></p></th></tr><tr><th><p><strong>任务下发接口RPS限制</strong></p></th><th><p><strong>同时处理中任务数量</strong></p></th></tr></thead><tbody><tr><td><p>text-embedding-async-v2</p></td><td rowspan="2"><p>0.0007元</p></td><td><p>2000万Token</p><p>有效期：百炼开通后90天内</p></td><td rowspan="2"><p>1</p></td><td rowspan="2"><p>当前用户在系统通用文本向量异步作业排队中和运行中的作业数量不超过50个。</p><p>另外，为了避免大量突发的作业占据太多资源，限制并发的作业数为3个，即任意时间，单个用户最多只有3个通用文本向量的异步作业在并发运行，其他的作业只能在队列中等待。</p></td></tr><tr><td><p>text-embedding-async-v1</p></td><td><p>无免费额度</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

通用文本向量批处理接口API支持通过HTTP和DashScope SDK进行调用。

在调用前，先[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。

<a id="http调用"></a>

<a id="eb441c2e13too"></a>

## HTTP调用

HTTP调用仅支持异步模式，需通过两步完成：

1.  **创建任务**：首先发送一个请求创建任务，该请求会返回任务ID。
2.  **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。

**通过HTTP调用时需配置的endpoint：**

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="创建任务"></a>

<a id="6628e753b9k79"></a>

### 创建任务

<table><tbody><tr><td><a id="8cc4ebc60c7io"></a><h5>请求参数</h5><a id="36fa8fa1af1e6"></a><h6>请求头（Headers）</h6><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h6>请求体（Request Body）</h6><p><strong>model</strong> <code>string</code><strong>（必选）</strong></p><p>调用模型名称，可以选择<code>text-embedding-async-v1</code>或者<code>text-embedding-async-v2</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>用户需要批量向量化处理的输入。</p><a id="accordion-属性"></a><section><p>属性</p><div><p>url <code>string</code> <strong>（必选）</strong></p><p>用户需要批量向量化的文件HTTP url。（需要embedding的内容，一行一条）</p><p>文本限制：</p><ul><li>单行字符串最长支持 2,048 Token</li><li>单次请求文本最大100,000行</li><li>文件大小不超过 200MB</li></ul></div></section><p><strong>parameters</strong> <code>object</code> <strong>（可选）</strong></p><p>向量化处理参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>text_type</strong> <code>string</code> <strong>（可选）</strong></p><p>参数值：</p><ul><li><code>document</code>(默认值)</li><li><code>query</code></li></ul><p>文本转换为向量后可以应用于检索、聚类、分类等下游任务，对检索这类非对称任务为了达到更好的检索效果建议区分查询文本（query）和底库文本（document）类型；聚类、分类等对称任务无需特别指定，采用系统默认值<code>document</code>即可。</p></div></section></td><td><a id="code-block"></a><pre class="language-bash"><code>curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -H 'X-DashScope-Async: enable' \
    -d '{
    &quot;model&quot;: &quot;text-embedding-async-v2&quot;,
    &quot;input&quot;: {
        &quot;url&quot;: &quot;https://modelscope.oss-cn-beijing.aliyuncs.com/resource/text_embedding_file.txt&quot;
    },
    &quot;parameters&quot;: {
        &quot;text_type&quot;: &quot;query&quot;
    }
}'
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="10da1d2a1e6yp"></a><h5>响应参数</h5><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h5>请求参数</h5><a id="36a28b657f196"></a><h6>请求头（Headers）</h6><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h6>URL路径参数（Path parameters）</h6><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-2"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><blockquote><p>若使用新加坡地域的模型，需将base_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h5>响应参数</h5><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>url</strong> <code>string</code></p><p>模型生成图片的URL地址。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>total_tokens</strong><code>integer</code></p><p>本次请求输入内容的Token数目，根据用户输入的文本文件被模型Tokenizer解析之后所对应的Token数目来进行计算。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、处理结果URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;&lt;Your Request ID&gt;&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;&lt;Your Task ID&gt;&quot;,
        &quot;task_status&quot;:&quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;:&quot;2025-02-20 14:37:13.328&quot;,
        &quot;scheduled_time&quot;:&quot;2025-02-20 14:37:13.352&quot;,
        &quot;end_time&quot;:&quot;2025-02-20 14:37:14.159&quot;,
        &quot;url&quot;:&quot;&lt;包含输出结果的url&gt;&quot;
    },
    &quot;usage&quot;:{
        &quot;total_tokens&quot;:258
    }
}
</code></pre></section><a id="任务执行中"></a><section><a id="任务执行中-h4"></a><h4>任务执行中</h4><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;&lt;Your Request ID&gt;&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;&lt;Your Task ID&gt;&quot;,
        &quot;task_status&quot;:&quot;RUNNING&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>如果因为某种原因导致任务执行失败，任务状态将被设置为FAILED，并通过code和message字段明确指示错误原因。</p><a id="code-block-7"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;&lt;Your Request ID&gt;&quot;
  &quot;output&quot;: {
        &quot;task_id&quot;: &quot;&lt;Your Task ID&gt;&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;:&quot;2025-02-20 15:57:19.039&quot;,
        &quot;scheduled_time&quot;:&quot;2025-02-20 15:57:19.059&quot;,
        &quot;end_time&quot;:&quot;2025-02-20 15:57:19.418&quot;,
        &quot;code&quot;: &quot;xxx&quot;,
         &quot;message&quot;: &quot;xxxxxx&quot;
  }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope"></a>

<a id="69cac67a477k2"></a>

## Dashscope

请先确认已安装最新版DashScope SDK，否则可能运行报错：[安装SDK](../../preparations/install-sdk.md)。

DashScope SDK目前已支持Python和Java。

SDK与HTTP接口的参数名基本一致，参数结构根据不同语言的SDK封装而定。参数说明可参考[万相-文生图V2](../../image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

由于模型处理时间较长，底层服务采用异步方式提供。SDK在上层进行了封装，支持同步、异步两种调用方式。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求体</h4><p><strong>model</strong> <code>string</code><strong>（必选）</strong></p><p>调用模型名称，可以选择<code>text-embedding-async-v1</code>或者<code>text-embedding-async-v2</code>。</p><p>url <code>string</code> <strong>（必选）</strong></p><p>用户需要批量向量化的文件HTTP url。（需要向量化的内容，一行一条）</p><p>文本限制：</p><ul><li>单行字符串最长支持2,048Token</li><li>单次请求文本最大100,000行</li><li>文件大小不超过 200MB</li></ul><p><strong>text_type</strong> <code>string</code><strong>可选</strong></p><p>文本转换为向量后可以应用于检索、聚类、分类等下游任务，对检索这类非对称任务为了达到更好的检索效果建议区分查询文本（query）和底库文本（document）类型；聚类、分类等对称任务可以不用特殊指定，采用系统默认值<code>document</code>即可。</p></td><td><a id="sec-tabs-4"></a><section><a id="同步调用"></a><section><a id="同步调用-h4"></a><h4>同步调用</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

# 提交批处理任务并等待完成（任务失败或被取消时抛出 DashScopeError）
job = client.embeddings.jobs.create(
    model=&quot;text-embedding-async-v1&quot;,
    file_url=&quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241016/nigwvr/text_embedding_file.txt&quot;,
    text_type=&quot;document&quot;)
result = client.embeddings.jobs.wait(job)
print(result)
print(result.result_url)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>import com.alibaba.dashscope.embeddings.BatchTextEmbedding;
import com.alibaba.dashscope.embeddings.BatchTextEmbeddingParam;
import com.alibaba.dashscope.embeddings.BatchTextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.task.AsyncTaskListResult;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
        // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
    public static void basicCall() throws ApiException, NoApiKeyException {
        BatchTextEmbeddingParam param = BatchTextEmbeddingParam.builder()
                .model(BatchTextEmbedding.Models.TEXT_EMBEDDING_ASYNC_V1)
                .url(&quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241016/nigwvr/text_embedding_file.txt&quot;)
                .textType(BatchTextEmbeddingParam.TextType.DOCUMENT)
                .build();
        BatchTextEmbedding textEmbedding = new BatchTextEmbedding();
        BatchTextEmbeddingResult result = textEmbedding.call(param);
        System.out.println(result);
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
        try {
            basicCall();
        } catch (ApiException | NoApiKeyException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div></div></section><a id="异步调用"></a><section><a id="异步调用-h4"></a><h4>异步调用</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

# 创建异步任务
def create_async_task():
    job = client.embeddings.jobs.create(
        model=&quot;text-embedding-async-v1&quot;,
        file_url=&quot;https://modelscope.oss-cn-beijing.aliyuncs.com/resource/text_embedding_file.txt&quot;,
        text_type=&quot;document&quot;)
    print(job.task_id, job.status)
    return job

# 获取异步任务信息
def fetch_task_status(job):
    snapshot = client.embeddings.jobs.fetch(job.task_id)
    print(snapshot.status)

# 等待异步任务结束，内部封装指数退避轮询，会一直等待任务结束；任务失败或被取消时抛出 DashScopeError
def wait_task(job):
    done = client.embeddings.jobs.wait(job)
    print(done.status, done.result_url)

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(job):
    snapshot = client.embeddings.jobs.cancel(job.task_id)
    print(snapshot.status)

if __name__ == '__main__':
    try:
        job = create_async_task()
        fetch_task_status(job)
        wait_task(job)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)
</code></pre></div><a id="fig-code-group-2-java-tab"></a>Java<div><a id="code-code-group-2-java"></a><pre class="language-java"><code>import com.alibaba.dashscope.embeddings.BatchTextEmbedding;
import com.alibaba.dashscope.embeddings.BatchTextEmbeddingParam;
import com.alibaba.dashscope.embeddings.BatchTextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.task.AsyncTaskListResult;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
        // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;

    /**创建批处理任务*/
    public static BatchTextEmbeddingResult createTask() throws ApiException, NoApiKeyException {
        BatchTextEmbeddingParam param = BatchTextEmbeddingParam.builder()
                .model(BatchTextEmbedding.Models.TEXT_EMBEDDING_ASYNC_V1)
                .url(&quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241016/nigwvr/text_embedding_file.txt&quot;)
                .textType(BatchTextEmbeddingParam.TextType.DOCUMENT)
                .build();
        BatchTextEmbedding textEmbedding = new BatchTextEmbedding();
        return textEmbedding.asyncCall(param);

    }

    /**获取任务状态*/
    public static void fetchTaskStatus(BatchTextEmbeddingResult result)
            throws ApiException, NoApiKeyException {
        BatchTextEmbedding textEmbedding = new BatchTextEmbedding();
        result = textEmbedding.fetch(result, null);
        System.out.println(result);
    }

    /**等待任务结束，wait内部封装了轮询逻辑，会一直等待任务结束*/
    public static void waitTask(BatchTextEmbeddingResult result)
            throws ApiException, NoApiKeyException {
        BatchTextEmbedding textEmbedding = new BatchTextEmbedding();
        result = textEmbedding.wait(result, null);
        System.out.println(result);
    }

    /**取消任务，只能取消处于pending状态的任务*/
    public static void cancelTask(BatchTextEmbeddingResult result)
            throws ApiException, NoApiKeyException {
        BatchTextEmbedding textEmbedding = new BatchTextEmbedding();
        result = textEmbedding.cancel(result, null);
        System.out.println(result);
    }

    /**查询已经提交的任务*/
    public static void list() throws ApiException, NoApiKeyException {
        AsyncTaskListParam param = AsyncTaskListParam.builder().pageNo(1).pageSize(20).build();
        BatchTextEmbedding textEmbedding = new BatchTextEmbedding();
        AsyncTaskListResult result = textEmbedding.list(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            BatchTextEmbeddingResult task = createTask();
            fetchTaskStatus(task);
            waitTask(task);
            // list();
        } catch (ApiException | NoApiKeyException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="e9c6861476m70"></a><h4>响应参数</h4><blockquote><p>Python SDK 2.0 中，<code>client.embeddings.jobs.create</code> / <code>wait</code> / <code>fetch</code> 返回 Job 对象，以下为其字段口径。</p></blockquote><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>task_id</strong><code>string</code></p><p>任务唯一标识。可用于任务明细溯源和问题排查。</p><p><strong>status</strong><code>string</code></p><p>任务状态</p><ul><li>SUCCEEDED: 任务执行成功</li><li>FAILED: 任务执行失败</li><li>CANCELED： 任务被取消</li><li>PENDING：任务排队中</li><li>SUSPENDED：任务挂起</li><li>RUNNING：任务处理中</li></ul><p><strong>result_url</strong><code>string</code></p><p>包含Embedding结果的url，任务执行失败时返回参数中该参数为空。可通过 <code>job.result_url</code> 读取。</p><p><strong>code</strong><code>string</code></p><p>任务执行失败，表示失败原因（对应异常的 <code>e.code</code>），成功执行时响应中不会包含此参数。详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>任务执行失败，表示失败详细信息（对应异常的 <code>e.message</code>），成功执行时响应中不会包含此参数。</p><strong>调用失败</strong><p>请求失败或任务执行失败时，SDK 抛出 <strong>DashScopeError</strong>，可通过 <code>e.status_code</code>（HTTP返回码）、<code>e.code</code>（错误码）、<code>e.message</code>（错误信息）、<code>e.request_id</code>（请求唯一标识）获取失败详情。详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>usage</strong><code>object</code></p><strong>属性</strong><a id="accordion-details"></a><section><p>Details</p><div><p><strong>total_tokens</strong> <code>integer</code></p><p>本次请求输入内容的Token数目，算法的计量是根据用户输入字符串被模型Tokenizer解析之后对应的Token数目来进行。</p></div></section></td><td><a id="sec-tabs-5"></a><section><a id="同步调用-2"></a><section><a id="同步调用-2-h4"></a><h4>同步调用</h4><a id="sec-tabs-6"></a><section><a id="成功响应-2"></a><section><a id="成功响应-2-h4"></a><h4>成功响应</h4><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;&lt;Your Request ID&gt;&quot;,
    &quot;task_id&quot;: &quot;&lt;Your Task ID&gt;&quot;,
    &quot;status&quot;: &quot;SUCCEEDED&quot;,
    &quot;result_url&quot;: &quot;&lt;包含输出结果的url&gt;&quot;,
    &quot;usage&quot;: {
        &quot;total_tokens&quot;: 384
    }
}
</code></pre></section><a id="异常响应-2"></a><section><a id="异常响应-2-h4"></a><h4>异常响应</h4><strong>请求失败</strong><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;&lt;Your Request ID&gt;&quot;
}
</code></pre><strong>任务执行失败</strong><p>任务处于 FAILED 终态时，<code>jobs.wait</code> / <code>jobs.fetch</code> 将抛出 <code>DashScopeError</code>，以下为对应的任务快照内容：</p><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;&lt;Your Request ID&gt;&quot;,
    &quot;task_id&quot;: &quot;&lt;Your Task ID&gt;&quot;,
    &quot;status&quot;: &quot;FAILED&quot;,
    &quot;code&quot;: &quot;InvalidFile.TypeNotTxt&quot;,
    &quot;message&quot;: &quot;File type should be txt&quot;
}
</code></pre></section></section></section><a id="异步调用-2"></a><section><a id="异步调用-2-h4"></a><h4>异步调用</h4><a id="sec-tabs-7"></a><section><a id="成功响应-3"></a><section><a id="成功响应-3-h4"></a><h4>成功响应</h4><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;&lt;Your Request ID&gt;&quot;,
    &quot;task_id&quot;: &quot;&lt;Your Task ID&gt;&quot;,
    &quot;status&quot;: &quot;SUCCEEDED&quot;,
    &quot;result_url&quot;: &quot;&lt;包含输出结果的url&gt;&quot;,
    &quot;usage&quot;: {
        &quot;total_tokens&quot;: 384
    }
}
</code></pre></section><a id="异常响应-3"></a><section><a id="异常响应-3-h4"></a><h4>异常响应</h4><strong>请求失败</strong><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;&lt;Your Request ID&gt;&quot;
}
</code></pre><strong>任务执行失败</strong><p>任务处于 FAILED 终态时，<code>jobs.wait</code> / <code>jobs.fetch</code> 将抛出 <code>DashScopeError</code>，以下为对应的任务快照内容：</p><a id="code-block-13"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;&lt;Your Request ID&gt;&quot;,
    &quot;task_id&quot;: &quot;&lt;Your Task ID&gt;&quot;,
    &quot;status&quot;: &quot;FAILED&quot;,
    &quot;code&quot;: &quot;InvalidFile.TypeNotTxt&quot;,
    &quot;message&quot;: &quot;File type should be txt&quot;
}
</code></pre></section></section></section></section></td></tr></tbody></table>

<a id="常见问题"></a>

<a id="b03b052639hkc"></a>

## 常见问题

<a id="输入文件限制"></a>

<a id="49c9b59f66abi"></a>

### 输入文件限制

-   输入文件需为 **UTF-8 编码的文本文件**，每行包含一个需要计算文字向量的字符串。系统会逐行处理每个输入，并在最终输出文件中返回对应的行号和生成的 embedding 结果。
-   单个文件大小不得超过 **200MB**。
-   单次请求的文本行数不得超过 **100,000 行**。
-   每行内容的长度不得超过 **2,048 Token**。
-   空行（即不包含任何字符的行）会被系统自动跳过，不会计算其文字向量。然而，为了便于结果对应，输出文件中仍会保留这些空行的行号。

<a id="输出文件说明"></a>

<a id="43b0a60e7fzap"></a>

### 输出文件说明

-   当任务成功完成后，提交的输入数据将被转换为向量结果，并存储在输出文件中。为了节省存储空间并方便下载，输出文件会被压缩为 `.gz` 格式。下载至本地后可解压缩以获取对应的文本输出文件。
-   任务数据（如任务状态、处理结果URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存包含任务结果的输出文件。
-   经过模型向量化后输出的文件是一个 jsonl 格式文件，即每一行都是一个完整的 json 结构，包含对应输入文件特定行的向量化输出。

<a id="错误码"></a>

<a id="7cfb84ee806h3"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="基础限流"></a>

<a id="6d04415aa6jdb"></a>

## 基础限流

为了保证用户调用模型的公平性，通用文本向量对用户设置了基础限流。如果超出调用限制，用户的API请求将因为限流控制而失败，用户需要等待一段时间待满足限流条件后方能再次调用。各模型详细限流条件请参见[限流](../../../model-user-guide/get-started-with-models/rate-limit.md)。
