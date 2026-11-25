# 同步接口API详情

通用文本向量模型可将文本数据转换为数值向量，用于语义搜索、推荐、聚类、分类等下游任务。

<a id="模型概览"></a>

<a id="0e41425c577u4"></a>

## 模型概览

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>向量维度</strong></th><th><strong>最大行数</strong></th><th><p><strong>单行最大</strong><a href="https://help.aliyun.com/zh/model-studio/billing-for-model-studio">Token</a><strong>数</strong></p></th><th><strong>单价（每千输入Token）</strong></th><th><strong>支持语种</strong></th><th><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>2560、2,048、1,536、1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.0005元</p><p><a href="../../toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.00025元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p></td><td><p>100万Token</p><p>有效期：百炼开通后90天内</p></td></tr><tr><td><p>qwen3.7-text-embedding-flash</p></td><td><p>1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.000125元</p><p><a href="../../toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.000063元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p></td><td><p>100万Token</p><p>有效期：百炼开通后90天内</p></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p>属于<a href="https://qwenlm.github.io/zh/blog/qwen3-embedding/">Qwen3-Embedding</a>系列</p></blockquote></td><td><p>2,048、1,536、1,024（默认）、768、512、256、128、64</p></td><td rowspan="2"><p>10</p></td><td rowspan="2"><p>8,192</p></td><td rowspan="2"><p>0.0005元</p><p><a href="../../toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.00025元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种及多种编程语言</p></td><td><p>100万Token</p><p>有效期：百炼开通后90天内</p></td></tr><tr><td><p>text-embedding-v3</p></td><td><p>1,024（默认）、768、512、256、128或64</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种</p></td><td><p>无免费额度</p></td></tr><tr><td><p>text-embedding-v2</p></td><td rowspan="2"><p>1,536</p></td><td rowspan="2"><p>25</p></td><td rowspan="2"><p>2,048</p></td><td rowspan="2"><p>0.0007元</p><p><a href="../../toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.00035元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语</p></td><td rowspan="2"><p>无免费额度</p></td></tr><tr><td><p>text-embedding-v1</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>向量维度</strong></th><th><strong>最大行数</strong></th><th><p><strong>单行最大</strong>Token<strong>数</strong></p></th><th><strong>单价（每千输入Token）</strong></th><th><strong>支持语种</strong></th><th><strong>免费额度</strong></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>2560、2,048、1,536、1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.000525元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p></td><td><p>无免费额度</p></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p>属于<a href="https://qwenlm.github.io/zh/blog/qwen3-embedding/">Qwen3-Embedding</a>系列</p></blockquote></td><td><p>2,048、1,536、1,024（默认）、768、512、256、128、64</p></td><td rowspan="2"><p>10</p></td><td rowspan="2"><p>8,192</p></td><td rowspan="2"><p>0.000514元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种及多种编程语言</p></td><td><p>无免费额度</p></td></tr><tr><td><p>text-embedding-v3</p></td><td><p>1,024（默认）、768、512</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种</p></td><td><p>无免费额度</p></td></tr></tbody></table>

关于模型限流，请参考[限流](../../../model-user-guide/get-started-with-models/rate-limit.md#953ddcd76495l)。

<a id="前提条件"></a>

<a id="9d4c1e7735hni"></a>

## 前提条件

若熟悉OpenAI生态，可使用兼容API快速迁移；DashScope API则提供更丰富的独有特性。请根据您的需求选择。

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](../../preparations/install-sdk.md)。

<a id="openai兼容"></a>

<a id="f4e8c45964o4x"></a>

## OpenAI兼容

<a id="sec-tabs-2"></a>

<a id="公共云"></a>

<a id="公共云-h4"></a>

#### 公共云

