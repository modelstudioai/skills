# 新版智能体应用 API 参考

本文介绍 DashScope API 调用阿里云百炼新版智能体应用的输入与输出参数。

**相关指南：**[新版智能体应用（Agent 2.0）](../application-user-guide/agent-development/llm-application/new-single-agent-application.md)。

> **重要**
>
> 本文档仅适用于华北2（北京）地域。

<a id="前置准备"></a>

<a id="e846d6db23z61"></a>

## 前置准备

开始前，请确保您已完成以下操作：

1.  **创建应用：**前往[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)创建阿里云百炼**新版智能体应用**并获取应用 ID。
2.  **获取 API Key：**通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **安装SDK（可选）：**若使用 SDK 调用，请安装相应语言的[DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="调用方式"></a>

<a id="69cac67a477k2"></a>

## 调用方式

-   **HTTP 接口调用**
    
    请求地址：`POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion`
    
    > 其中 `APP_ID` 需替换为您的实际应用 ID。
    
-   **SDK 调用**
    
    Python/Java SDK：已默认配置正确的 endpoint
    
    自定义 endpoint：可通过 base\_url 参数配置
    

**在线调试**：通过**应用卡片 -> 发布 -> API 调试**路径进入调试页面后，填写参数并点击运行即可。

<table><tbody><tr><td><a id="989b585548qnj"></a><h3>请求体</h3><p><strong>app_id</strong><code>string</code><strong>（必选）</strong></p><p>应用标识。</p><p>在<a href="https://bailian.console.aliyun.com/#/app-center">应用管理</a>的应用卡片上获取。</p><blockquote><p>Java SDK中为 <strong>appId。</strong>通过 HTTP 调用时，请将实际的应用 ID 放入 <strong>URL</strong>中，替换<code>APP_ID</code>。</p></blockquote><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>用户的输入指令，用于指导应用生成回复。</p><blockquote><p>通过 HTTP 调用时，请将 <strong>prompt</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>session_id</strong><code>string</code> （可选）</p><p>历史对话标识。</p><p>传入<code>session_id</code>时，请求将自动携带云端存储的对话历史。此时必须传递<code>prompt</code>。</p><p>该 ID 在连续<strong>1 小时内</strong>无任何请求后将自动失效。</p><blockquote><p>Java SDK 中为 <strong>setSessionId</strong>。通过 HTTP 调用时，请将 <strong>session_id</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>workspace</strong> <code>string</code> （可选）</p><p>业务空间标识。相关文档：<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#732535cfc959h">获取Workspace ID</a>。</p><p>仅调用<a href="https://help.aliyun.com/zh/model-studio/use-workspace">子业务空间</a>的应用时需传递<code>workspace ID</code>。</p><blockquote><p>通过 HTTP 调用时，请指定Header中的 <strong>X-DashScope-WorkSpace</strong>。</p></blockquote><p><strong>stream</strong> <code>boolean</code>（可选） 默认值为 <code>false</code></p><p>是否以流式输出方式回复。</p><p>推荐设置为<code>true</code>，可提升阅读体验并降低超时风险。</p><p>参数值：</p><ul><li><code>false</code>（默认）：模型生成全部内容后一次性返回；</li><li><code>true</code>（推荐）：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。</li></ul><blockquote><p>通过Java SDK实现流式输出请通过<code>streamCall</code>接口调用；通过HTTP实现流式输出请在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</p></blockquote><p><strong>incremental_output</strong> <code>boolean</code>（可选）默认值为 <code>false</code></p><p>在<strong>流式输出模式下</strong>是否开启增量输出。</p><p>推荐设置为<code>true</code>，可提升阅读体验。</p><p>参数值：</p><ul><li><code>false</code>（默认）：每次输出当前已经生成的整个序列，最后一次输出为生成的完整结果。</li></ul><a id="code-block"></a><pre class="language-text"><code>I
I like
I like apple
I like apple.
</code></pre><ul><li><code>true</code>（推荐）：增量输出，即后续输出内容不包含已输出的内容。需要实时地逐个读取这些片段以获得完整的结果。</li></ul><a id="code-block-2"></a><pre class="language-text"><code>I
like
apple
.
</code></pre><blockquote><p>Java SDK中为<strong>incrementalOutput</strong>*。*通过HTTP调用时，请将<strong>incremental_output</strong>放入<strong>parameters</strong>对象中。</p></blockquote><p><strong>enable_thinking</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>此参数用于在<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>中切换思考模式和非思考模式。</p><p>参数值：</p><ul><li>False（默认）：非思考模式。直接返回最终答案（<code>text</code>字段）。</li><li>True：启用思考模式。模型先输出思考过程，再返回最终答案。</li></ul><p>优先级：</p><ul><li>若调用时未设置此参数，以应用内模型的思考模式开关状态为准。</li><li>若调用时设置了<code>enable_thinking</code>，以 API 参数为准。</li></ul><div><div><p><strong>重要</strong>要获取思考过程的内容，必须同时将<code>has_thoughts</code>设为<code>True</code>，则：</p><ol><li>思考过程：<code>thought</code>字段获取。</li><li>最终答案：<code>text</code>字段获取。</li></ol></div></div><blockquote><p>开启<code>enable_thinking</code>有极小概率不会输出思考过程。</p></blockquote><blockquote><p>Java SDK中为<strong>enableThinking</strong>。通过HTTP调用时，请将 <strong>enable_thinking</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK的版本至少应为<strong>2.20.0</strong>。</p></blockquote><p><strong>has_thoughts</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否输出已开启思考模式的模型思考过程，在<code>thoughts</code>字段中查看。</p><p>参数值：</p><ul><li>True：输出。</li><li>False（默认）：不输出。</li></ul><blockquote><p>Java SDK 中为 <strong>hasThoughts</strong>。通过 HTTP 调用时，请将 <strong>has_thoughts</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><p><strong>image_list</strong> <code>array</code>（可选）</p><p>图片列表。支持图像 URL 和 Data URL（Base64 编码）。应用内需选择<strong><a href="../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a></strong>模型。</p><p><code>base64</code>编码格式可构建为 <a href="https://www.rfc-editor.org/rfc/rfc2397">Data URL</a>：<code>data:[MIME_type];base64,{base64_image}</code>。详细说明和代码示例见本文档<a href="new-agent-application-api-reference-be3bf785ec80b8bd.md">视觉理解章节</a>。</p><blockquote><p>Java SDK 中为 <strong>images</strong>。通过 HTTP 调用时，请将 <strong>image_list</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>file_list</strong> <code>array</code>（可选）</p><p>文件 URL 列表。</p><blockquote><p>Java SDK中为 <strong>files</strong>。通过HTTP调用时，请将 <strong>file_list</strong>放入 <strong>input</strong>对象中。</p></blockquote><blockquote><p>Python Dashscope SDK 的版本至少应为2.0.1，Java Dashscope SDK的版本至少应为2.21.13。</p></blockquote><p><strong>model_id</strong><code>string</code>（可选）</p><p>模型名称。</p><p>API 调用时，可通过此参数传递本次调用使用的模型名称。</p><p>优先级：当通过 API 传递的<code>model_id</code>与控制台配置不同时，以 API 参数值为准。</p><blockquote><p>Java SDK 中为 <strong>modelId</strong>。通过HTTP调用时，请将 <strong>model_id</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK 的版本至少应为<strong>2.19.3</strong>。</p></blockquote></td><td><a id="sec-tabs"></a><section><a id="单轮对话"></a><section><a id="单轮对话-h4"></a><h4>单轮对话</h4><a id="sec-tabs-2"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-3"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 替换为实际的应用 ID
        prompt='你是谁？')
    print(response.text)
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-4"></a><pre class="language-java"><code>// 建议dashscope SDK的版本 &gt;= 2.12.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void appCall()
            throws ApiException, NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;你是谁？&quot;)
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf(&quot;text: %s\n&quot;,
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;message：&quot;+e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http"></a><section><a id="http-h4"></a><h4>HTTP</h4><a id="sec-tabs-3"></a><section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-5"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你是谁？&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。</p></blockquote></section><a id="php"></a><section><a id="php-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-6"></a><pre class="language-php"><code>&lt;?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你是谁？'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }}
else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js"></a><section><a id="node-js-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-7"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="code-block-8"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;你是谁？&quot;
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></section><a id="c"></a><section><a id="c-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-9"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你是谁？&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go"></a><section><a id="go-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-10"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;你是谁？&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section></section></section></section><a id="多轮对话"></a><section><a id="多轮对话-h4"></a><h4>多轮对话</h4><p>多轮对话通过<code>session_id</code>维护会话上下文：</p><ol><li><p>首次请求：无需传入 session_id，响应中会返回新生成的session_id。</p></li><li><p>后续请求：携带上一次响应的 session_id 即可延续对话。</p></li><li><p>有效期：session_id 在最后一次请求后 1 小时内有效。</p></li></ol><a id="sec-tabs-4"></a><section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-11"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

def call_with_session():
    client = dashscope.Client(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
    try:
        response = client.apps.completions.create(
            app_id='APP_ID',  # 替换为实际的应用 ID
            prompt='你是谁？')

        responseNext = client.apps.completions.create(
                    app_id='APP_ID',  # 替换为实际的应用 ID
                    prompt='你有什么技能?',
                    session_id=response.session_id)  # 上一轮response的session_id

        print('%s\n session_id=%s\n' % (responseNext.text, responseNext.session_id))
        # print('%s\n' % (response.usage))
    except DashScopeError as e:
        print(f'request_id={e.request_id}')
        print(f'code={e.code}')
        print(f'message={e.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')

if __name__ == '__main__':
    call_with_session()
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-12"></a><pre class="language-java"><code>import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Arrays;
import java.util.List;
public class Main {
    public static void callWithSession()
            throws ApiException, NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 替换为实际的应用 ID
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;你是谁？&quot;)
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        param.setSessionId(result.getOutput().getSessionId());
        param.setPrompt(&quot;你有什么技能?&quot;);
        result = application.call(param);

        System.out.printf(&quot;%s\n session_id: %s\n&quot;,
                result.getOutput().getText(), result.getOutput().getSessionId());
    }

    public static void main(String[] args) {
        try {
            callWithSession();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-2"></a><section><a id="http-2-h4"></a><h4>HTTP</h4><a id="sec-tabs-5"></a><section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-13"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你是谁？&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-14"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你有什么技能？&quot;,
        &quot;session_id&quot;:&quot;4f8ef7233dc641aba496cb201fa59f8c&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre></section><a id="php-2"></a><section><a id="php-2-h4"></a><h4>PHP</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-15"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你是谁？'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    };
    if (isset($response_data['output']['session_id'])) {
        echo &quot;session_id={$response_data['output']['session_id']}\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-16"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你有什么技能？',
        // 替换为实际上一轮对话返回的session_id
        'session_id' =&gt; '2e658bcb514f4d30ab7500b4766a8d43'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    };
    if (isset($response_data['output']['session_id'])) {
        echo &quot;session_id={$response_data['output']['session_id']}\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js-2"></a><section><a id="node-js-2-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-17"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例（上一轮对话）</strong><a id="code-block-18"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;你是谁？&quot;
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
            console.log(`session_id=${response.data.output.session_id}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-19"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    // session_id替换为实际上一轮对话的session_id
    const data = {
        input: {
            prompt: &quot;你有什么技能？&quot;,
            session_id: 'fe4ce8b093bf46159ea9927a7b22f0d3',
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
            console.log(`session_id=${response.data.output.session_id}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
</code></pre></section><a id="c-2"></a><section><a id="c-2-h4"></a><h4>C#</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-20"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你是谁？&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-21"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你有什么技能？&quot;&quot;,
                    &quot;&quot;session_id&quot;&quot;: &quot;&quot;7b830e4cc8fe44faad0e648f9b71435f&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-2"></a><section><a id="go-2-h4"></a><h4>Go</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-22"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;你是谁？&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-23"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;:     &quot;你有什么技能？&quot;,
			&quot;session_id&quot;: &quot;f7eea37f0c734c20998a021b688d6de2&quot;, // 替换为实际上一轮对话的session_id
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section><blockquote><p>APP_ID替换为实际的应用 ID。下一轮对话的输入参数<code>session_id</code>字段值替换为实际上一轮对话返回的session_id值。</p></blockquote></section></section></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><p>通过<code>stream</code>实现流式输出。</p><a id="sec-tabs-6"></a><section><a id="python-3"></a><section><a id="python-3-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-24"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    stream = client.apps.completions.create(
                app_id='APP_ID',
                prompt='你是谁？',
                stream=True,  # 流式输出
                incremental_output=True)  # 增量输出

    for partial in stream:
        print(f'{partial.text}\n')  # 处理只输出文本text
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-3"></a><section><a id="java-3-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-25"></a><pre class="language-java"><code>// 建议dashscope SDK的版本 &gt;= 2.15.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;// 流式输出
// 智能体应用调用实现流式输出结果

public class Main {
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 替换为实际的应用 ID
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;你是谁?&quot;)
                // 增量输出
                .incrementalOutput(true)
                .build();
        Application application = new Application();
        // .streamCall（）：流式输出内容
        Flowable&lt;ApplicationResult&gt; result = application.streamCall(param);
        result.blockingForEach(data -&gt; {
            System.out.printf(&quot;%s\n&quot;,
                    data.getOutput().getText());
        });
    }
    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-3"></a><section><a id="http-3-h4"></a><h4>HTTP</h4><a id="sec-tabs-7"></a><section><a id="curl-3"></a><section><a id="curl-3-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-26"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--header 'X-DashScope-SSE: enable' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你是谁？&quot;

    },
    &quot;parameters&quot;:  {
        &quot;incremental_output&quot;:true
    },
    &quot;debug&quot;: {}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。</p></blockquote></section><a id="php-3"></a><section><a id="php-3-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-27"></a><pre class="language-php"><code>&lt;?php

// 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你是谁？'],
    &quot;parameters&quot; =&gt; [
        'incremental_output' =&gt; true]];// 增量输出
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, false); // 不返回传输的数据
curl_setopt($ch, CURLOPT_WRITEFUNCTION, function ($ch, $string) {
    echo $string; // 处理流式数据
    return strlen($string);
});
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key,
    'X-DashScope-SSE: enable' // 流式输出
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);

