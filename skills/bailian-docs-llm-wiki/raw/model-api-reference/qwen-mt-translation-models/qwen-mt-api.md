# Qwen-MT API参考

本文介绍通过OpenAI兼容接口 或 DashScopeAPI 调用 Qwen-MT 模型的输入与输出参数。

> 相关文档： [翻译能力（Qwen-MT）](../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md)

<a id="openai-兼容"></a>

<a id="d397bcc41eu3q"></a>

## OpenAI 兼容

<a id="sec-tabs"></a>

<a id="北京地域"></a>

<a id="北京地域-h4"></a>

#### 北京地域

SDK 调用配置的`base_url`为：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="新加坡地域"></a>

<a id="新加坡地域-h4"></a>

#### 新加坡地域

SDK 调用配置的`base_url`为：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="美国-弗吉尼亚-地域"></a>

<a id="美国-弗吉尼亚-地域-h4"></a>

#### 美国（弗吉尼亚）地域

SDK 调用配置的`base_url`：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

> 您需要已 [获取与配置 API Key](../preparations/get-api-key.md) 并 [配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) 。若通过OpenAI SDK进行调用，需要 [安装SDK](../preparations/install-sdk.md) 。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h3>请求体</h3></td><td rowspan="12"><a id="sec-tabs-2"></a><section><a id="基础使用"></a><section><a id="基础使用-h4"></a><h4>基础使用</h4><a id="sec-tabs-3"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><a id="code-block"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下是北京地域的base_url
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;我看到这个视频后没有笑&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;
}

completion = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    extra_body={
        &quot;translation_options&quot;: translation_options
    }
)
print(completion.choices[0].message.content)
</code></pre></section><a id="node-js"></a><section><a id="node-js-h4"></a><h4>Node.js</h4><a id="code-block-2"></a><pre class="language-javascript"><code>// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下是北京地域的base_url
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);
const completion = await openai.chat.completions.create({
    model: &quot;qwen-mt-plus&quot;,
    messages: [
        { role: &quot;user&quot;, content: &quot;我看到这个视频后没有笑&quot; }
    ],
    translation_options: {
        source_lang: &quot;Chinese&quot;,
        target_lang: &quot;English&quot;
    }
});
console.log(JSON.stringify(completion));
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen-mt-plus&quot;,
    &quot;messages&quot;: [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;看完这个视频我没有笑&quot;}],
    &quot;translation_options&quot;: {
      &quot;source_lang&quot;: &quot;auto&quot;,
      &quot;target_lang&quot;: &quot;English&quot;
      }
}'
</code></pre></section></section></section><a id="术语干预"></a><section><a id="术语干预-h4"></a><h4>术语干预</h4><a id="sec-tabs-4"></a><section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><a id="code-block-4"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下是北京地域的base_url
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;terms&quot;: [
        {
            &quot;source&quot;: &quot;生物传感器&quot;,
            &quot;target&quot;: &quot;biological sensor&quot;
        },
        {
            &quot;source&quot;: &quot;石墨烯&quot;,
            &quot;target&quot;: &quot;graphene&quot;
        },
        {
            &quot;source&quot;: &quot;化学元素&quot;,
            &quot;target&quot;: &quot;chemical elements&quot;
        },
        {
            &quot;source&quot;: &quot;身体健康状况&quot;,
            &quot;target&quot;: &quot;health status of the body&quot;
        }
    ]
}