**使用SDK调用时需配置的base\_url：**`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

**使用HTTP方式调用时需配置的endpoint：**`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="d150fab3e6rgl"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>必选</strong></p><p>调用的模型名称，参考<a href="text-embedding-synchronous-api.md#0e41425c577u4">模型概览</a>表格中的模型名称进行选择。</p><p><strong>input</strong><code>array&lt;string&gt; 或 string 或 file</code><strong>必选</strong></p><p>输入待处理的文本。可以是字符串（string）、字符串列表（array）或文件（file）。不同模型版本支持的文本长度和批量大小不同，具体如下：</p><ul><li><strong>qwen3.7-text-embedding 模型：</strong><ul><li><strong>输入为字符串</strong>：最长支持 <strong>128,000</strong> Token。</li><li><strong>输入为字符串列表或文件</strong>：最多支持 <strong>20</strong> 条（行），每条（行）最长支持 <strong>128,000</strong> Token。</li></ul></li><li><strong>text-embedding-v3 / v4 模型：</strong><ul><li><strong>输入为字符串</strong>：最长支持 <strong>8,192</strong> Token。</li><li><strong>输入为字符串列表或文件</strong>：最多支持 <strong>10</strong> 条（行），每条（行）最长支持 <strong>8,192</strong> Token。</li></ul></li><li><strong>text-embedding-v1 / v2 模型：</strong><ul><li><strong>输入为字符串</strong>：最长支持 <strong>2,048</strong> Token。</li><li><strong>输入为字符串列表或文件</strong>：最多支持 <strong>25</strong> 条（行），每条（行）最长支持 <strong>2,048</strong> Token。</li></ul></li></ul><p><strong>dimensions</strong> <code>integer</code> <strong>可选</strong></p><p>指定的向量维度，必须为以下值之一：<code>2560（仅适用于qwen3.7-text-embedding）、</code>2048（仅适用于<code>text-embedding-v4</code>）、1536（仅适用于<code>text-embedding-v4</code>）1024、768、512、256、128 或 64，默认值为1024。</p><p><strong>encoding_format</strong> <code>string</code> <strong>可选</strong></p><p>用于控制返回的Embedding格式，入参支持<code>float</code>和<code>base64</code>，出参的Embedding数据也支持<code>float</code>和<code>base64</code>两种格式。实际返回格式取决于请求路由到的网关：</p><ul><li><p><strong>老网关</strong>：无论<code>encoding_format</code>设置为<code>float</code>还是<code>base64</code>，均只返回<code>float</code>类型数据，不支持输出<code>base64</code>数据。</p></li><li><p><strong>新网关</strong>：</p><ul><li><strong>短请求</strong>：按<code>encoding_format</code>设置的格式返回数据。</li><li><strong>长请求</strong>：内部路由到老网关，仅返回<code>float</code>类型数据。</li></ul></li></ul></td><td><a id="sec-tabs-3"></a><section><a id="输入字符串"></a><section><a id="输入字符串-h4"></a><h4>输入字符串</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    # 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
)

completion = client.embeddings.create(
    model=&quot;qwen3.7-text-embedding&quot;,
    input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
    dimensions=1024, # 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
    encoding_format=&quot;float&quot;
)

print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.EmbeddingCreateParams;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
                .baseUrl(&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;)
                .build();

        // 创建向量化请求参数
        EmbeddingCreateParams params = EmbeddingCreateParams.builder()
                .model(&quot;qwen3.7-text-embedding&quot;)
                .input(EmbeddingCreateParams.Input.ofString(&quot;衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买&quot;))
                // 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
                .dimensions(1024)
                .build();

        try {
            // 发送请求并获取响应
            CreateEmbeddingResponse response = client.embeddings().create(params);
            System.out.println(response);
        } catch (Exception e) {
            System.err.println(&quot;请求出错，请查看错误码对照网页：&quot;);
            System.err.println(&quot;https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio?spm=a2c4g.11186623.help-menu-2400256.d_0_17_0.18733a66lTrcHv#1c38f58abfcml&quot;);
            System.err.println(&quot;错误详情：&quot; + e.getMessage());
            e.printStackTrace();
        }
    }
}
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
    &quot;input&quot;: &quot;风急天高猿啸哀，渚清沙白鸟飞回，无边落木萧萧下，不尽长江滚滚来&quot;,
    &quot;dimensions&quot;: 1024,
    &quot;encoding_format&quot;: &quot;float&quot;
}'
</code></pre></div><a id="fig-code-group-dashscope-cli-tab"></a>dashscope CLI<div><a id="code-code-group-dashscope-cli"></a><pre class="language-bash"><code># 通过 dashscope 命令行调用
export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
dashscope embeddings create -m text-embedding-v3 -i &quot;你好世界&quot;
</code></pre></div></div><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../../preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div></section><a id="输入字符串列表"></a><section><a id="输入字符串列表-h4"></a><h4>输入字符串列表</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    # 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
)