if ($status_code != 200) {
    echo &quot;HTTP Status Code: $status_code\n&quot;;
    echo &quot;Request Failed.\n&quot;;
}
?&gt;
</code></pre></section><a id="node-js-3"></a><section><a id="node-js-3-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-28"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="accordion-1-输出完整响应"></a><section><p>1.输出完整响应</p><div><a id="code-block-29"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;你是谁？&quot;
        },
        parameters: {
            'incremental_output' : 'true' // 增量输出
        },
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable' // 流式输出
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            // 处理流式响应
            response.data.on('data', (chunk) =&gt; {
                console.log(`Received chunk: ${chunk.toString()}`);
            });
        } else {
            console.log(&quot;Request failed:&quot;);
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></div></section><p>可展开折叠面板查看具体内容：</p><a id="accordion-2-只输出text字段内容"></a><section><p>2.只输出text字段内容</p><div><a id="code-block-30"></a><pre class="language-javascript"><code>const axios = require('axios');
const { Transform } = require('stream');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID'; // 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: { prompt: &quot;你是谁？&quot; },
        parameters: { incremental_output: true }, // 增量输出
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable' // 流式输出
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            // // 处理流式响应 SSE协议解析转换流
            const sseTransformer = new Transform({
                transform(chunk, encoding, callback) {
                    this.buffer += chunk.toString();

                    // 按SSE事件分割（两个换行符）
                    const events = this.buffer.split(/\n\n/);
                    this.buffer = events.pop() || ''; // 保留未完成部分

                    events.forEach(eventData =&gt; {
                        const lines = eventData.split('\n');
                        let textContent = '';

                        // 解析事件内容
                        lines.forEach(line =&gt; {
                            if (line.startsWith('data:')) {
                                try {
                                    const jsonData = JSON.parse(line.slice(5).trim());
                                    if (jsonData.output?.text) {
                                        textContent = jsonData.output.text;
                                    }
                                } catch(e) {
                                    console.error('JSON解析错误:', e.message);
                                }
                            }
                        });

                        if (textContent) {
                            // 添加换行符并推送
                            this.push(textContent + '\n');
                        }
                    });

                    callback();
                },
                flush(callback) {
                    if (this.buffer) {
                        this.push(this.buffer + '\n');
                    }
                    callback();
                }
            });
            sseTransformer.buffer = '';

            // 管道处理
            response.data
                .pipe(sseTransformer)
                .on('data', (textWithNewline) =&gt; {
                    process.stdout.write(textWithNewline); // 自动换行输出
                })
                .on('end', () =&gt; console.log(&quot;&quot;))
                .on('error', err =&gt; console.error(&quot;管道错误:&quot;, err));

        } else {
            console.log(&quot;请求失败，状态码:&quot;, response.status);
            response.data.on('data', chunk =&gt; console.log(chunk.toString()));
        }
    } catch (error) {
        console.error(`API调用失败: ${error.message}`);
        if (error.response) {
            console.error(`状态码: ${error.response.status}`);
            error.response.data.on('data', chunk =&gt; console.log(chunk.toString()));
        }
    }
}