completion = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    extra_body={
        &quot;translation_options&quot;: translation_options
    }
)
print(completion.choices[0].message.content)
</code></pre></section><a id="node-js-2"></a><section><a id="node-js-2-h4"></a><h4>Node.js</h4><a id="code-block-5"></a><pre class="language-javascript"><code>// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下是北京地域的base_url
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);
const completion = await openai.chat.completions.create({
    model: &quot;qwen-mt-plus&quot;,
    messages: [
        { role: &quot;user&quot;, content: &quot;而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。&quot; }
    ],
    translation_options: {
        source_lang: &quot;Chinese&quot;,
        target_lang: &quot;English&quot;,
        terms: [
            {
                &quot;source&quot;: &quot;生物传感器&quot;,
                &quot;target&quot;: &quot;biological sensor&quot;
            },
            {
                &quot;source&quot;: &quot;石墨烯&quot;,
                &quot;target&quot;: &quot;graphene&quot;
            },
            {
                &quot;source&quot;: &quot;化学元素&quot;,
                &quot;target&quot;: &quot;chemical elements&quot;
            },
            {
                &quot;source&quot;: &quot;身体健康状况&quot;,
                &quot;target&quot;: &quot;health status of the body&quot;
            }
        ]
    }
});
console.log(JSON.stringify(completion));
</code></pre></section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;messages&quot;: [
    {
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: &quot;而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。&quot;
    }
  ],
  &quot;translation_options&quot;: {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;terms&quot;: [
      {
        &quot;source&quot;: &quot;生物传感器&quot;,
        &quot;target&quot;: &quot;biological sensor&quot;
      },
      {
        &quot;source&quot;: &quot;石墨烯&quot;,
        &quot;target&quot;: &quot;graphene&quot;
      },
      {
        &quot;source&quot;: &quot;化学元素&quot;,
        &quot;target&quot;: &quot;chemical elements&quot;
      },
      {
        &quot;source&quot;: &quot;身体健康状况&quot;,
        &quot;target&quot;: &quot;health status of the body&quot;
      }
    ]
  }
}'
</code></pre></section></section></section><a id="翻译记忆"></a><section><a id="翻译记忆-h4"></a><h4>翻译记忆</h4><a id="sec-tabs-5"></a><section><a id="python-3"></a><section><a id="python-3-h4"></a><h4>Python</h4><a id="code-block-7"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下是北京地域的base_url
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;通过如下命令可以看出安装thrift的版本信息；&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;tm_list&quot;: [
        {
            &quot;source&quot;: &quot;您可以通过如下方式查看集群的内核版本信息:&quot;,
            &quot;target&quot;: &quot;You can use one of the following methods to query the engine version of a cluster:&quot;
        },
        {
            &quot;source&quot;: &quot;我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;&quot;,
            &quot;target&quot;: &quot;The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.&quot;
        },
        {
            &quot;source&quot;: &quot;您可以通过PyPI来安装SDK,安装命令如下:&quot;,
            &quot;target&quot;: &quot;You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:&quot;
        }
    ]
}

completion = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    extra_body={
        &quot;translation_options&quot;: translation_options
    }
)
print(completion.choices[0].message.content)
</code></pre></section><a id="node-js-3"></a><section><a id="node-js-3-h4"></a><h4>Node.js</h4><a id="code-block-8"></a><pre class="language-javascript"><code>// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下是北京地域的base_url
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);
const completion = await openai.chat.completions.create({
    model: &quot;qwen-mt-plus&quot;,
    messages: [
        { role: &quot;user&quot;, content: &quot;通过如下命令可以看出安装thrift的版本信息；&quot; }
    ],
    translation_options: {
        source_lang: &quot;Chinese&quot;,
        target_lang: &quot;English&quot;,
        tm_list: [
            {
                &quot;source&quot;: &quot;您可以通过如下方式查看集群的内核版本信息:&quot;,
                &quot;target&quot;: &quot;You can use one of the following methods to query the engine version of a cluster:&quot;
            },
            {
                &quot;source&quot;: &quot;我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;&quot;,
                &quot;target&quot;: &quot;The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.&quot;
            },
            {
                &quot;source&quot;: &quot;您可以通过PyPI来安装SDK,安装命令如下:&quot;,
                &quot;target&quot;: &quot;You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:&quot;
            }
        ]
    }
});
console.log(JSON.stringify(completion));
</code></pre></section><a id="curl-3"></a><section><a id="curl-3-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-9"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;messages&quot;: [
    {
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: &quot;通过如下命令可以看出安装thrift的版本信息；&quot;
    }
  ],
  &quot;translation_options&quot;: {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;tm_list&quot;:[
          {&quot;source&quot;: &quot;您可以通过如下方式查看集群的内核版本信息:&quot;, &quot;target&quot;: &quot;You can use one of the following methods to query the engine version of a cluster:&quot;},
          {&quot;source&quot;: &quot;我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;&quot;, &quot;target&quot;: &quot;The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.&quot;},
          {&quot;source&quot;: &quot;您可以通过PyPI来安装SDK,安装命令如下:&quot;, &quot;target&quot;: &quot;You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:&quot;}
    ]
  }
}'
</code></pre></section></section></section><a id="领域提示"></a><section><a id="领域提示-h4"></a><h4>领域提示</h4><a id="sec-tabs-6"></a><section><a id="python-4"></a><section><a id="python-4-h4"></a><h4>Python</h4><a id="code-block-10"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下是北京地域的base_url
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;domains&quot;: &quot;The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.&quot;
}