completion = client.embeddings.create(
    model=&quot;qwen3.7-text-embedding&quot;,
    input=['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来'],
    dimensions=1024,# 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
    encoding_format=&quot;float&quot;
)

print(completion.model_dump_json())
</code></pre></div><a id="fig-code-group-2-java-tab"></a>Java<div><a id="code-code-group-2-java"></a><pre class="language-java"><code>import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.EmbeddingCreateParams;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
                .baseUrl(&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;)
                .build();

        // 创建输入字符串列表
        List&lt;String&gt; inputList = Arrays.asList(
            &quot;风急天高猿啸哀&quot;,
            &quot;渚清沙白鸟飞回&quot;,
            &quot;无边落木萧萧下&quot;,
            &quot;不尽长江滚滚来&quot;
        );

        // 存储所有响应的列表
        List&lt;CreateEmbeddingResponse&gt; responses = new ArrayList&lt;&gt;();

        // 循环处理每个字符串
        for (String text : inputList) {
            try {
                // 创建向量化请求参数
                EmbeddingCreateParams params = EmbeddingCreateParams.builder()
                        .model(&quot;qwen3.7-text-embedding&quot;)
                        .input(EmbeddingCreateParams.Input.ofString(text))
                        // 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
                        .dimensions(1024)
                        .build();

                // 发送请求并获取响应
                CreateEmbeddingResponse response = client.embeddings().create(params);
                responses.add(response);
                System.out.println(&quot;处理文本: &quot; + text);
                System.out.println(&quot;向量化结果: &quot; + response);
                System.out.println(&quot;------------------------&quot;);
            } catch (Exception e) {
                System.err.println(&quot;处理文本时出错: &quot; + text);
                System.err.println(&quot;错误详情：&quot; + e.getMessage());
                e.printStackTrace();
            }
        }

        // 打印总结信息
        System.out.println(&quot;\n总共处理了 &quot; + responses.size() + &quot; 个文本&quot;);
    }
}
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
    &quot;input&quot;: [
        &quot;风急天高猿啸哀&quot;,
        &quot;渚清沙白鸟飞回&quot;,
        &quot;无边落木萧萧下&quot;,
        &quot;不尽长江滚滚来&quot;
        ],
    &quot;dimensions&quot;: 1024,
    &quot;encoding_format&quot;: &quot;float&quot;
}'
</code></pre></div></div></section><a id="输入文件"></a><section><a id="输入文件-h4"></a><h4>输入文件</h4><a id="sec-tabs-4"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><a id="code-block"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    # 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
)
# 确保将 'texts_to_embedding.txt' 替换为您自己的文件名或路径
with open('texts_to_embedding.txt', 'r', encoding='utf-8') as f:
    completion = client.embeddings.create(
        model=&quot;qwen3.7-text-embedding&quot;,
        input=f,
        dimensions=1024,# 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
        encoding_format=&quot;float&quot;
    )