callDashScope();
</code></pre></div></section></section><a id="c-3"></a><section><a id="c-3-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-31"></a><pre class="language-csharp"><code>using System.Net;
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID
        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            client.DefaultRequestHeaders.Add(&quot;X-DashScope-SSE&quot;, &quot;enable&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你是谁&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {&quot;&quot;incremental_output&quot;&quot;: true},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            Console.WriteLine(DateTime.Now.ToString(&quot;yyyy-MM-dd HH:mm:ss:fff&quot;));
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Post, url);
                request.Content = content;

                HttpResponseMessage response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(DateTime.Now.ToString(&quot;yyyy-MM-dd HH:mm:ss:fff&quot;));
                    using (var stream = await response.Content.ReadAsStreamAsync())
                    using (var reader = new StreamReader(stream))
                    {
                        string? line; // 声明为可空字符串
                        while ((line = await reader.ReadLineAsync()) != null)
                        {
                            if (line.StartsWith(&quot;data:&quot;))
                            {
                                string data = line.Substring(5).Trim();
                                Console.WriteLine(data);
                                Console.WriteLine(DateTime.Now.ToString(&quot;yyyy-MM-dd HH:mm:ss:fff&quot;));
                            }
                        }
                    }
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-3"></a><section><a id="go-3-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-32"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
	&quot;strings&quot;
	&quot;time&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体，其中incremental_output为是否开启流式响应
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;你是谁？&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{
			&quot;incremental_output&quot;: true,
		},
		&quot;debug&quot;: map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头,其中X-DashScope-SSE设置为enable，表示开启流式响应
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)
	req.Header.Set(&quot;X-DashScope-SSE&quot;, &quot;enable&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		body, _ := io.ReadAll(resp.Body)
		fmt.Println(string(body))
		return
	}

	// 处理流式响应
	reader := io.Reader(resp.Body)
	buf := make([]byte, 1024)
	for {
		n, err := reader.Read(buf)
		if n &gt; 0 {
			data := string(buf[:n])
			lines := strings.Split(data, &quot;\n&quot;)
			for _, line := range lines {
				line = strings.TrimSpace(line)
				if len(line) &gt;= 5 &amp;&amp; line[:5] == &quot;data:&quot; {
					timestamp := time.Now().Format(&quot;2006-01-02 15:04:05.000&quot;)
					fmt.Printf(&quot;%s: %s\n&quot;, timestamp, line[5:])
				} else if len(line) &gt; 0 {
					fmt.Println(line)
				}
			}
		}
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Printf(&quot;Error reading response: %v\n&quot;, err)
			break
		}
	}
}
</code></pre></section></section></section></section></section><a id="文件问答"></a><section><a id="文件问答-h4"></a><h4>文件问答</h4><p>指定<code>file_list</code>传入文件（文档、图片、音视频）URL，启用文件问答功能。</p><p><strong>应用配置：</strong>应用内需开启<strong>预解析文件</strong>开关。</p><a id="sec-tabs-8"></a><section><a id="python-4"></a><section><a id="python-4-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-33"></a><pre class="language-python"><code># 需要 dashscope 2.0.1 及以上版本
import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    stream = client.apps.completions.create(
        app_id='YOUR_APP_ID',  # 应用ID替换YOUR_APP_ID
        prompt='一句话总结文件内容',
        stream=True,  # 流式输出
        incremental_output=True, # 增量输出
        file_list=[&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3&quot;],
    )

    for response in stream:
        print('%s\n' % (response.text))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre><strong>响应示例</strong><a id="code-block-34"></a><pre class="language-json"><code>该文件是一条简短的欢迎
