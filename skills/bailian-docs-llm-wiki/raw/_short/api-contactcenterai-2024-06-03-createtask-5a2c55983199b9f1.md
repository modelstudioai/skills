# CreateTask - 通过上传离线任务数据进行通义晓蜜CCAI-对话分析

通过创建离线异步任务，进行对话分析。应用调用支持 HTTP 调用来完成客户的响应。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

<a id="前提条件"></a>

## 前提条件

-   1.已开通通义晓蜜 CCAI-对话分析 AIO 服务。
-   2.已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：获取 APP-ID 和 WORKSPACE-ID。

<a id="注意事项"></a>

## 注意事项

-   1.目前任务数据在服务端保存时间为 90 天。
-   2.对话内容字数限制为 2 万字，超过部分会自动截断。
-   3.音频文件建议使用 8k 采样率，使用其他采样率会影响最终效果。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/CreateTask)

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

当前API暂无授权信息透出。

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/ccai/app/{appId}/createTask HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>否</td><td><div><p>业务空间 ID</p></div></td><td>llm-ik******RVYCKzt</td></tr><tr><td>appId</td><td>string</td><td>否</td><td><div><p>应用 ID</p></div></td><td>a070a49c681f4a95a0f0*********35c</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求 Body</p></div></td><td></td></tr><tr><td>dialogue</td><td>object</td><td>否</td><td><div><p>对话内容列表</p></div></td><td></td></tr><tr><td>sentences</td><td>array&lt;object&gt;</td><td>是</td><td><div><p>对话内容</p></div></td><td></td></tr><tr><td></td><td>object</td><td>否</td><td><div><p>对话内容</p></div></td><td></td></tr><tr><td>role</td><td>string</td><td>是</td><td><div><p>通话角色</p><ul><li>user：客户</li><li>agent：客服</li><li>system：系统消息</li></ul></div></td><td>user</td></tr><tr><td>text</td><td>string</td><td>是</td><td><div><p>对话文本</p></div></td><td>请问怎么申请新卡</td></tr><tr><td>sessionId</td><td>string</td><td>否</td><td><div><p>客服会话 sessionId</p></div></td><td>session-01</td></tr><tr><td>examples</td><td>object</td><td>否</td><td><div><p>指令示例</p></div></td><td></td></tr><tr><td>output</td><td>string</td><td>否</td><td><div><p>输出示例</p></div></td><td>问题描述：询问2.2更新时间，处理方案：已告知</td></tr><tr><td>sentences</td><td>array&lt;object&gt;</td><td>是</td><td><div><p>对话内容示例</p></div></td><td></td></tr><tr><td></td><td>object</td><td>是</td><td><div><p>对话内容示例</p></div></td><td></td></tr><tr><td>role</td><td>string</td><td>是</td><td><div><p>通话角色</p><ul><li>user：客户</li><li>agent：客服</li><li>system：系统消息</li></ul></div></td><td>user</td></tr><tr><td>text</td><td>string</td><td>是</td><td><div><p>对话文本</p></div></td><td>什么时候更新</td></tr><tr><td>fields</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>字段结构信息</p></div></td><td></td></tr><tr><td></td><td>object</td><td>是</td><td><div><p>字段结构信息</p></div></td><td></td></tr><tr><td>code</td><td>string</td><td>否</td><td><div><p>字段编码</p></div></td><td>phoneNumber</td></tr><tr><td>desc</td><td>string</td><td>是</td><td><div><p>字段描述</p></div></td><td>用户来电咨询的原因分类，主要有投诉、咨询、政策建议等。</td></tr><tr><td>enumValues</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>枚举值列表</p></div></td><td></td></tr><tr><td></td><td>object</td><td>是</td><td><div><p>枚举值列表</p></div></td><td></td></tr><tr><td>desc</td><td>string</td><td>是</td><td><div><p>枚举描述</p></div></td><td>客户有新的需求/新的场景，客服跟进沟通需求细节</td></tr><tr><td>enumValue</td><td>string</td><td>是</td><td><div><p>枚举值</p></div></td><td>新业务拓展</td></tr><tr><td>name</td><td>string</td><td>是</td><td><div><p>字段名称</p></div></td><td>来电原因类型</td></tr><tr><td>modelCode</td><td>string</td><td>是</td><td><div><p>模型 code</p></div></td><td>tyxmTurbo</td></tr><tr><td>resultTypes</td><td>array</td><td>否</td><td><div><p>大模型处理类型</p></div></td><td></td></tr><tr><td></td><td>string</td><td>是</td><td><div><p>summary-对话摘要，title-标题生成、fields-字段信息抽取、keywords -关键字抽取，service_inspection-服务质检、question_solution-问题和解决方案、questions_and_answer-QA 抽取、custom_prompt-自定义指令</p></div></td><td>summary</td></tr><tr><td>serviceInspection</td><td>object</td><td>否</td><td><div><p>服务质检结构信息</p></div></td><td></td></tr><tr><td>inspectionContents</td><td>array&lt;object&gt;</td><td>是</td><td><div><p>服务质检维度结构</p></div></td><td></td></tr><tr><td></td><td>object</td><td>是</td><td><div><p>服务质检维度结构</p></div></td><td></td></tr><tr><td>content</td><td>string</td><td>是</td><td><div><p>服务质检维度描述</p></div></td><td>客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。</td></tr><tr><td>title</td><td>string</td><td>是</td><td><div><p>服务质检维度名称</p></div></td><td>客服是否过度承诺</td></tr><tr><td>inspectionIntroduction</td><td>string</td><td>是</td><td><div><p>服务质检场景详细介绍及描述</p></div></td><td>请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等</td></tr><tr><td>sceneIntroduction</td><td>string</td><td>是</td><td><div><p>服务质检场景</p></div></td><td>保险销售场景</td></tr><tr><td>taskType</td><td>string</td><td>是</td><td><div><p>任务类型 audio -语音文件 ，text - 文本</p></div></td><td>text</td></tr><tr><td>templateIds</td><td>array</td><td>否</td><td><div><p>模版 id 列表</p></div></td><td></td></tr><tr><td></td><td>string</td><td>是</td><td><div><p>模版 id，模版 id 和指令任务类型同时存在时，优先使用模版 id</p></div></td><td>34</td></tr><tr><td>transcription</td><td>object</td><td>否</td><td><div><p>语音类型执行参数</p></div></td><td></td></tr><tr><td>autoSplit</td><td>integer</td><td>否</td><td><div><p>单轨音频自动区分通话人，取值：0 为自动识别，取值：1 为不自动识别；默认：1；备注：只适用于 8k 采样率音频文件</p></div></td><td>1</td></tr><tr><td>clientChannel</td><td>integer</td><td>否</td><td><div><p>适用于双轨录音，指定客户角色的轨道编号，取值：0、1，默认 1，即第 1 轨为客户；通常音轨都是从 0 开始编号，2 个轨就是 0，1；具体 0 是客服还是客户，需要您自行确认。**若使用此参数，请务必传入 autoSplit 参数，值为 0。**单轨文件忽略此参数。</p></div></td><td>1</td></tr><tr><td>fileName</td><td>string</td><td>是</td><td><div><p>文件名。</p></div></td><td>sss.mp3</td></tr><tr><td>serviceChannel</td><td>integer</td><td>否</td><td><div><p>适用于双轨录音，指定客服角色的轨道编号，取值：0、1，默认 0，即第 0 轨为客服；通常音轨都是从 0 开始编号，2 个轨就是 0，1；具体 0 是客服还是客户，需要您自行确认。**若使用此参数，请务必传入 autoSplit 参数，值为 0。**若单轨文件忽略此参数。</p></div></td><td>1</td></tr><tr><td>serviceChannelKeywords</td><td>array</td><td>否</td><td><div><p>多数情况下适用于单轨录音，设置一组客服可能说的关键词列表（请确保选择那些区别性比较高的关键词），通过对转写文本从上到下逐句分析，当一句话命中某一个关键词时，则判定该句的角色为客服，则另一个角色就是客户。</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>多数情况下适用于单轨录音，设置一组客服可能说的关键词列表（请确保选择那些区别性比较高的关键词），通过对转写文本从上到下逐句分析，当一句话命中某一个关键词时，则判定该句的角色为客服，则另一个角色就是客户。</p></div></td><td>你好</td></tr><tr><td>voiceFileUrl</td><td>string</td><td>是</td><td><div><p>文件地址</p></div></td><td><a href="http://1111.com/sss.mp3">http://1111.com/sss.mp3</a></td></tr><tr><td>asrModelCode</td><td>string</td><td>否</td><td><div><p>语音转写模型，取值 asr （小模型），paraformer（大模型）</p></div></td><td>asr</td></tr><tr><td>level</td><td>string</td><td>否</td><td><div><p>语音转写优先级</p></div></td><td>low</td></tr><tr><td>vocabularyId</td><td>string</td><td>否</td><td><div><p>语音热词 id</p></div></td><td>esnvknv*****skdnvjksd</td></tr><tr><td>roleIdentification</td><td>boolean</td><td>否</td><td><div><p>自动识别通话角色，true 为自动识别，false 为不自动识别。默认：false</p></div></td><td>true</td></tr><tr><td>languageHints</td><td>string</td><td>否</td><td><div><p>识别语言，默认值为中文普通话，其他支持的语种和方言请联系客服</p></div></td><td>zh</td></tr><tr><td>customPrompt</td><td>string</td><td>否</td><td><div><p>自定义指令</p></div></td><td>对通话内容进行总结</td></tr><tr><td>variables</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>变量列表</p></div></td><td></td></tr><tr><td></td><td>object</td><td>否</td><td><div><p>变量列表</p></div></td><td></td></tr><tr><td>variableCode</td><td>string</td><td>否</td><td><div><p>变量 code</p></div></td><td>name</td></tr><tr><td>variableValue</td><td>string</td><td>否</td><td><div><p>变量值</p></div></td><td>张三</td></tr><tr><td>categoryTags</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>标签分类列表</p></div></td><td></td></tr><tr><td></td><td>object</td><td>否</td><td><div><p>标签分类列表</p></div></td><td></td></tr><tr><td>tagName</td><td>string</td><td>否</td><td><div><p>标签名称</p></div></td><td>客服过度承诺</td></tr><tr><td>tagDesc</td><td>string</td><td>否</td><td><div><p>标签描述</p></div></td><td>客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为</td></tr><tr><td>responseFormatType</td><td>string</td><td>否</td><td><div><p>输出结果格式化类型，jsonObject-json 结构，text-原始字符串</p></div></td><td>jsonObject</td></tr><tr><td>callBackUrl</td><td>string</td><td>否</td><td><div><p>任务完成后回调参数</p></div></td><td>123.456.com/callback</td></tr></tbody></table>