completion = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    extra_body={
        &quot;translation_options&quot;: translation_options
    }
)
print(completion.choices[0].message.content)
</code></pre></section><a id="node-js-4"></a><section><a id="node-js-4-h4"></a><h4>Node.js</h4><a id="code-block-11"></a><pre class="language-javascript"><code>// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from &quot;openai&quot;;

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下是北京地域的base_url
        baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
    }
);
const completion = await openai.chat.completions.create({
    model: &quot;qwen-mt-plus&quot;,
    messages: [
        { role: &quot;user&quot;, content: &quot;第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。&quot; }
    ],
    translation_options: {
        source_lang: &quot;Chinese&quot;,
        target_lang: &quot;English&quot;,
        domains: &quot;The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.&quot;
    }
});
console.log(JSON.stringify(completion));
</code></pre></section><a id="curl-4"></a><section><a id="curl-4-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-12"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;messages&quot;: [
    {
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: &quot;第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。&quot;
    }
  ],
  &quot;translation_options&quot;: {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;domains&quot;: &quot;The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.&quot;
  }
}'
</code></pre></section></section></section></section></td></tr><tr><td><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型：qwen-mt-plus、qwen-mt-flash、qwen-mt-lite。</p></td></tr><tr><td><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>消息数组，用于向大模型传递上下文。仅支持传入 User Message。</p><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于传递待翻译的句子。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>待翻译的句子。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，必须设为<code>user</code>。</p></div></section></div></section></td></tr><tr><td><p><strong>stream</strong><code>boolean</code>（可选） 默认值为 <code>false</code></p><p>是否以流式方式输出回复。</p><p>可选值：</p><ul><li><code>false</code>：等待模型生成完整回复后一次性返回。</li><li><code>true</code>：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。</li></ul><div><div><p><strong>说明</strong>当前仅qwen-mt-flash、qwen-mt-lite模型支持以增量形式返回数据，每次返回仅包含新生成的内容。qwen-mt-plus模型以非增量形式返回数据，每次返回当前已经生成的整个序列，暂时无法修改。如：</p><p>I</p><p>I didn</p><p>I didn't</p><p>I didn't laugh</p><p>I didn't laugh after</p><p>...</p></div></div></td></tr><tr><td><p><strong>stream_options</strong><code>object</code>（可选）</p><p>流式输出的配置项，仅在 <code>stream</code> 为 <code>true</code> 时生效。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>include_usage</strong><code>boolean</code>（可选）默认值为 <code>false</code></p><p>是否在<strong>最后一个数据块</strong>包含Token消耗信息。</p><p>可选值：</p><ul><li><code>true</code>：包含；</li><li><code>false</code>：不包含。</li></ul></div></section></td></tr><tr><td><p><strong>max_tokens</strong><code>integer</code>（可选）</p><p>用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。</p><p>默认值与最大值均为模型的最大输出长度，请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#154957e783dxk">模型选型</a>。</p></td></tr><tr><td><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p></td></tr><tr><td><p><strong>temperature</strong><code>float</code>（可选）默认值为0.65</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p></td></tr><tr><td><p><strong>top_p</strong><code>float</code>（可选）默认值为0.8</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p></td></tr><tr><td><p><strong>top_k</strong><code>integer</code>（可选）默认值为1</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;top_k&quot;: xxx}</code>；通过 Node.js SDK或HTTP方式调用时，请作为顶层参数传递。</p></td></tr><tr><td><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。</p><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;repetition_penalty&quot;: xxx}</code>；通过 Node.js SDK或HTTP方式调用时，请作为顶层参数传递。</p></td></tr><tr><td><p><strong>translation_options</strong><code>object</code><strong>（必选）</strong></p><p>需配置的翻译参数。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>source_lang</strong> <code>string</code> （必选）</p><p>源语言的英文全称，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#038d2865bbydc">支持的语言</a>。若设为<code>auto</code>，模型会自动识别输入的语种。</p><p><strong>target_lang</strong> <code>string</code> （必选）</p><p>目标语言的英文全称，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#038d2865bbydc">支持的语言</a>。</p><p><strong>terms</strong> <code>arrays</code> （可选）</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#2bf54a5ab5voe">术语干预</a>功能时需设置的术语数组。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>source</strong> <code>string</code> （必选）</p><p>源语言的术语。</p><p><strong>target</strong> <code>string</code> （必选）</p><p>目标语言的术语。</p></div></section><p><strong>tm_list</strong> <code>arrays</code> （可选）</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#17e15234e7gfp">翻译记忆</a>功能时需设置的翻译记忆数组。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>source</strong> <code>string</code> （必选）</p><p>源语言的语句。</p><p><strong>target</strong> <code>string</code> （必选）</p><p>目标语言的语句。</p></div></section><p><strong>domains</strong> <code>string</code> （可选）</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#4af23a31db7lf">领域提示</a>功能时需设置的领域提示语句。</p><blockquote><p>领域提示语句暂时只支持英文。</p></blockquote></div></section><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;translation_options&quot;: xxx}</code>；通过 Node.js SDK或HTTP方式调用时，请作为顶层参数传递。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h3>chat响应对象（非流式输出）</h3></td><td rowspan="9"><a id="code-block-13"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;chatcmpl-999a5d8a-f646-4039-968a-167743ae0f22&quot;,
  &quot;choices&quot;: [
    {
      &quot;finish_reason&quot;: &quot;stop&quot;,
      &quot;index&quot;: 0,
      &quot;logprobs&quot;: null,
      &quot;message&quot;: {
        &quot;content&quot;: &quot;I didn't laugh after watching this video.&quot;,
        &quot;refusal&quot;: null,
        &quot;role&quot;: &quot;assistant&quot;,
        &quot;annotations&quot;: null,
        &quot;audio&quot;: null,
        &quot;function_call&quot;: null,
        &quot;tool_calls&quot;: null
      }
    }
  ],
  &quot;created&quot;: 1762346157,
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;object&quot;: &quot;chat.completion&quot;,
  &quot;service_tier&quot;: null,
  &quot;system_fingerprint&quot;: null,
  &quot;usage&quot;: {
    &quot;completion_tokens&quot;: 9,
    &quot;prompt_tokens&quot;: 53,
    &quot;total_tokens&quot;: 62,
    &quot;completion_tokens_details&quot;: null,
    &quot;prompt_tokens_details&quot;: null
  }
}
</code></pre></td></tr><tr><td><p><strong>id</strong><code>string</code></p><p>本次请求的唯一标识符。</p></td></tr><tr><td><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>模型停止生成的原因。</p><p>有两种情况：</p><ul><li>自然停止输出时为<code>stop</code>；</li><li>生成长度过长而结束为<code>length</code>。</li></ul><p><strong>index</strong><code>integer</code></p><p>当前对象在<code>choices</code>数组中的索引。</p><p><strong>message</strong><code>object</code></p><p>模型输出的消息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>模型翻译结果。</p><p><strong>refusal</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>audio</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>function_call</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>tool_calls</strong> <code>array</code></p><p>该参数当前固定为<code>null</code>。</p></div></section></div></section></td></tr><tr><td><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。</p></td></tr><tr><td><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p></td></tr><tr><td><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion</code>。</p></td></tr><tr><td><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p></td></tr><tr><td><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p></td></tr><tr><td><p><strong>usage</strong> <code>object</code></p><p>本次请求的 Token 消耗信息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="e98e6b7aa5nb2"></a><h3>chat响应chunk对象（流式输出）</h3></td><td rowspan="9"><a id="fig-code-group"></a><div><a id="fig-code-group-增量输出-tab"></a>增量输出<div><a id="code-code-group-增量输出"></a><pre class="language-json"><code>{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot;&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: &quot;assistant&quot;, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot;I&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot; didn&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot;'t&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot; laugh&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot; after&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot; watching&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot; this&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot; video&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot;.&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: null, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot;&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: &quot;stop&quot;, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [{&quot;delta&quot;: {&quot;content&quot;: &quot;&quot;, &quot;function_call&quot;: null, &quot;refusal&quot;: null, &quot;role&quot;: null, &quot;tool_calls&quot;: null}, &quot;finish_reason&quot;: &quot;stop&quot;, &quot;index&quot;: 0, &quot;logprobs&quot;: null}], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: null}
{&quot;id&quot;: &quot;chatcmpl-d8aa6596-b366-4ed0-9f6d-2e89247f554e&quot;, &quot;choices&quot;: [], &quot;created&quot;: 1762504029, &quot;model&quot;: &quot;qwen-mt-flash&quot;, &quot;object&quot;: &quot;chat.completion.chunk&quot;, &quot;service_tier&quot;: null, &quot;system_fingerprint&quot;: null, &quot;usage&quot;: {&quot;completion_tokens&quot;: 9, &quot;prompt_tokens&quot;: 56, &quot;total_tokens&quot;: 65, &quot;completion_tokens_details&quot;: null, &quot;prompt_tokens_details&quot;: null}}
</code></pre></div><a id="fig-code-group-非增量输出-tab"></a>非增量输出<div><a id="code-code-group-非增量输出"></a><pre class="language-json"><code>{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:&quot;assistant&quot;,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after watching&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after watching this&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after watching this video&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after watching this video.&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after watching this video.&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:&quot;stop&quot;,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;I didn’t laugh after watching this video.&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:&quot;stop&quot;,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-478e183e-cbdc-4ea0-aeae-4c2ba1d03e4d&quot;,&quot;choices&quot;:[],&quot;created&quot;:1762346453,&quot;model&quot;:&quot;qwen-mt-plus&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:{&quot;completion_tokens&quot;:9,&quot;prompt_tokens&quot;:56,&quot;total_tokens&quot;:65,&quot;completion_tokens_details&quot;:null,&quot;prompt_tokens_details&quot;:null}}
</code></pre></div></div></td></tr><tr><td><p><strong>id</strong><code>string</code></p><p>本次调用的唯一标识符。每个chunk对象有相同的 id。</p></td></tr><tr><td><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。若设置<code>include_usage</code>参数为<code>true</code>，则在最后一个chunk中为空。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>delta</strong> <code>object</code></p><p>流式返回的输出内容。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>翻译结果，qwen-mt-flash和qwen-mt-lite为增量式更新，qwen-mt-plus为非增量式更新。</p><p><strong>function_call</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>refusal</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息对象的角色，只在第一个chunk中有值。</p></div></section><p><strong>finish_reason</strong> <code>string</code></p><p>模型停止生成的原因。有三种情况：</p><ul><li>自然停止输出时为<code>stop</code>；</li><li>生成未结束时为<code>null</code>；</li><li>生成长度过长而结束为<code>length</code>。</li></ul><p><strong>index</strong> <code>integer</code></p><p>当前响应在<code>choices</code>数组中的索引。</p></div></section></td></tr><tr><td><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。每个chunk有相同的时间戳。</p></td></tr><tr><td><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p></td></tr><tr><td><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion.chunk</code>。</p></td></tr><tr><td><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p></td></tr><tr><td><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p></td></tr><tr><td><p><strong>usage</strong> <code>object</code></p><p>本次请求消耗的Token。只在<code>include_usage</code>为<code>true</code>时，在最后一个chunk返回。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p></div></section></td></tr></tbody></table>

<a id="dashscope"></a>

<a id="69cac67a477k2"></a>

## DashScope

<a id="sec-tabs-7"></a>

<a id="北京地域-2"></a>

<a id="北京地域-2-h4"></a>

#### 北京地域

HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK 调用无需配置接入地址，构造 `Client` 时通过 `workspace` 与 `region` 参数指定地域（默认华北2（北京）地域）。

<a id="新加坡地域-2"></a>

<a id="新加坡地域-2-h4"></a>

#### 新加坡地域

HTTP 请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-8"></a>

<a id="python代码"></a>

<a id="python代码-h4"></a>

#### Python代码

<a id="code-block-14"></a>

```python
import os
import dashscope

# 以下为新加坡地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="ap-southeast-1",
)
```

<a id="java代码"></a>

<a id="java代码-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-15"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-16"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";
```

<a id="美国-弗吉尼亚-地域-2"></a>

<a id="美国-弗吉尼亚-地域-2-h4"></a>

#### 美国（弗吉尼亚）地域

HTTP 请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-9"></a>

<a id="python代码-2"></a>

<a id="python代码-2-h4"></a>

#### Python代码

<a id="code-block-17"></a>

```python
import os
import dashscope

# 以下为美国（弗吉尼亚）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="us-east-1",
)
```

<a id="java代码-2"></a>

<a id="java代码-2-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-18"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-19"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";
```