信息，内容为&quot;欢迎
与使用阿里云&quot;。
</code></pre></section><a id="java-4"></a><section><a id="java-4-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-35"></a><pre class="language-java"><code>// dashscope SDK 的版本 &gt;= 2.21.13；
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;YOUR_APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;一句话总结文件内容&quot;)
                .files(Arrays.asList(
                        &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3&quot;))
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());// 处理只输出文本text
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre><strong>响应示例</strong><a id="code-block-36"></a><pre class="language-json"><code>该文件是一条简短的欢迎信息，内容为&quot;欢迎与使用阿里云&quot;。
</code></pre></section><a id="curl-4"></a><section><a id="curl-4-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-37"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{YOUR_APP_ID}/completion \
        --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
        --header 'Content-Type: application/json' \
        --data '{
        &quot;input&quot;: {
            &quot;prompt&quot;: &quot;一句话总结文件内容&quot;,
            &quot;file_list&quot;:[&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3&quot;]
        },
        &quot;debug&quot;: {}
        }'
</code></pre><strong>响应示例</strong><a id="code-block-38"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;reject_status&quot;: false,
        &quot;session_id&quot;: &quot;545547dddcbf4296af0173da1a6e5a74&quot;,
        &quot;text&quot;: &quot;该文件是阿里云的欢迎提示，内容为\&quot;欢迎与使用阿里云\&quot;。&quot;
    },
    &quot;usage&quot;: {
        &quot;models&quot;: [
            {
                &quot;input_tokens&quot;: 103,
                &quot;model_id&quot;: &quot;qwen-plus-latest&quot;,
                &quot;output_tokens&quot;: 304
            }
        ]
    },
    &quot;request_id&quot;: &quot;6900cfac-0aa5-4c6e-aa9c-7a69f7b4d5bc&quot;
}
</code></pre></section></section></section><a id="视觉理解"></a><section><a id="视觉理解-h4"></a><h4>视觉理解</h4><p>通过 <code>image_list</code> 参数传入图像 URL 或 Data URL（Base64 编码）启用视觉理解功能。应用内需使用<strong><a href="../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a></strong>模型。</p><div><div><p><strong>说明</strong>支持使用 Base64 编码本地图像。将图像编码为 Base64 字符串后，按<code>data:[MIME_type];base64,{base64_image}</code>格式构建 Data URL 传入。<code>MIME_type</code> 必须与图像格式匹配。常见格式：PNG 使用 <code>image/png</code>，JPEG 使用 <code>image/jpeg</code>，WebP 使用 <code>image/webp</code>。</p></div></div><a id="sec-tabs-9"></a><section><a id="python-5"></a><section><a id="python-5-h4"></a><h4>Python</h4><strong>URL请求示例</strong><a id="code-block-39"></a><pre class="language-python"><code>import os
import dashscope
# 需要 dashscope 2.0.1 及以上版本
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 应用ID替换APP_ID
        prompt='这是什么',
        image_list=['https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg'],
    )
    print('%s\n' % (response.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre><strong>Base64 编码示例</strong><a id="code-block-40"></a><pre class="language-python"><code>import os
import base64
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

# 将本地图像编码为 Base64 字符串
def encode_image(image_path):
    with open(image_path, &quot;rb&quot;) as image_file:
        return base64.b64encode(image_file.read()).decode(&quot;utf-8&quot;)

# 编码本地图像
base64_image = encode_image(&quot;/path/to/your/image.jpeg&quot;)  # 替换为实际图像路径

# 构建 Data URL（注意：MIME type 需与图像格式匹配）
data_url = f&quot;data:image/jpeg;base64,{base64_image}&quot;

# 调用应用 API
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 应用ID替换APP_ID
        prompt='这张图片里有什么？',
        image_list=[data_url],  # 使用 Data URL
    )
    print('%s\n' % (response.text))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-5"></a><section><a id="java-5-h4"></a><h4>Java</h4><strong>URL请求示例</strong><a id="code-block-41"></a><pre class="language-java"><code>// 建议dashscope SDK 的版本 &gt;= 2.19.0；
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Arrays;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;这是什么？&quot;)
                .images(Arrays.asList(&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;))
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());// 处理只输出文本text
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre><strong>Base64 编码示例</strong><a id="code-block-42"></a><pre class="language-java"><code>// 建议dashscope SDK 的版本 &gt;= 2.19.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Base64;