<a id="语音识别参数说明"></a>

<a id="api-detail-39"></a>

## 语音识别参数说明

上传语音文件时，需要通过 serviceChannel 或 clientChannel 设置不同角色的音轨，后台服务通过音轨来识别角色。或是通过 serviceChannelKeywords 设置客服通话中的关键字，后台服务通过客服通话中的关键字来识别角色。

<a id="回调参数说明"></a>

## 回调参数说明

假设调用方传入的回调地址是：[http://aliyun.com/callback，那么回调时的完整](http://aliyun.com/callback%EF%BC%8C%E9%82%A3%E4%B9%88%E5%9B%9E%E8%B0%83%E6%97%B6%E7%9A%84%E5%AE%8C%E6%95%B4) URL 为 [http://aliyun.com/callback?taskId=xxx&amp;timestamp=xxx&amp;taskType=xxx&amp;signature=YOUR\_SIGNATURE&amp;&amp;success=xxx，其中：](http://aliyun.com/callback?taskId=xxx&amp;timestamp=xxx&amp;taskType=xxx&amp;signature=YOUR_SIGNATURE&amp;&amp;success=xxx%EF%BC%8C%E5%85%B6%E4%B8%AD%EF%BC%9A)

-   taskId：为任务 ID
-   timestamp：为调用时的时间戳，单位：毫秒
-   taskType：为任务类型
-   success：为是否成功
-   signature：为签名，调用方可用来判断请求是否来自阿里云；计算说明：将 taskId=xxx&timestamp=xxx&aliUid=xxx 进行 md5+base64 加密，注意顺序；调用方接到回调后，taskId 和 timestamp 可以从回调 URL 中获取，aliUid 即为阿里云主账号 ID。通过计算来比对自己计算出的 signature，与 URL 中的 signature 是否一致，详见下方 Java 代码示例。

<a id="code-block-2"></a>

```java
import java.net.URLEncoder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;
import org.apache.commons.codec.binary.Base64;

public class Sample {

    public static void signature() {
        long timestamp = System.currentTimeMillis();
        String taskId = "xxx";
        String aliUid = "xxx";
        // 将 taskId=xxx&timestamp=xxx&aliUid=xxx 进行 md5 + base64 加密，放在 signature 字段
        String signature;
        try {
            signature = URLEncoder.encode(md5Base64("taskId=" + taskId + "&timestamp=" + timestamp + "&aliUid=" + aliUid), "utf-8");
            System.out.println(signature);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String md5Base64(String str) throws NoSuchAlgorithmException {
        //string 编码必须为 utf-8
        byte[] utfBytes = str.getBytes(StandardCharsets.UTF_8);
        MessageDigest mdTemp = MessageDigest.getInstance("MD5");
        mdTemp.update(utfBytes);
        byte[] md5Bytes = mdTemp.digest();
        return Base64.encodeBase64String(md5Bytes);
    }
}
```

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| data | object | 数据 |  |
| taskId | string | 任务 ID。 | 20240905-\*\*\*\*\*\*\*\*-93E9-5D45-B4EF-045743A34071 |
| requestId | string | 请求 id | 9F1DB065-AE0D-5EE3-B1AF-48632CB0831C |
| success | string | 是否成功 | True |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```text
{
  "data": {
    "taskId": "20240905-********-93E9-5D45-B4EF-045743A34071"
  },
  "requestId": "9F1DB065-AE0D-5EE3-B1AF-48632CB0831C",
  "success": "True"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | CCAI.InvalidParam.NotExist | The specified parameter %s is not valid. | 请求API的参数不存在 |
| 400 | CCAI.ParamInvalid.IllegalParamValue | The parameter value of the request API is illegal %s. | 请求API的参数不合法 |
| 400 | CCAI.Throttling.Qpm | Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475). | 触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。 |
| 400 | CCAI.Throttling.Qps | Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475). | 触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。 |
| 403 | CCAI.IllegalPermission.NoAuth | User not authorized to operate on the specified resource. | 该用户未被授权可操作指定资源 |
| 403 | CCAI.ParamNotfound.MissParam | Parameter verification failed, The specified parameter %s is missing. | 参数校验失败，指定参数缺失。 |
| 403 | CCAI.TenantPermission.NoAuth | The current account does not have the permission to specify the business space. Please authorize the business space permission. | 当前账号没有指定业务空间的权限，请进行业务空间权限授权。 |
| 429 | Ccai.Throttling.Qps | Trigger current QPS limit, pay API please buy higher QPS, free API if you have special requirements, please contact us through the DingTalk group (62730018475). | 无效错误码，后续下线 |
| 500 | CCAI.InternalError | The request processing has failed due to some unknown error, exception or failure. | 系统内部错误，请稍后重试 |

访问[错误中心](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode)查看更多错误码。