print(completion.model_dump_json())
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><a id="code-block-2"></a><pre class="language-java"><code>import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.EmbeddingCreateParams;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
                .baseUrl(&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;)
                .build();

        // 确保将 'texts_to_embedding.txt' 替换为您自己的文件名或绝对路径
        String filePath = &quot;/src/main/java/org/example/text_to_embedding.txt&quot;;

        try {
            // 读取文件内容
            StringBuilder fileContent = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    fileContent.append(line).append(&quot;\n&quot;);
                }
            }

            // 创建向量化请求参数
            EmbeddingCreateParams params = EmbeddingCreateParams.builder()
                    .model(&quot;qwen3.7-text-embedding&quot;)
                    .input(EmbeddingCreateParams.Input.ofString(fileContent.toString()))
                    // 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
                    .dimensions(1024)
                    .build();

            // 发送请求并获取响应
            CreateEmbeddingResponse response = client.embeddings().create(params);
            System.out.println(response);

        } catch (IOException e) {
            System.err.println(&quot;读取文件时出错：&quot; + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println(&quot;请求出错，请查看错误码对照网页：&quot;);
            System.err.println(&quot;https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio?spm=a2c4g.11186623.help-menu-2400256.d_0_17_0.18733a66lTrcHv#1c38f58abfcml&quot;);
            System.err.println(&quot;错误详情：&quot; + e.getMessage());
            e.printStackTrace();
        }
    }
}
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><blockquote><p>确保将 'texts_to_embedding.txt' 替换为您自己的文件名或路径</p></blockquote><a id="code-block-3"></a><pre class="language-bash"><code>FILE_CONTENT=$(cat texts_to_embedding.txt | jq -Rs .)
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
    &quot;input&quot;: ['&quot;$FILE_CONTENT&quot;'],
    &quot;dimensions&quot;: 1024,
    &quot;encoding_format&quot;: &quot;float&quot;
}'
</code></pre></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="c451676492bm7"></a><h3>响应对象</h3><p><strong>data</strong><code>array</code></p><p>任务输出信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>embedding</strong><code>list</code></p><p>本次调用返回object对象的value，类型是元素为float数据的数组，包含具体Embedding向量。</p><p><strong>index</strong><code>integer</code></p><p>本结构中的算法结果对应的输入文字在输入数组中的索引值。</p><p><strong>object</strong><em>string</em></p><p>本次调用返回的object对象类型，默认为embedding。</p></div></section><p><strong>model</strong><code>string</code></p><p>本次调用的模型名。</p><p><strong>object</strong><em>string</em></p><p>本次调用返回的data类型，默认为list。</p><p><strong>usage</strong><code>object</code></p><p>本次请求的 Token 用量。<code>qwen3.7-text-embedding-flash</code> 返回 <code>prompt_tokens</code> 和 <code>total_tokens</code>；其他已上线的文本向量模型仅返回 <code>total_tokens</code>。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>prompt_tokens</strong><em>integer</em></p><p>仅 <code>qwen3.7-text-embedding-flash</code> 返回。表示本次请求输入内容的 Token 总数，取值与 <code>total_tokens</code> 相同。</p><p><strong>total_tokens</strong> <em>integer</em></p><p>本次请求消耗的 Token 总数，用于计量计费和审计。Token 数目按输入字符串被模型 Tokenizer 解析后的结果统计，与自行估算的字符数或词数可能不一致。</p></div></section><p><strong>id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-qwen3-7-text-embedding-成功响应-tab"></a>qwen3.7-text-embedding 成功响应<div><a id="code-code-group-3-qwen3-7-text-embedding-成功响应"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;embedding&quot;: [
        -0.0695386752486229, 0.030681096017360687, ...
      ],
      &quot;index&quot;: 0,
      &quot;object&quot;: &quot;embedding&quot;
    },
    ...
    {
      &quot;embedding&quot;: [
        -0.06348952651023865, 0.060446035116910934, ...
      ],
      &quot;index&quot;: 5,
      &quot;object&quot;: &quot;embedding&quot;
    }
  ],
  &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
  &quot;object&quot;: &quot;list&quot;,
  &quot;usage&quot;: {
    &quot;total_tokens&quot;: 184
  },
  &quot;id&quot;: &quot;73591b79-d194-9bca-8bb5-xxxxxxxxxxxx&quot;
}
</code></pre></div><a id="fig-code-group-3-qwen3-7-text-embedding-flash-成功响应-tab"></a>qwen3.7-text-embedding-flash 成功响应<div><a id="code-code-group-3-qwen3-7-text-embedding-flash-成功响应"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;embedding&quot;: [-0.0695386752486229, 0.030681096017360687, ...],
      &quot;index&quot;: 0,
      &quot;object&quot;: &quot;embedding&quot;
    }
  ],
  &quot;model&quot;: &quot;qwen3.7-text-embedding-flash&quot;,
  &quot;object&quot;: &quot;list&quot;,
  &quot;usage&quot;: {
    &quot;prompt_tokens&quot;: 184,
    &quot;total_tokens&quot;: 184
  },
  &quot;id&quot;: &quot;73591b79-d194-9bca-8bb5-xxxxxxxxxxxx&quot;
}
</code></pre></div><a id="fig-code-group-3-异常响应-tab"></a>异常响应<div><a id="code-code-group-3-异常响应"></a><pre class="language-json"><code>{
    &quot;error&quot;: {
        &quot;message&quot;: &quot;Incorrect API key provided. &quot;,
        &quot;type&quot;: &quot;invalid_request_error&quot;,
        &quot;param&quot;: null,
        &quot;code&quot;: &quot;invalid_api_key&quot;
    }
}
</code></pre></div></div></td></tr></tbody></table>

<a id="dashscope"></a>