public class Main {
    // 将本地图像编码为 Base64 字符串
    public static String encodeImage(String imagePath) throws IOException {
        byte[] imageBytes = Files.readAllBytes(Paths.get(imagePath));
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    public static void appCall() throws NoApiKeyException, InputRequiredException, IOException {
        // 编码本地图像
        String base64Image = encodeImage(&quot;/path/to/your/image.jpeg&quot;); // 替换为实际图像路径

        // 构建 Data URL（注意：MIME type 需与图像格式匹配）
        String dataUrl = &quot;data:image/jpeg;base64,&quot; + base64Image;

        ApplicationParam param = ApplicationParam.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;这张图片里有什么？&quot;)
                .images(Arrays.asList(dataUrl)) // 使用 Data URL
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;, result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException | IOException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-4"></a><section><a id="http-4-h4"></a><h4>HTTP</h4><a id="sec-tabs-10"></a><section><a id="curl-5"></a><section><a id="curl-5-h4"></a><h4>curl</h4><strong>URL请求示例</strong><a id="code-block-43"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;这是什么&quot;,
        &quot;image_list&quot;:[&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;]
    },
    &quot;debug&quot;: {}
}'
</code></pre><strong>Base64 编码示例</strong><a id="code-block-44"></a><pre class="language-bash"><code># 将本地图像编码为 Base64 字符串
base64_image=$(base64 -i /path/to/your/image.jpeg)  # macOS/Linux

