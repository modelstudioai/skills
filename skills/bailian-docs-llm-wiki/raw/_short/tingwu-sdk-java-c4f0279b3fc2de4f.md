# 服务端Java SDK

本文介绍通义听悟 Java SDK，帮助开发者快速调用服务。

<a id="前提条件"></a>

<a id="8a24f2ed09vr0"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)（DashScope版本号须>=2.21.1）

<a id="接口说明"></a>

<a id="a9c2d00f626mo"></a>

## 接口说明

<a id="tingwuparam-java"></a>

<a id="9d8aa23203p61"></a>

### TingWuParam.java

参数配置类。以[汽车销售服务洞察](tingwu-automotive-service-insights-94d0acc8e49a880f.md)为例，创建任务主要参数如下，更多参数说明请参见[汽车销售服务洞察API参考](tingwu-automotive-service-insights-api-86d5370ec77024c9.md)或[购车客户画像API参考](tingwu-automotive-customer-profile-api-9e1f3b05a5915147.md)：

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义业务类型</p><p>具体参数请参见API参考</p></td><td><p>tingwu-automotive-service-insights</p></td></tr><tr><td><p>input</p></td><td><p>object</p></td><td><p>是</p></td><td><p>传入相关业务参数</p></td><td></td></tr><tr><td><p>input.fileUrl</p></td><td><p>string</p></td><td rowspan="3"><p>3选1</p></td><td><p>待分析文件oss URL地址，sdk调用</p></td><td><p>https://<em><strong>.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Expires=</strong></em>&amp;Signature=YOUR_SIGNATURE</p></td></tr><tr><td><p>input.text</p></td><td><p>string</p></td><td><p>待分析文本</p></td><td><p>每行必须按照如下格式：</p><p>${发言人名称}: ${发言人内容}</p><p>例子比如：</p><a id="code-block"></a><pre class="language-text"><code>张3: 我想买一个SUV汽车
李4: 想要什么价位的？
</code></pre></td></tr><tr><td><p>input.dataId</p></td><td><p>string</p></td><td><p>关联已上传并解析完成的任务</p></td><td></td></tr><tr><td><p>input.appId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>应用id</p></td><td></td></tr><tr><td><p>input.task</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义任务类型：</p><ul><li>createTask：表示创建任务</li><li>getTask：表示获取任务结果</li></ul></td><td><p>createTask</p></td></tr><tr><td><p>parameters</p></td><td><p>object</p></td><td><p>否</p></td><td><p>请求参数（若传入空对象则复用已发布上线的配置项）</p><p>具体参数请参见API参考</p></td><td></td></tr></tbody></table>

<a id="示例代码"></a>

<a id="8b67acda1apgy"></a>

#### 示例代码

<a id="code-block-2"></a>

```java
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.multimodal.tingwu.TingWuParam;

//构建自定义 Input
public static Map<String, Object> buildCustomInput(String appId) {
        Map<String, Object> params = new HashMap<>();
        params.put("fileUrl", "http://demo.com/test.mp3");
        params.put("appId", appId);
        params.put("task", "createTask");
        //设置其他参数
        return params;
}
//构建 TingWuParam
TingWuParam param = TingWuParam.builder().
    model("tingwu-automotive-service-insights")
    .input(buildCustomInput("your_app_id"))
    .parameters(new HashMap<>())  //设置parameters参数
    .apiKey("your_api_key")
    .build();
```

<a id="tingwu-java"></a>

<a id="a01efde01al2m"></a>

### TingWu.java

-   听悟 Http服务接口类。

<a id="code-block-3"></a>

```java
/**
 * the tingwu client with baseUrl
 * param protocol : http or websocket, default should http
 * param baseUrl : custom server host
 */
public TingWu(String protocol, String baseUrl)
```

-   发送请求，返回[响应结果](tingwu-sdk-java-c4f0279b3fc2de4f.md#16ca9e9081zuf)。

<a id="code-block-4"></a>

```java
/**
 * Call the server to get the whole result, only http protocol
 * param param: the TingWuParam
 * return DashScopeResult
 */
public DashScopeResult call(TingWuParam param)
```

<a id="响应结果"></a>

<a id="16ca9e9081zuf"></a>

## 响应结果

以[汽车销售服务洞察](tingwu-automotive-service-insights-94d0acc8e49a880f.md)为例，主要返回参数如下，更多说明请参见[汽车销售服务洞察API参考](tingwu-automotive-service-insights-api-86d5370ec77024c9.md)或[购车客户画像API参考](tingwu-automotive-customer-profile-api-9e1f3b05a5915147.md)：

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>object</p></td><td></td><td></td></tr><tr><td><p>output.dataId</p></td><td><p>string</p></td><td><p>任务id</p></td><td></td></tr><tr><td><p>output.status</p></td><td><p>string</p></td><td><ul><li><p>0：成功</p></li><li><p>1：进行中</p></li><li><p>2：失败</p></li></ul></td><td><p>0</p></td></tr><tr><td><p>usage</p></td><td><p>object</p></td><td></td><td></td></tr><tr><td><p>code</p></td><td><p>string</p></td><td><p>错误码</p></td><td><p>InvalidParameter</p></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td><p>Agent Input text format error.</p></td></tr><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求id</p></td><td><p>f97ee37d-0f9c-9b93-b6bf-bd263a232bf9</p></td></tr></tbody></table>

响应结果示例：

<a id="code-block-5"></a>

```json
{
    "output": {
        "dataId": "dj***"
    },
    "usage": {},
    "request_id": "8313c0bc-ff3f-98e8-b87a-0118f6fe3049"
}
```