<a id="69cac67a477k2"></a>

## DashScope

<a id="sec-tabs-5"></a>

<a id="公共云-2"></a>

<a id="公共云-2-h4"></a>

#### 公共云

**使用SDK调用时需配置的base\_url：**https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1

**使用HTTP方式调用时需配置的endpoint：**POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>必选</strong></p><p>调用的模型，参考<a href="text-embedding-synchronous-api.md#0e41425c577u4">模型概览</a>表格中的模型名称进行选择。</p><p><strong>input</strong><code>string</code><em>或</em><code>array&lt;string&gt;</code><strong>必选</strong></p><p>输入待处理的文本。可以是字符串（string）、字符串列表（array）或文件（file）。不同模型版本支持的文本长度和批量大小不同，具体如下：</p><ul><li><strong>qwen3.7-text-embedding、qwen3.7-text-embedding-flash 模型：</strong><ul><li><strong>输入为字符串</strong>：最长支持 <strong>128,000</strong> Token。</li><li><strong>输入为字符串列表或文件</strong>：最多支持 <strong>20</strong> 条（行），每条（行）最长支持 <strong>128,000</strong> Token。</li></ul></li><li><strong>text-embedding-v3 / v4 模型：</strong><ul><li><strong>输入为字符串</strong>：最长支持 <strong>8,192</strong> Token。</li><li><strong>输入为字符串列表或文件</strong>：最多支持 <strong>10</strong> 条（行），每条（行）最长支持 <strong>8,192</strong> Token。</li></ul></li><li><strong>text-embedding-v1 / v2 模型：</strong><ul><li><strong>输入为字符串</strong>：最长支持 <strong>2,048</strong> Token。</li><li><strong>输入为字符串列表或文件</strong>：最多支持 <strong>25</strong> 条（行），每条（行）最长支持 <strong>2,048</strong> Token。</li></ul></li></ul><p><strong>text_type</strong> <code>string</code><strong>可选</strong></p><blockquote><p>通过 HTTP 调用时，请将 <strong>text_type</strong>放入parameters对象中。</p></blockquote><p>文本转换为向量后可以应用于检索、聚类、分类等下游任务，对检索这类非对称任务为了达到更好的检索效果建议区分查询文本（query）和底库文本（document）类型，入库、聚类、分类等对称任务可以不用特殊指定，采用系统默认值<code>document</code>即可。</p><p><strong>dimension</strong> <code>integer</code> <strong>可选</strong></p><blockquote><p>通过 HTTP 调用时，请将 <strong>dimension</strong>放入parameters对象中。</p></blockquote><p>指定的向量维度，必须为以下值之一：<code>2560（仅适用于qwen3.7-text-embedding）、</code>2048（仅适用于<code>text-embedding-v4</code>）、1536（仅适用于<code>text-embedding-v4</code>）1024、768、512、256、128 或 64，默认值为1024。</p><p><strong>output_type</strong> <code>string</code> <strong>可选</strong></p><blockquote><p>通过 HTTP 调用时，请将 <strong>output_type</strong>放入parameters对象中。</p></blockquote><p>用户指定输出离散向量表示只适用于<code>qwen3.7-text-embedding、``text-embedding-v3</code>与<code>text-embedding-v4</code>模型，取值在dense、sparse、dense&amp;sparse之间，默认取dense，只输出连续向量。稀疏向量输出（<code>sparse</code>和<code>dense&amp;amp;sparse</code>）仅支持通过 DashScope 接口调用。</p><p><strong>instruct</strong> <code>string</code> <strong>可选</strong></p><p>添加自定义任务说明，可用于指导模型理解查询意图。建议使用英文撰写，通常可带来约 1%–5% 的效果提升。</p><p>该参数仅在 <code>text_type</code> 取值为 <code>query</code> 时生效，并按输入文本的条数计入 Token 用量。<code>text_type</code> 取值为 <code>document</code> 或未设置 <code>text_type</code> 时，该参数不生效，也不计入 Token 用量。</p></td><td><a id="sec-tabs-6"></a><section><a id="输入字符串-2"></a><section><a id="输入字符串-2-h4"></a><h4>输入字符串</h4><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>Python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

resp = client.embeddings.create(
    model=&quot;qwen3.7-text-embedding&quot;,
    input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
    dimension=1024,  # 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
    output_type=&quot;dense&amp;sparse&quot;
)