# 构建 Data URL（注意：MIME type 需与图像格式匹配）
data_url=&quot;data:image/jpeg;base64,${base64_image}&quot;

# 调用应用 API
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data &quot;{
    \&quot;input\&quot;: {
        \&quot;prompt\&quot;: \&quot;这张图片里有什么？\&quot;,
        \&quot;image_list\&quot;: [\&quot;${data_url}\&quot;]
    },
    \&quot;debug\&quot;: {}
}&quot;
</code></pre></section><a id="php-4"></a><section><a id="php-4-h4"></a><h4>PHP</h4><strong>URL请求示例</strong><a id="code-block-45"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        &quot;prompt&quot; =&gt; &quot;这是什么&quot;,
        &quot;image_list&quot; =&gt; [&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;],
    ],
    &quot;debug&quot; =&gt; [],
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre><strong>Base64 编码示例</strong><a id="code-block-46"></a><pre class="language-php"><code>&lt;?php
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID';

function encodeImage($imagePath) {
    if (!file_exists($imagePath)) die(&quot;Error: Image file not found&quot;);
    return base64_encode(file_get_contents($imagePath));
}

$base64Image = encodeImage(&quot;/path/to/your/image.jpeg&quot;);
$dataUrl = &quot;data:image/jpeg;base64,&quot; . $base64Image;

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;
$data = [&quot;input&quot; =&gt; [&quot;prompt&quot; =&gt; &quot;这张图片里有什么？&quot;, &quot;image_list&quot; =&gt; [$dataUrl]], &quot;debug&quot; =&gt; []];

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json', 'Authorization: Bearer ' . $api_key]);

$response = curl_exec($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($status_code == 200) {
    $response_data = json_decode($response, true);
    echo $response_data['output']['text'];
}
?&gt;
</code></pre></section><a id="node-js-4"></a><section><a id="node-js-4-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-47"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>URL请求示例</strong><a id="code-block-48"></a><pre class="language-javascript"><code>import axios from 'axios';
async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';//替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;这是什么&quot;,
            image_list: [&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;],
        },
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre><strong>Base64 编码示例</strong><a id="code-block-49"></a><pre class="language-javascript"><code>import axios from 'axios';
import fs from 'fs';