> 您需要已 [获取与配置 API Key](../preparations/get-api-key.md) 并 [配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) 。若通过DashScope SDK进行调用，需要 [安装DashScope SDK](../preparations/install-sdk.md) 。

<table><tbody><tr><td><a id="2a1c410015otp"></a><h3>请求体</h3></td><td rowspan="11"><a id="sec-tabs-10"></a><section><a id="基础使用-2"></a><section><a id="基础使用-2-h4"></a><h4>基础使用</h4><a id="sec-tabs-11"></a><section><a id="python-5"></a><section><a id="python-5-h4"></a><h4>Python</h4><a id="code-block-20"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将下行region替换为：region=&quot;ap-southeast-1&quot;
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;我看到这个视频后没有笑&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;auto&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
}
response = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    parameters={&quot;translation_options&quot;: translation_options}
)
print(response.choices[0].message.content)
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><a id="code-block-21"></a><pre class="language-java"><code>// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请将{WorkspaceId}替换为真实的业务空间ID，并释放下列注释
    // static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1&quot;;}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(&quot;我看到这个视频后没有笑&quot;)
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang(&quot;auto&quot;)
                .targetLang(&quot;English&quot;)
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen-mt-plus&quot;)
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;错误信息：&quot;+e.getMessage());
            e.printStackTrace();
        } finally {
            System.exit(0);
        }
    }
}
</code></pre></section><a id="curl-5"></a><section><a id="curl-5-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-22"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H &quot;Authorization: $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;content&quot;: &quot;我看到这个视频后没有笑&quot;,
        &quot;role&quot;: &quot;user&quot;
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;translation_options&quot;: {
      &quot;source_lang&quot;: &quot;auto&quot;,
      &quot;target_lang&quot;: &quot;English&quot;
    }
  }
}'
</code></pre></section></section></section><a id="术语干预-2"></a><section><a id="术语干预-2-h4"></a><h4>术语干预</h4><a id="sec-tabs-12"></a><section><a id="python-6"></a><section><a id="python-6-h4"></a><h4>Python</h4><a id="code-block-23"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将下行region替换为：region=&quot;ap-southeast-1&quot;
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)
messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;terms&quot;: [
        {
            &quot;source&quot;: &quot;生物传感器&quot;,
            &quot;target&quot;: &quot;biological sensor&quot;
        },
        {
            &quot;source&quot;: &quot;石墨烯&quot;,
            &quot;target&quot;: &quot;graphene&quot;
        },
        {
            &quot;source&quot;: &quot;化学元素&quot;,
            &quot;target&quot;: &quot;chemical elements&quot;
        },
        {
            &quot;source&quot;: &quot;身体健康状况&quot;,
            &quot;target&quot;: &quot;health status of the body&quot;
        }
    ]
}
response = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    parameters={&quot;translation_options&quot;: translation_options}
)
print(response.choices[0].message.content)
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><a id="code-block-24"></a><pre class="language-java"><code>// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.aigc.generation.TranslationOptions.Term;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请将{WorkspaceId}替换为真实的业务空间ID，并释放下列注释
    // static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1&quot;;}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(&quot;而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。&quot;)
                .build();
        Term term1 = Term.builder()
                .source(&quot;生物传感器&quot;)
                .target(&quot;biological sensor&quot;)
                .build();
        Term term2 = Term.builder()
                .source(&quot;身体健康状况&quot;)
                .target(&quot;health status of the body&quot;)
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang(&quot;auto&quot;)
                .targetLang(&quot;English&quot;)
                .terms(Arrays.asList(term1, term2))
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen-mt-plus&quot;)
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main() {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;错误信息：&quot;+e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="curl-6"></a><section><a id="curl-6-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-25"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H &quot;Authorization: $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;content&quot;: &quot;而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。&quot;,
        &quot;role&quot;: &quot;user&quot;
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;translation_options&quot;: {
      &quot;source_lang&quot;: &quot;Chinese&quot;,
      &quot;target_lang&quot;: &quot;English&quot;,
      &quot;terms&quot;: [
        {
          &quot;source&quot;: &quot;生物传感器&quot;,
          &quot;target&quot;: &quot;biological sensor&quot;
        },
        {
          &quot;source&quot;: &quot;身体健康状况&quot;,
          &quot;target&quot;: &quot;health status of the body&quot;
        }
      ]
  }
}'
</code></pre></section></section></section><a id="翻译记忆-2"></a><section><a id="翻译记忆-2-h4"></a><h4>翻译记忆</h4><a id="sec-tabs-13"></a><section><a id="python-7"></a><section><a id="python-7-h4"></a><h4>Python</h4><a id="code-block-26"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将下行region替换为：region=&quot;ap-southeast-1&quot;
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)
messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;通过如下命令可以看出安装thrift的版本信息；&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;tm_list&quot;: [
        {
            &quot;source&quot;: &quot;您可以通过如下方式查看集群的内核版本信息:&quot;,
            &quot;target&quot;: &quot;You can use one of the following methods to query the engine version of a cluster:&quot;
        },
        {
            &quot;source&quot;: &quot;我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;&quot;,
            &quot;target&quot;: &quot;The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.&quot;
        },
        {
            &quot;source&quot;: &quot;您可以通过PyPI来安装SDK,安装命令如下:&quot;,
            &quot;target&quot;: &quot;You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:&quot;
        }
    ]}
response = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    parameters={&quot;translation_options&quot;: translation_options}
)
print(response.choices[0].message.content)
</code></pre></section><a id="java-3"></a><section><a id="java-3-h4"></a><h4>Java</h4><a id="code-block-27"></a><pre class="language-java"><code>// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.aigc.generation.TranslationOptions.Tm;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请将{WorkspaceId}替换为真实的业务空间ID，并释放下列注释
    // static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1&quot;;}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(&quot;通过如下命令可以看出安装thrift的版本信息；&quot;)
                .build();
        Tm tm1 = Tm.builder()
                .source(&quot;您可以通过如下方式查看集群的内核版本信息:&quot;)
                .target(&quot;You can use one of the following methods to query the engine version of a cluster:&quot;)
                .build();
        Tm tm2 = Tm.builder()
                .source(&quot;我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;&quot;)
                .target(&quot;The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.&quot;)
                .build();
        Tm tm3 = Tm.builder()
                .source(&quot;您可以通过PyPI来安装SDK,安装命令如下:&quot;)
                .target(&quot;You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:&quot;)
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang(&quot;auto&quot;)
                .targetLang(&quot;English&quot;)
                .tmList(Arrays.asList(tm1, tm2, tm3))
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen-mt-plus&quot;)
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main() {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;错误信息：&quot;+e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="curl-7"></a><section><a id="curl-7-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-28"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H &quot;Authorization: $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;content&quot;: &quot;通过如下命令可以看出安装thrift的版本信息；&quot;,
        &quot;role&quot;: &quot;user&quot;
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;translation_options&quot;: {
      &quot;source_lang&quot;: &quot;Chinese&quot;,
      &quot;target_lang&quot;: &quot;English&quot;,
      &quot;tm_list&quot;:[
          {&quot;source&quot;: &quot;您可以通过如下方式查看集群的内核版本信息:&quot;, &quot;target&quot;: &quot;You can use one of the following methods to query the engine version of a cluster:&quot;},
          {&quot;source&quot;: &quot;我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;&quot;, &quot;target&quot;: &quot;The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.&quot;},
          {&quot;source&quot;: &quot;您可以通过PyPI来安装SDK,安装命令如下:&quot;, &quot;target&quot;: &quot;You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:&quot;}
      ]
  }
}'
</code></pre></section></section></section><a id="领域提示-2"></a><section><a id="领域提示-2-h4"></a><h4>领域提示</h4><a id="sec-tabs-14"></a><section><a id="python-8"></a><section><a id="python-8-h4"></a><h4>Python</h4><a id="code-block-29"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将下行region替换为：region=&quot;ap-southeast-1&quot;
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: &quot;第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。&quot;
    }
]
translation_options = {
    &quot;source_lang&quot;: &quot;Chinese&quot;,
    &quot;target_lang&quot;: &quot;English&quot;,
    &quot;domains&quot;: &quot;The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.&quot;
}
response = client.chat.completions.create(
    model=&quot;qwen-mt-plus&quot;,
    messages=messages,
    parameters={&quot;translation_options&quot;: translation_options}
)
print(response.choices[0].message.content)
</code></pre></section><a id="java-4"></a><section><a id="java-4-h4"></a><h4>Java</h4><a id="code-block-30"></a><pre class="language-java"><code>// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请将{WorkspaceId}替换为真实的业务空间ID，并释放下列注释
    // static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1&quot;;}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(&quot;第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。&quot;)
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang(&quot;auto&quot;)
                .targetLang(&quot;English&quot;)
                .domains(&quot;The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.&quot;)
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen-mt-plus&quot;)
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main() {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;错误信息：&quot;+e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="curl-8"></a><section><a id="curl-8-h4"></a><h4>curl</h4><p>各地域的<a href="qwen-mt-api.md">请求地址</a>和API Key不同，以下是北京地域的请求地址。</p><a id="code-block-31"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H &quot;Authorization: $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
  &quot;model&quot;: &quot;qwen-mt-plus&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;content&quot;: &quot;第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。&quot;,
        &quot;role&quot;: &quot;user&quot;
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;translation_options&quot;: {
      &quot;source_lang&quot;: &quot;Chinese&quot;,
      &quot;target_lang&quot;: &quot;English&quot;,
      &quot;domains&quot;: &quot;The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.&quot;}
  }
}'
</code></pre></section></section></section></section></td></tr><tr><td><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型：qwen-mt-plus、qwen-mt-flash、qwen-mt-lite。</p></td></tr><tr><td><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>消息数组，用于向大模型传递上下文。仅支持传入 User Message。</p><a id="accordion-消息类型-2"></a><section><p>消息类型</p><div><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于传递待翻译的句子。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>待翻译的句子。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，必须设为<code>user</code>。</p></div></section></div></section></td></tr><tr><td><p><strong>max_tokens</strong><code>integer</code>（可选）</p><p>用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。</p><p>默认值与最大值均为模型的最大输出长度，请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#154957e783dxk">模型选型</a>。</p><blockquote><p>Java SDK中为<strong>maxTokens</strong>*。*通过HTTP调用时，请将 <strong>max_tokens</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr><tr><td><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><blockquote><p>通过HTTP调用时，请将 <strong>seed</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr><tr><td><p><strong>temperature</strong><code>float</code>（可选）默认值为0.65</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>通过HTTP调用时，请将 <strong>temperature</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr><tr><td><p><strong>top_p</strong><code>float</code>（可选）默认值为0.8</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>Java SDK中为<strong>topP</strong>*。*通过HTTP调用时，请将 <strong>top_p</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr><tr><td><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。</p><blockquote><p>Java SDK中为<strong>repetitionPenalty</strong>*。*通过HTTP调用时，请将 <strong>repetition_penalty</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr><tr><td><p><strong>top_k</strong><code>integer</code>（可选）默认值为1</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><blockquote><p>Java SDK中为<strong>topK</strong>*。*通过HTTP调用时，请将 <strong>top_k</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr><tr><td><p><strong>stream</strong><code>boolean</code>（可选）</p><p>是否以流式方式输出回复。</p><p>可选值：</p><ul><li><code>false</code>：等待模型生成完整回复后一次性返回。</li><li><code>true</code>：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。</li></ul><div><div><p><strong>说明</strong>当前仅qwen-mt-flash、qwen-mt-lite模型支持以增量形式返回数据，每次返回仅包含新生成的内容。qwen-mt-plus模型以非增量形式返回数据，每次返回当前已经生成的整个序列，暂时无法修改。如：</p><p>I</p><p>I didn</p><p>I didn't</p><p>I didn't laugh</p><p>I didn't laugh after</p><p>...</p></div></div><blockquote><p>该参数仅支持Python SDK。通过Java SDK实现流式输出请通过<code>streamCall</code>接口调用；通过HTTP实现流式输出请在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</p></blockquote></td></tr><tr><td><p><strong>translation_options</strong><code>object</code><strong>（必选）</strong></p><p>需配置的翻译参数。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>source_lang</strong> <code>string</code> （必选）</p><p>源语言的英文全称，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#038d2865bbydc">支持的语言</a>。若设为<code>auto</code>，模型会自动识别输入的语种。</p><p><strong>target_lang</strong> <code>string</code> （必选）</p><p>目标语言的英文全称，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#038d2865bbydc">支持的语言</a>。</p><p><strong>terms</strong> <code>arrays</code> （可选）</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#2bf54a5ab5voe">术语干预</a>功能时需设置的术语数组。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>source</strong> <code>string</code> （必选）</p><p>源语言的术语。</p><p><strong>target</strong> <code>string</code> （必选）</p><p>目标语言的术语。</p></div></section><p><strong>tm_list</strong> <code>arrays</code> （可选）</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#17e15234e7gfp">翻译记忆</a>功能时需设置的翻译记忆数组。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>source</strong> <code>string</code> （必选）</p><p>源语言的语句。</p><p><strong>target</strong> <code>string</code> （必选）</p><p>目标语言的语句。</p></div></section><p><strong>domains</strong> <code>string</code> （可选）</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#4af23a31db7lf">领域提示</a>功能时需设置的领域提示语句。</p><blockquote><p>领域提示语句暂时只支持英文。</p></blockquote></div></section><blockquote><p>Java SDK中为<code>translationOptions</code>。通过HTTP调用时，请将 <strong>translation_options</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h3>chat响应对象（流式与非流式输出格式一致）</h3><blockquote><p>Python SDK 调用失败时会抛出<code>DashScopeError</code>，可通过<code>e.code</code>/<code>e.status_code</code>/<code>e.message</code>/<code>e.request_id</code>获取错误信息。Java SDK 调用失败会抛出<code>ApiException</code>，可通过<code>ApiException.getStatus().getStatusCode()</code>获取错误状态码。</p></blockquote></td><td rowspan="4"><a id="code-block-32"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;9b4ec3b2-6d29-40a6-a08b-7e3c9a51c289&quot;,
  &quot;choices&quot;: [
    {
      &quot;index&quot;: 0,
      &quot;finish_reason&quot;: &quot;stop&quot;,
      &quot;message&quot;: {
        &quot;role&quot;: &quot;assistant&quot;,
        &quot;content&quot;: &quot;I didn't laugh after watching this video.&quot;
      }
    }
  ],
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 53,
    &quot;output_tokens&quot;: 9,
    &quot;total_tokens&quot;: 62
  }
}
</code></pre></td></tr><tr><td><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><blockquote><p>Java SDK返回参数为<strong>requestId。</strong></p></blockquote></td></tr><tr><td><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>index</strong><code>integer</code></p><p>当前对象在<code>choices</code>数组中的索引。</p><p><strong>finish_reason</strong><code>string</code></p><p>模型结束生成的原因。有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>因模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code>；</li></ul><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>string</code></p><p>翻译的结果。</p></div></section></div></section></td></tr><tr><td><p><strong>usage</strong><code>object</code></p><p>本次请求使用的Token信息。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数，为<strong>input_tokens</strong>与<strong>output_tokens</strong>之和<strong>。</strong></p></div></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="97e145aeabbwf"></a>

## 错误码

如果模型调用失败，Python SDK 会抛出`DashScopeError`，可通过`e.code`/`e.message`/`e.request_id`获取错误信息，请参见[错误码](../preparations/error-code.md)进行解决。

.aliyun-docs-content .one-codeblocks pre {

max-height: calc(80vh - 136px) !important;

height: auto;

}

.tab-item {

font-size: 12px !important; /_你可以根据需要调整字体大小_/

padding: 0px 5px !important;

}

.expandable-content {

border-left: none !important;

border-right: none !important;

border-bottom: none !important;

}