print(resp)
</code></pre></div><a id="fig-code-group-4-java-tab"></a>Java<div><a id="code-code-group-4-java"></a><pre class="language-java"><code>import java.util.Arrays;
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

/**
 * 千问文本向量模型调用示例
 */
public final class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
        try {
            // 构建请求参数
            TextEmbeddingParam param = TextEmbeddingParam
                    .builder()
                    .model(&quot;qwen3.7-text-embedding&quot;)  // 使用text-embedding-v4模型
                    .texts(Arrays.asList(&quot;衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买&quot;))  // 输入文本
                    .parameter(&quot;dimension&quot;, 1024)  // 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
                    .build();

            // 创建模型实例并调用
            TextEmbedding textEmbedding = new TextEmbedding();
            TextEmbeddingResult result = textEmbedding.call(param);

            // 输出结果
            System.out.println(result);

        } catch (ApiException | NoApiKeyException e) {
            System.out.println(&quot;调用失败：&quot; + e.getMessage());
        }
    }
}
</code></pre></div><a id="fig-code-group-4-curl-tab"></a>curl<div><a id="code-code-group-4-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
    &quot;input&quot;: {
        &quot;texts&quot;: [
        &quot;风急天高猿啸哀，渚清沙白鸟飞回，无边落木萧萧下，不尽长江滚滚来&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;dimension&quot;: 1024,
        &quot;output_type&quot;: &quot;dense&quot;
    }
}'
</code></pre></div></div></section><a id="输入字符串列表-2"></a><section><a id="输入字符串列表-2-h4"></a><h4>输入字符串列表</h4><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>Python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

DASHSCOPE_MAX_BATCH_SIZE = 10

inputs = ['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来']

result = None
batch_counter = 0
try:
    for i in range(0, len(inputs), DASHSCOPE_MAX_BATCH_SIZE):
        batch = inputs[i:i + DASHSCOPE_MAX_BATCH_SIZE]
        resp = client.embeddings.create(
            model=&quot;qwen3.7-text-embedding&quot;,
            input=batch,
            dimension=1024  # 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
        )
        if result is None:
            result = resp
        else:
            for emb in resp.embeddings:
                emb.index += batch_counter
                result.embeddings.append(emb)
            result.usage.total_tokens += resp.usage.total_tokens
        batch_counter += len(batch)
except DashScopeError as e:
    print(f&quot;HTTP返回码：{e.status_code}&quot;)
    print(f&quot;错误码：{e.code}&quot;)
    print(f&quot;错误信息：{e.message}&quot;)
    print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)

print(result)
</code></pre></div><a id="fig-code-group-5-java-tab"></a>Java<div><a id="code-code-group-5-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.List;
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.embeddings.TextEmbeddingResultItem;
import com.alibaba.dashscope.utils.Constants;

public final class Main {
    private static final int DASHSCOPE_MAX_BATCH_SIZE = 10;

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
        List&lt;String&gt; inputs = Arrays.asList(
                &quot;风急天高猿啸哀&quot;,
                &quot;渚清沙白鸟飞回&quot;,
                &quot;无边落木萧萧下&quot;,
                &quot;不尽长江滚滚来&quot;
        );

        TextEmbeddingResult result = null;
        int batchCounter = 0;

        for (int i = 0; i &lt; inputs.size(); i += DASHSCOPE_MAX_BATCH_SIZE) {
            List&lt;String&gt; batch = inputs.subList(i, Math.min(i + DASHSCOPE_MAX_BATCH_SIZE, inputs.size()));
            TextEmbeddingParam param = TextEmbeddingParam.builder()
                    .model(&quot;qwen3.7-text-embedding&quot;)
                    .texts(batch)
                    .parameter(&quot;dimension&quot;, 1024)  // 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
                    .build();

            TextEmbedding textEmbedding = new TextEmbedding();
            try {
                TextEmbeddingResult resp = textEmbedding.call(param);
                if (resp != null) {
                    if (result == null) {
                        result = resp;
                    } else {
                        for (var emb : resp.getOutput().getEmbeddings()) {
                            emb.setTextIndex(emb.getTextIndex() + batchCounter);
                            result.getOutput().getEmbeddings().add(emb);
                        }
                        result.getUsage().setTotalTokens(result.getUsage().getTotalTokens() + resp.getUsage().getTotalTokens());
                    }
                } else {
                    System.out.println(resp);
                }
            } catch (ApiException | NoApiKeyException e) {
                e.printStackTrace();
            }
            batchCounter += batch.size();
        }