async function callWithBase64() {
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';

    const imageBuffer = fs.readFileSync('/path/to/your/image.jpeg');
    const base64Image = imageBuffer.toString('base64');
    const dataUrl = `data:image/jpeg;base64,${base64Image}`;

    const response = await axios.post(
        `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`,
        { input: { prompt: &quot;这张图片里有什么？&quot;, image_list: [dataUrl] } },
        { headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' } }
    );

    console.log(response.data.output.text);
}

callWithBase64();
</code></pre></section><a id="c-4"></a><section><a id="c-4-h4"></a><h4>C#</h4><strong>URL请求示例</strong><a id="code-block-50"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);;
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;这是什么&quot;&quot;,
                    &quot;&quot;image_list&quot;&quot;: [&quot;&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;&quot;]
                }},
                &quot;&quot;parameters&quot;&quot;: {{
                }},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre><strong>Base64 编码示例</strong><a id="code-block-51"></a><pre class="language-csharp"><code>using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        var apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;);
        var appId = &quot;APP_ID&quot;;

        byte[] imageBytes = File.ReadAllBytes(&quot;/path/to/your/image.jpeg&quot;);
        var base64Image = Convert.ToBase64String(imageBytes);
        var dataUrl = $&quot;data:image/jpeg;base64,{base64Image}&quot;;

        using var client = new HttpClient();
        client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

        var json = $@&quot;{{&quot;&quot;input&quot;&quot;: {{&quot;&quot;prompt&quot;&quot;: &quot;&quot;这张图片里有什么？&quot;&quot;, &quot;&quot;image_list&quot;&quot;: [&quot;&quot;{dataUrl}&quot;&quot;]}}, &quot;&quot;debug&quot;&quot;: {{}}}}&quot;;
        var content = new StringContent(json, Encoding.UTF8, &quot;application/json&quot;);
        var response = await client.PostAsync($&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;, content);

        Console.WriteLine(await response.Content.ReadAsStringAsync());
    }
}
</code></pre></section><a id="go-4"></a><section><a id="go-4-h4"></a><h4>Go</h4><strong>URL请求示例</strong><a id="code-block-52"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]interface{}{
			&quot;prompt&quot;:     &quot;这是什么&quot;,
			&quot;image_list&quot;: []string{&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;},
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre><strong>Base64 编码示例</strong><a id="code-block-53"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/base64&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot;

	imageData, _ := os.ReadFile(&quot;/path/to/your/image.jpeg&quot;)
	base64Image := base64.StdEncoding.EncodeToString(imageData)
	dataUrl := fmt.Sprintf(&quot;data:image/jpeg;base64,%s&quot;, base64Image)

	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]interface{}{&quot;prompt&quot;: &quot;这张图片里有什么？&quot;, &quot;image_list&quot;: []string{dataUrl}},
	}

	jsonData, _ := json.Marshal(requestBody)
	req, _ := http.NewRequest(&quot;POST&quot;, fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId), bytes.NewBuffer(jsonData))
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	client := &amp;http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Println(string(body))
}
</code></pre></section></section></section></section></section><a id="自定义参数传递"></a><section><a id="自定义参数传递-h4"></a><h4>自定义参数传递</h4><p>通过<code>biz_params</code>传递自定义参数。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#b774db7cdc0aa">调用智能体应用-传递自定义参数</a>。</p><a id="sec-tabs-11"></a><section><a id="python-6"></a><section><a id="python-6-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-54"></a><pre class="language-python"><code>import os
import dashscope
# 需要 dashscope 2.0.1 及以上版本
from dashscope import DashScopeError

client = dashscope.Client(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
biz_params = {
    # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换&lt;TOOL_ID&gt;
    &quot;user_defined_params&quot;: {
        &quot;&lt;TOOL_ID&gt;&quot;: {
            &quot;article_index&quot;: 2}}}
try:
    response = client.apps.completions.create(
        app_id='APP_ID',
        prompt='寝室公约内容',
        biz_params=biz_params)
    print('%s\n' % (response.text))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-6"></a><section><a id="java-6-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-55"></a><pre class="language-java"><code>import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        String bizParams =
                // 智能体应用的自定义插件输入参数传递，自定义的插件ID替换&lt;TOOL_ID&gt;
                &quot;{\&quot;user_defined_params\&quot;:{\&quot;&lt;TOOL_ID&gt;\&quot;:{\&quot;article_index\&quot;:2}}}&quot;;
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;寝室公约内容&quot;)
                .bizParams(JsonUtils.parse(bizParams))
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-5"></a><section><a id="http-5-h4"></a><h4>HTTP</h4><strong>请求示例</strong><a id="code-block-56"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;寝室公约内容&quot;,
        &quot;biz_params&quot;:
        {
            &quot;user_defined_params&quot;:
            {
                &quot;&lt;TOOL_ID&gt;&quot;:
                    {
                    &quot;article_index&quot;: 2
                    }
            }
        }
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;:{}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。&lt;TOOL_ID&gt;替换为插件ID。</p></blockquote></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f304e81314ngo"></a><h3>响应对象</h3><p>调用失败时，Python SDK 会抛出 <code>DashScopeError</code>，可通过 <code>e.code</code>/<code>e.status_code</code>/<code>e.message</code>/<code>e.request_id</code> 获取错误信息。</p></td><td rowspan="4"><strong>成功响应示例</strong><p>以下为 Python SDK 2.0 响应对象形态（HTTP 调用时，<code>text</code>/<code>finish_reason</code>/<code>session_id</code> 等字段位于 <code>output</code> 对象内）。</p><a id="code-block-57"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;fdfc3182-bc9d-4b45-a287-cd83b13aca02&quot;,
    &quot;text&quot;: &quot;你好！我是千问，阿里巴巴集团旗下的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等。有什么需要我帮忙的吗？&quot;,
    &quot;finish_reason&quot;: &quot;stop&quot;,
    &quot;session_id&quot;: &quot;cbb2e26ac4cc4cc3b2d114e1f73c127e&quot;,
    &quot;thoughts&quot;: null,
    &quot;doc_references&quot;: null,
    &quot;workflow_message&quot;: null,
    &quot;usage&quot;: {
        &quot;models&quot;: [
            {
                &quot;model_id&quot;: &quot;qwen-plus-latest&quot;,
                &quot;input_tokens&quot;: 142,
                &quot;output_tokens&quot;: 296
            }
        ]
    }
}
</code></pre><strong>异常响应示例</strong><p>在访问请求出错的情况下，Python SDK 会抛出异常，异常的 <code>code</code> 和 <code>message</code> 属性会指明错误原因。</p><p>此处展示未传入正确<code>API-KEY</code>的异常响应示例。</p><a id="code-block-58"></a><pre class="language-json"><code>request_id=1d14958f-0498-91a3-9e15-be477971967b,
code=401,
message=Invalid API-key provided.
</code></pre></td></tr><tr><td><p><strong>request_id</strong> <code>string</code></p><p>本次调用的唯一标识符。</p><blockquote><p>Java SDK返回参数为<code>requestId</code>。</p></blockquote></td></tr><tr><td><p><strong>output</strong> <code>object</code></p><p>调用结果信息。</p><a id="accordion-output属性"></a><section><p>output属性</p><div><p><strong>text</strong> <code>string</code></p><p>模型生成的回复内容。</p><p><strong>finish_reason</strong> <code>string</code></p><p>完成原因。</p><p><code>stop</code>为自然结束（遇预设标记），<code>null</code>为强制中断（如达到最大长度限制或手动停止）。</p><p><strong>session_id</strong><code>string</code></p><p>当前对话的唯一标识。</p><p>在后续请求中传入，可携带历史对话记录。</p><p><strong>thoughts</strong><code>array</code></p><p>调用时将<code>has_thoughts</code>参数设置为True，即可在<code>thoughts</code>中查看<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>的思考过程。</p><a id="accordion-thoughts属性"></a><section><p>thoughts属性</p><div><p><strong>thought</strong> <code>string</code></p><p>模型的思考过程。</p><strong>使用步骤</strong><ol><li>控制台应用内选择<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>，并成功发布；</li><li>API 调用时将 <code>has_thoughts</code> 参数设为 <code>True</code>。</li></ol><p><strong>action_type</strong> <code>string</code></p><p>大模型返回的执行步骤类型。如reasoning表示<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>的思考过程。</p><p><strong>action_name</strong> <code>string</code></p><p>执行的action名称，如思考过程。</p><p><strong>action</strong> <code>string</code></p><p>执行的步骤。</p><p><strong>action_input_stream</strong> <code>string</code></p><p>入参的流式结果。</p><p><strong>action_input</strong> <code>string</code></p><p>输入参数。</p></div></section></div></section></td></tr><tr><td><p><strong>doc_references</strong> <code>null</code></p><p>新版智能体应用（Agent 2.0）将知识库统一为工具由智能体自主调用，该字段固定返回 <code>null</code>（与旧版智能体应用 Agent 1.0 不同）。如需在回答中展示知识来源，请在应用配置中开启<strong>展示回答来源</strong>功能，引用信息将以角标形式嵌入回答文本中。</p></td></tr><tr><td><p><strong>usage</strong> <code>object</code></p><p>表示本次请求使用的数据信息。</p><a id="accordion-usage属性"></a><section><p>usage属性</p><div><p><strong>models</strong><code>array</code></p><p>本次调用的模型信息。</p><a id="accordion-models属性"></a><section><p>models属性</p><div><p><strong>model_id</strong> <code>string</code></p><p>本次应用调用到的模型 ID。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>用户输入文本转换成Token后的长度。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>模型生成回复转换为Token后的长度。</p></div></section></div></section></td></tr></tbody></table>

<a id="qpm限制"></a>

<a id="qpm_limit_h2_new_agent"></a>

## QPM限制

单应用默认QPM（每分钟请求数）为15000。

<a id="错误码"></a>

<a id="97e145aeabbwf"></a>

## 错误码

如果调用失败并返回报错信息，请参阅[错误码](../model-api-reference/preparations/error-code.md)进行解决。