        System.out.println(result);
    }
}
</code></pre></div><a id="fig-code-group-5-curl-tab"></a>curl<div><a id="code-code-group-5-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
    &quot;input&quot;: {
        &quot;texts&quot;: [
          &quot;风急天高猿啸哀&quot;,
          &quot;渚清沙白鸟飞回&quot;,
          &quot;无边落木萧萧下&quot;,
          &quot;不尽长江滚滚来&quot;
        ]
    },
    &quot;parameters&quot;: {
          &quot;dimension&quot;: 1024,
          &quot;output_type&quot;: &quot;dense&quot;
    }
}'
</code></pre></div></div></section><a id="输入文件-2"></a><section><a id="输入文件-2-h4"></a><h4>输入文件</h4><a id="sec-tabs-7"></a><section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><a id="code-block-4"></a><pre class="language-python"><code>import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

with open('texts_to_embedding.txt', 'r', encoding='utf-8') as f:
    resp = client.embeddings.create(
        model=&quot;qwen3.7-text-embedding&quot;,
        input=f,
        dimension=1024 # 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
    )

    print(resp)
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><a id="code-block-5"></a><pre class="language-java"><code>import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public final class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
        try (BufferedReader reader = new BufferedReader(new FileReader(&quot;&lt;文件所来自的内容根的路径&gt;&quot;))) {
            StringBuilder content = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append(&quot;\n&quot;);
            }

            TextEmbeddingParam param = TextEmbeddingParam.builder()
                    .model(&quot;qwen3.7-text-embedding&quot;)
                    .text(content.toString())
                    .parameter(&quot;dimension&quot;, 1024)  // 指定向量维度（仅 qwen3.7-text-embedding、text-embedding-v3及 text-embedding-v4支持该参数）
                    .build();

            TextEmbedding textEmbedding = new TextEmbedding();
            TextEmbeddingResult result = textEmbedding.call(param);

            if (result != null) {
                System.out.println(result);
            } else {
                System.out.println(&quot;Failed to get embedding: &quot; + result);
            }
        } catch (IOException | ApiException | NoApiKeyException e) {
            e.printStackTrace();
        }
    }
}
</code></pre></section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><blockquote><p>确保将 'texts_to_embedding.txt' 替换为您自己的文件名或路径</p></blockquote><a id="code-block-6"></a><pre class="language-bash"><code>FILE_CONTENT=$(cat texts_to_embedding.txt | jq -Rs .)
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-embedding&quot;,
    &quot;input&quot;: {
        &quot;texts&quot;: ['&quot;$FILE_CONTENT&quot;']
    },
    &quot;parameters&quot;: {
        &quot;dimension&quot;: 1024,
        &quot;output_type&quot;: &quot;dense&quot;
    }
}'
</code></pre></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="e9c6861476m70"></a><h3>响应对象</h3><blockquote><p>Python SDK 2.0 中，<code>client.embeddings.create</code> 返回的响应对象字段如下（HTTP 接口返回的 JSON 中，<code>embeddings</code> 包裹在 <code>output</code> 内）。</p></blockquote><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>embeddings</strong><code>array</code></p><p>本次请求的算法输出内容，是一个由结构组成的数组，每一个数组中包含一个对应的输入 text 的算法输出内容。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>sparse_embedding</strong> <code>array</code></p><p>对应字符串的算法输出离散向量表示 （sparse embedding仅适用于<code>text-embedding-v3</code>与<code>text-embedding-v4</code>）。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>index</strong> <code>integer</code></p><p>词汇或字符在词汇表中的位置索引。</p><p><strong>value</strong> <code>float</code></p><p>表示该 <code>Token</code> 的权重或重要性分数，值越高，表示该 <code>Token</code> 在当前文本上下文中的重要性或相关性越大。</p><p><strong>token</strong> <code>string</code></p><p>实际的文本单元或词汇表中的词。</p></div></section><p><strong>embedding</strong> <code>array</code></p><p>对应字符串的算法输出连续向量表示 （dense embedding)。</p><p><strong>index</strong> <code>integer</code></p><p>本结构中的算法结果对应的输入文字在输入数组中的索引值。</p></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求的 Token 用量。<code>qwen3.7-text-embedding-flash</code> 返回 <code>prompt_tokens</code> 和 <code>total_tokens</code>；其他已上线的文本向量模型仅返回 <code>total_tokens</code>。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>prompt_tokens</strong> <code>integer</code></p><p>仅 <code>qwen3.7-text-embedding-flash</code> 返回。表示本次请求输入内容的 Token 总数，取值与 <code>total_tokens</code> 相同。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>本次请求消耗的 Token 总数，用于计量计费和审计。Token 数目按输入字符串被模型 Tokenizer 解析后的结果统计，与自行估算的字符数或词数可能不一致。</p><p>设置 <code>instruct</code> 且 <code>text_type</code> 取值为 <code>query</code> 时，<code>instruct</code> 会按输入文本的条数重复计入 Token 用量。</p></div></section><strong>调用失败</strong><p>调用失败时，SDK 抛出 <strong>DashScopeError</strong>，可通过 <code>e.status_code</code>（HTTP返回码）、<code>e.code</code>（错误码）、<code>e.message</code>（错误信息）、<code>e.request_id</code>（请求唯一标识）获取失败详情。详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-qwen3-7-text-embedding-成功响应-tab"></a>qwen3.7-text-embedding 成功响应<div><a id="code-code-group-6-qwen3-7-text-embedding-成功响应"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;1ba94ac8-e058-99bc-9cc1-7fdb37940a46&quot;,
    &quot;embeddings&quot;: [
      {
         &quot;index&quot;: 0,
         &quot;sparse_embedding&quot;:[
           {&quot;index&quot;:7149,&quot;value&quot;:0.829,&quot;token&quot;:&quot;风&quot;},
           .....
           {&quot;index&quot;:111290,&quot;value&quot;:0.9004,&quot;token&quot;:&quot;哀&quot;}],
         &quot;embedding&quot;: [-0.006929283495992422,-0.005336422007530928, ...]
      },
      {
         &quot;index&quot;: 1,
         &quot;sparse_embedding&quot;:[
           {&quot;index&quot;:246351,&quot;value&quot;:1.0483,&quot;token&quot;:&quot;渚&quot;},
           .....
           {&quot;index&quot;:2490,&quot;value&quot;:0.8579,&quot;token&quot;:&quot;回&quot;}],
         &quot;embedding&quot;: [-0.006929283495992422,-0.005336422007530928, ...]
      },
      {
         &quot;index&quot;: 2,
         &quot;sparse_embedding&quot;:[
           {&quot;index&quot;:3759,&quot;value&quot;:0.7065,&quot;token&quot;:&quot;无&quot;},
           .....
           {&quot;index&quot;:1130,&quot;value&quot;:0.815,&quot;token&quot;:&quot;下&quot;}],
         &quot;embedding&quot;: [-0.006929283495992422,-0.005336422007530928, ...]
      },
      {
         &quot;index&quot;: 3,
         &quot;sparse_embedding&quot;:[
           {&quot;index&quot;:562,&quot;value&quot;:0.6752,&quot;token&quot;:&quot;不&quot;},
           .....
           {&quot;index&quot;:1589,&quot;value&quot;:0.7097,&quot;token&quot;:&quot;来&quot;}],
         &quot;embedding&quot;: [-0.001945948973298072,-0.005336422007530928, ...]
      }
    ],
    &quot;usage&quot;:{
        &quot;total_tokens&quot;:27
    }
}
</code></pre></div><a id="fig-code-group-6-qwen3-7-text-embedding-flash-成功响应-tab"></a>qwen3.7-text-embedding-flash 成功响应<div><a id="code-code-group-6-qwen3-7-text-embedding-flash-成功响应"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;1ba94ac8-e058-99bc-9cc1-7fdb37940a46&quot;,
    &quot;embeddings&quot;: [
        {
            &quot;index&quot;: 0,
            &quot;embedding&quot;: [-0.006929283495992422, -0.005336422007530928, ...]
        }
    ],
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 27,
        &quot;total_tokens&quot;: 27
    }
}
</code></pre></div><a id="fig-code-group-6-异常响应-http-接口返回-tab"></a>异常响应（HTTP 接口返回）<div><a id="code-code-group-6-异常响应-http-接口返回"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;xxxxxxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
