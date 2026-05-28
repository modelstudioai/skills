# 妙笔API最佳实践

本文提供妙笔写作链路 API的几个最佳实践，帮助您快速入门并开发您自己的业务应用。

## 前提条件

-   已开通服务，开通地址：[https://common-buy.aliyun.com/?spm=a2c4g.11186623.0.0.225a777dIkFbJA&commodityCode=sfm\_miaobi\_public\_cn&request={%22guige%22:%22try%22}](https://common-buy.aliyun.com/?spm=a2c4g.11186623.0.0.225a777dIkFbJA&commodityCode=sfm_miaobi_public_cn&request={%22guige%22:%22try%22})；
    
-   [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)；
    
-   [获取 AccessKey ID、AccessKey Secret](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)；
    
-   引入妙笔SDK [注意获取最新SDK版本](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)；
    

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-aimiaobi20230801</artifactId>
  <version>1.0.103</version>
</dependency>
```

## 1、直接生成文章

基于妙笔提供的API，本节通过直接生成文章场景来帮助您熟悉API的使用。

生成调用demo如下：

-   Java：
    

```
package org.example.writing;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.ResponseIterable;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.List;

public class RunWritingV2DirectWritingDemo {
    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("DOMAIN", "aimiaobi.cn-beijing.aliyuncs.com");

    public static AsyncClient asyncClient() {
        return AsyncClient.builder().credentialsProvider(
                StaticCredentialProvider.create(Credential.builder().accessKeyId(ALIBABA_CLOUD_ACCESS_KEY_ID).accessKeySecret(ALIBABA_CLOUD_ACCESS_KEY_SECRET).build())
        ).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(
                ClientOverrideConfiguration.create().setProtocol("HTTPS").setEndpointOverride(ENDPOINT)
        ).build();
    }

    public static void main(String[] args) {
        directWriting();
    }

    public static void directWriting() {
        String prompt = "写一个关于机器学习的文章";
        RunWritingV2Request.Builder builder = RunWritingV2Request.builder().workspaceId(WORKSPACE_ID);
        //启用联网溯源与溯源
        builder.sourceTraceMethod("modelSourceTrace").useSearch(true);
        builder.prompt(prompt);

        AsyncClient client = asyncClient();

        ResponseIterable<RunWritingV2ResponseBody> runWritingV2ResponseBodies = client.runWritingV2WithResponseIterable(builder.build());
        GenerateTraceability generateTraceability = null;
        for (RunWritingV2ResponseBody item : runWritingV2ResponseBodies) {
            System.out.println(JSONObject.toJSONString(item));
            if (item.getHeader().getErrorMessage() != null) {
                System.out.println("写作失败：" + item.getHeader().getErrorMessage());
                break;
            }
            if ("task-progress-start-generating".equals(item.getHeader().getEvent())) {
                System.out.println(item.getPayload().getOutput().getText());
            }

            generateTraceability = item.getPayload().getOutput().getGenerateTraceability();
        }
        if (generateTraceability != null) {
            //模型实际引用的文章列表
            List<GenerateTraceability.News> news = generateTraceability.getNews();
            System.out.println(
                    JSONObject.toJSONString(news)
            );
        }
    }

}
```

-   Python：
    

```
import os
from alibabacloud_tea_openapi_sse.client import Client as OpenApiClient
from alibabacloud_tea_openapi_sse import models as open_api_models
from alibabacloud_tea_util_sse import models as open_api_util_models
import asyncio
import json

endpoint = 'aimiaobi.cn-beijing.aliyuncs.com'
# 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
# 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')

access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')

workspace_id = os.environ.get('WORKSPACE_ID')

# 详情接口文档请参考：https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunWritingV2?spm=a2c4g.11186623.0.0.201c715eKrroz5&RegionId=cn-beijing

def _create_client() -> OpenApiClient:
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint
    )
    return OpenApiClient(config)

def create_sse_api_info(action) -> open_api_models.Params:
    """
    API 相关
    @param path: params
    @return: OpenApi.Params
    """
    params = open_api_models.Params(
        # 接口名称
        action=action,
        # 接口版本
        version='2023-08-01',
        # 接口协议
        protocol='HTTPS',
        # 接口 HTTP 方法
        method='POST',
        auth_type='AK',
        style='RPC',
        pathname="",
        # 接口请求体内容格式,
        req_body_type='formData',
        # 接口响应体内容格式,
        body_type='sse'
    )
    return params

class SseClient:
    def __init__(self) -> None:
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        self.endpoint = endpoint
        self._runtime = open_api_util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = _create_client()

    async def run_writing(self, body):
        request = open_api_models.OpenApiRequest(body=body)
        return self._client.call_sse_api_async(params=create_sse_api_info("RunWritingV2"), request=request,
                                               runtime=self._runtime)

async def test_run_writing():
    client = SseClient()
    # 直接写作
    writing_params = {
        "Prompt": "写一个关于机器学习的文章",
        "UseSearch": True,
        "SourceTraceMethod": "modelSourceTrace",
        "WorkspaceId": workspace_id
    }
    async for item in await  client.run_writing(writing_params):
        try:
            data = json.loads(item.get('event').data)
            print(json.dumps(data, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(e)
            print('------json.JSONDecodeError--------')

if __name__ == '__main__':
    asyncio.run(test_run_writing())
```

## 2、使用**模板生成文章**

```
package org.example.writing;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.GenerateTraceability;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunWritingV2Request;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunWritingV2ResponseBody;
import darabonba.core.ResponseIterable;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.Data;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class RunWritingV2WithTemplate {
    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("DOMAIN", "aimiaobi.cn-beijing.aliyuncs.com");

    public static AsyncClient asyncClient() {
        return AsyncClient.builder().credentialsProvider(
                StaticCredentialProvider.create(Credential.builder().accessKeyId(ALIBABA_CLOUD_ACCESS_KEY_ID).accessKeySecret(ALIBABA_CLOUD_ACCESS_KEY_SECRET).build())
        ).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(
                ClientOverrideConfiguration.create().setProtocol("HTTPS").setEndpointOverride(ENDPOINT)
        ).build();
    }

    public static void main(String[] args) {
        WritingResult result = templateWriting();
        // 最终汇总输出（与 RunWritingV2Outline.java / RunWritingV2WithTemplate.py 对齐）
        System.out.println("==================== 【写作结果】 ====================");
        System.out.println(JSONObject.toJSONString(result));
    }

    /**
     * 模板写作 - 传媒-新闻报道。
     *
     * <p>使用 {@code promptMode=Template}，并通过 {@code writingParams} 传入：</p>
     * <ul>
     *   <li>{@code topic}           ：选题</li>
     *   <li>{@code corePerspective} ：核心观点</li>
     *   <li>{@code newsStructure}   ：新闻结构（如「编年体结构」）</li>
     * </ul>
     *
     * <p>同时启用联网检索与模型溯源（{@code modelSourceTrace}）。</p>
     *
     * @return 写作过程中收集的结果（{@link WritingResult}），结构与
     *         {@link RunWritingV2Outline.WritingResult} 对齐（模板写作不涉及大纲，故 outlines 为 null）。
     */
    public static WritingResult templateWriting() {
        AsyncClient client = asyncClient();

        //更多文体模板请参考接口：https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwritingstyles
        String writingScene = "media";
        String writingStyle = "新闻报道";

        // 模板字段（writingParams）
        Map<String, String> writingParams = new HashMap<>();
        writingParams.put("topic", "嫦娥六号实现人类首次月球背面采样返回");
        writingParams.put("corePerspective", "2024年6月25日，嫦娥六号返回器在内蒙古四子王旗预定区域成功着陆，"
                + "携带约1935.3克月球背面样品返回地球，实现人类历史上首次月背采样返回。"
                + "任务历时53天，先后完成发射入轨、地月转移、近月制动、环月飞行、着陆采样、月背起飞、"
                + "月球轨道交会对接、月地转移与再入回收等关键环节。这一里程碑式成就，"
                + "展现了我国航天科技自立自强的硬核实力，为国际月球与深空探测合作贡献了中国智慧与中国方案，"
                + "鼓舞了全国人民攀登科技高峰的信心与斗志。");
        writingParams.put("newsStructure", "编年体结构");

        RunWritingV2Request.Builder builder = RunWritingV2Request.builder()
                .workspaceId(WORKSPACE_ID)
                .step("Writing")
                .promptMode("Template")
                .writingScene(writingScene)
                .writingStyle(writingStyle)
                .writingParams(writingParams)
                .useSearch(true)
                .sourceTraceMethod("modelSourceTrace");

        // 与 RunWritingV2Outline.java 中 WritingResult 对齐的过程参数收集器
        // （模板写作不涉及大纲，故 outlines 字段为 null）
        WritingResult result = new WritingResult();

        ResponseIterable<RunWritingV2ResponseBody> stream = client.runWritingV2WithResponseIterable(builder.build());
        for (RunWritingV2ResponseBody item : stream) {
            // 打印原始事件体
            System.out.println(JSONObject.toJSONString(item));

            // 任务失败：打印错误并中断
            if (item.getHeader().getErrorMessage() != null) {
                System.err.println("ErrorCode: " + item.getHeader().getErrorCode()
                        + ", ErrorMessage: " + item.getHeader().getErrorMessage());
                break;
            }

            RunWritingV2ResponseBody.Output output = item.getPayload().getOutput();
            if (output == null) {
                continue;
            }

            // 正文增量：随流式事件持续覆盖，最终保留最后一条
            if (output.getText() != null && !output.getText().isEmpty()) {
                result.setText(output.getText());
            }

            // 溯源：任意阶段都可能携带，命中时刷新
            GenerateTraceability traceability = output.getGenerateTraceability();
            if (traceability != null && traceability.getNews() != null) {
                result.setNews(traceability.getNews());
            }
        }
        return result;
    }

    // ============================== 数据结构 ==============================

    /**
     * 模板写作的中间结果。
     *
     * <p>结构与 {@link RunWritingV2Outline.WritingResult} 对齐，便于上层统一消费；
     * 模板写作不涉及大纲，故未包含 outlines 字段。</p>
     */
    @Data
    public static class WritingResult {
        /**
         * 最终生成的正文（全量文本）。
         * <p>随流式事件持续覆盖，最终保留最后一条。</p>
         */
        private String text;

        /**
         * 溯源信息：正文中引用的文章列表。
         * <p>仅在启用溯源（如 {@code sourceTraceMethod=modelSourceTrace}）且有命中时不为空。</p>
         * <p>文章与正文中的 {@code [[n]]} 标记一一对应（索引从 1 开始）。</p>
         */
        private List<GenerateTraceability.News> news;
    }

}
```

```
"""
模板写作示例（Python）。

场景：传媒-新闻报道
  使用 promptMode=Template，并通过 writingParams 传入选题/核心观点/新闻结构等模板字段，
  开启联网检索与模型溯源（modelSourceTrace）。

接口文档：
  https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunWritingV2
"""
import asyncio
import json
import os
from typing import Any, Dict

from alibabacloud_tea_openapi_sse import models as open_api_models
from alibabacloud_tea_openapi_sse.client import Client as OpenApiClient
from alibabacloud_tea_util_sse import models as open_api_util_models

# ============================== 环境配置 ==============================
endpoint = os.environ.get("DOMAIN", "aimiaobi.cn-beijing.aliyuncs.com")
# 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
# 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
workspace_id = os.environ.get("WORKSPACE_ID")

# ============================== 客户端 ==============================
def _create_client() -> OpenApiClient:
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
    )
    return OpenApiClient(config)

def _create_sse_api_info(action: str) -> open_api_models.Params:
    return open_api_models.Params(
        action=action,
        version="2023-08-01",
        protocol="HTTPS",
        method="POST",
        auth_type="AK",
        style="RPC",
        pathname="",
        req_body_type="formData",
        body_type="sse",
    )

class SseClient:
    def __init__(self) -> None:
        self.endpoint = endpoint
        self._runtime = open_api_util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = _create_client()

    async def run_writing(self, body: Dict[str, Any]):
        request = open_api_models.OpenApiRequest(body=body)
        return self._client.call_sse_api_async(
            params=_create_sse_api_info("RunWritingV2"),
            request=request,
            runtime=self._runtime,
        )

# ============================== 模板写作 ==============================
async def template_writing() -> Dict[str, Any]:
    """
    模板写作 - 传媒-新闻报道。

    使用 PromptMode=Template，并通过 WritingParams 传入：
      - topic           ：选题
      - corePerspective ：核心观点
      - newsStructure   ：新闻结构（如「编年体结构」）

    :return: 写作过程中收集的结果，结构与 RunWritingV2OutlineWriting.py 对齐：
        {
          "text": "...",   # 最终生成的正文（随流式事件持续覆盖，最终保留最后一条）
          "news": [...]     # 溯源命中的引用文章列表
        }
    """
    client = SseClient()
    # 更多文体模板请参考接口：https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwritingstyles
    writing_scene = "media"
    writing_style = "新闻报道"

    # 模板字段（writingParams）
    writing_params: Dict[str, str] = {
        "topic": "嫦娥六号实现人类首次月球背面采样返回",
        "corePerspective": (
            "2024年6月25日，嫦娥六号返回器在内蒙古四子王旗预定区域成功着陆，"
            "携带约1935.3克月球背面样品返回地球，实现人类历史上首次月背采样返回。"
            "任务历时53天，先后完成发射入轨、地月转移、近月制动、环月飞行、着陆采样、月背起飞、"
            "月球轨道交会对接、月地转移与再入回收等关键环节。这一里程碑式成就，"
            "展现了我国航天科技自立自强的硬核实力，为国际月球与深空探测合作贡献了中国智慧与中国方案，"
            "鼓舞了全国人民攀登科技高峰的信心与斗志。"
        ),
        "newsStructure": "编年体结构",
    }

    body: Dict[str, Any] = {
        "WorkspaceId": workspace_id,
        "Step": "Writing",
        "PromptMode": "Template",
        "WritingScene": writing_scene,
        "WritingStyle": writing_style,
        "WritingParams": json.dumps(writing_params, ensure_ascii=False),
        # 启用联网检索
        "UseSearch": True,
        # 溯源方式：modelSourceTrace —— 模型在正文片段尾部输出 [[n]] 引用标记，索引从 1 开始
        "SourceTraceMethod": "modelSourceTrace",
    }

    # 与 RunWritingV2OutlineWriting.py 中 WritingResult 对齐的过程参数收集器
    # （模板写作不涉及大纲，故不包含 outlines 字段）
    result: Dict[str, Any] = {"text": None, "news": None}

    async for item in await client.run_writing(body):
        try:
            data = json.loads(item.get("event").data)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"[解析失败] {e}")
            continue

        # 打印原始事件体（与 Java 版 JSONObject.toJSONString(item) 对齐）
        print(json.dumps(data, ensure_ascii=False))

        header = data.get("Header", {}) or {}
        if header.get("ErrorMessage"):
            print(f"写作失败：{header.get('ErrorMessage')}")
            break

        output = (data.get("Payload", {}) or {}).get("Output", {}) or {}

        # 正文增量：随流式事件持续覆盖，最终保留最后一条
        text = output.get("Text")
        if text:
            result["text"] = text

        # 溯源：任意阶段都可能携带，命中时刷新
        traceability = output.get("GenerateTraceability")
        if traceability and traceability.get("News"):
            result["news"] = traceability.get("News")

    # 最终汇总输出
    print("==================== 【写作结果】 ====================")
    print(json.dumps(result, ensure_ascii=False))
    return result

if __name__ == "__main__":
    asyncio.run(template_writing())
```

## **3、分大纲生成文章**

```
package org.example.writing;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.ResponseIterable;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.Data;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 分步骤大纲写作示例（精简版）。
 *
 * <p>核心流程（两步走）：</p>
 * <ol>
 *   <li><b>OutlineGenerate</b>：根据 prompt 生成大纲（树形结构）。</li>
 *   <li><b>Writing</b>：基于上一步生成的大纲，分段检索并写正文。</li>
 * </ol>
 */
public class RunWritingV2Outline {

    // ============================== 环境配置 ==============================
    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("DOMAIN", "aimiaobi.cn-beijing.aliyuncs.com");

    // ============================== 步骤 / 事件常量 ==============================
    private static final String STEP_OUTLINE_GENERATE = "OutlineGenerate";
    private static final String STEP_WRITING = "Writing";

    private static final String EVT_TASK_FAILED = "task-failed";
    private static final String EVT_OUTLINE_GENERATE = "task-outline-generate";
    private static final String EVT_OUTLINE_GENERATE_REASONING = "task-outline-generate-reasoning";
    private static final String EVT_OUTLINE_GENERATE_END = "task-outline-generate-end";
    private static final String EVT_OUTLINE_SEARCH_START = "task-outline-search-start";
    private static final String EVT_OUTLINE_SEARCH = "task-outline-search";

    // 大纲写作专用固定值
    private static final String WRITING_STYLE_OUTLINE = "outlineWriting";
    private static final String WRITING_SCENE_OTHERS = "others";

    // ============================== 客户端 ==============================
    public static AsyncClient asyncClient() {
        return AsyncClient.builder()
                .credentialsProvider(StaticCredentialProvider.create(
                        Credential.builder()
                                .accessKeyId(ALIBABA_CLOUD_ACCESS_KEY_ID)
                                .accessKeySecret(ALIBABA_CLOUD_ACCESS_KEY_SECRET)
                                .build()))
                .serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3))
                .overrideConfiguration(ClientOverrideConfiguration.create()
                        .setProtocol("HTTPS")
                        .setEndpointOverride(ENDPOINT))
                .build();
    }

    // ============================== 入口：全链路 ==============================
    public static void main(String[] args) {
        AsyncClient client = asyncClient();
        String prompt = "写一篇关于新能源汽车的文章，3000字左右";

        // 步骤一：生成大纲
        System.out.println("==================== 【步骤一】生成大纲 ====================");
        WritingResult outlineResult =  runWriting(client, prompt, STEP_OUTLINE_GENERATE, null);

        if (outlineResult.getOutlines() == null || outlineResult.getOutlines().isEmpty()) {
            System.err.println("未获取到大纲，跳过正文写作。");
            return;
        }
        System.out.println("大纲预览：");
        for (WritingOutline outline : outlineResult.getOutlines()) {
            System.out.print(outlineToTreeStr(outline, 0));
        }

        // 步骤二：基于大纲写正文
        System.out.println("==================== 【步骤二】写正文 ====================");
        WritingResult writingResult =  runWriting(client, prompt, STEP_WRITING, outlineResult.getOutlines());
        System.out.println(JSONObject.toJSONString(writingResult));
    }

    // ============================== 核心调用 ==============================

    private static WritingResult runWriting(AsyncClient client,
                                            String prompt,
                                            String step,
                                            List<WritingOutline> outlines) {
        RunWritingV2Request request = buildRequest(prompt, step, outlines);
        ResponseIterable<RunWritingV2ResponseBody> stream = client.runWritingV2WithResponseIterable(request);

        WritingResult result = new WritingResult();
        for (RunWritingV2ResponseBody item : stream) {

            System.out.println(JSONObject.toJSONString(item));

            String event = item.getHeader().getEvent();
            RunWritingV2ResponseBody.Output output = item.getPayload().getOutput();

            // 任务失败：打印错误并中断
            if (EVT_TASK_FAILED.equals(event)) {
                System.err.println("ErrorCode: " + item.getHeader().getErrorCode()
                        + ", ErrorMessage: " + item.getHeader().getErrorMessage());
                break;
            }
            // 大纲事件：刷新大纲
            else if (isOutlineGenerateEvent(event)) {
                if (EVT_OUTLINE_GENERATE_REASONING.equals(event)) {
                    System.out.println("[大纲推理] " + output.getText());
                } else {
                    result.setOutlines(output.getOutlines());
                }
            }
            // 大纲检索事件
            else if (isOutlineSearchEvent(event)) {
                printOutlineSearch(event, output);
            }
            // 正文事件
            else {
                System.out.println("[正文片段] " + JSONObject.toJSONString(output.getText()));
                result.setText(output.getText());
            }
            if ( output.getGenerateTraceability()!=null ){
                //溯源
                result.setNews(output.getGenerateTraceability().getNews());
            }
        }
        return result;
    }

    private static RunWritingV2Request buildRequest(String prompt, String step,
                                                    List<WritingOutline> outlines) {
        RunWritingV2Request.Builder builder = RunWritingV2Request.builder()
                .workspaceId(WORKSPACE_ID)
                // 大纲写作固定使用 outlineWriting + others
                .writingStyle(WRITING_STYLE_OUTLINE)
                .writingScene(WRITING_SCENE_OTHERS)
                .sourceTraceMethod("modelSourceTrace")
                // 联网检索
                .useSearch(true)
                .step(step);

        if (prompt != null) {
            builder.prompt(prompt);
        }
        if (outlines != null) {
            builder.outlineList(outlines);
        }
        return builder.build();
    }

    // ============================== 事件辅助 ==============================

    private static boolean isOutlineGenerateEvent(String event) {
        return EVT_OUTLINE_GENERATE.equals(event)
                || EVT_OUTLINE_GENERATE_REASONING.equals(event)
                || EVT_OUTLINE_GENERATE_END.equals(event);
    }

    private static boolean isOutlineSearchEvent(String event) {
        return EVT_OUTLINE_SEARCH_START.equals(event) || EVT_OUTLINE_SEARCH.equals(event);
    }

    /** 简单打印大纲检索的开始与命中信息 */
    private static void printOutlineSearch(String event, RunWritingV2ResponseBody.Output output) {
        if (EVT_OUTLINE_SEARCH_START.equals(event)) {
            System.out.println("[大纲检索·开始] " + output.getText());
            return;
        }
        OutlineSearchResult sr = output.getSearchResult();
        if (sr == null || sr.getArticles() == null) {
            return;
        }
        System.out.println("[大纲检索·命中] " + sr.getOutline()
                + " (Query=" + sr.getQuery() + ", 共 " + sr.getArticles().size() + " 篇): "
                + sr.getArticles().stream().map(OutlineWritingArticle::getTitle)
                        .collect(Collectors.joining(", ")));
    }

    // ============================== 工具方法 ==============================

    /** 将单个大纲转换为树形文本结构（便于在控制台直观查看大纲结构）。 */
    public static String outlineToTreeStr(WritingOutline outline, int level) {
        StringBuilder sb = new StringBuilder();
        StringBuilder indent = new StringBuilder();
        for (int i = 0; i < level; i++) {
            indent.append("  ");
        }

        if (outline.getOutline() != null && !outline.getOutline().trim().isEmpty()) {
            String symbol = (level == 0) ? "┌─ " : "├─ ";
            sb.append(indent).append(symbol).append(outline.getOutline()).append("\n");
        }
        if (outline.getChildren() != null) {
            for (WritingOutline child : outline.getChildren()) {
                sb.append(outlineToTreeStr(child, level + 1));
            }
        }
        return sb.toString();
    }

    // ============================== 数据结构 ==============================

    /** 大纲写作的中间结果。 */
    @Data
    public static class WritingResult {
        /**
         * 大纲树形结构。
         * <p>仅在 {@code OutlineGenerate} 阶段会被刷新；在 {@code Writing} 阶段为 {@code null}。</p>
         * <p>可作为下一步「正文写作」的 {@code outlineList} 参数传入。</p>
         */
        private List<WritingOutline> outlines;

        /**
         * 最终生成的正文（全量文本）。
         * <p>仅在 {@code Writing} 阶段会被赋值；随流式事件持续覆盖，最终保留最后一条。</p>
         */
        private String text;

        /**
         * 溯源信息：正文中引用的文章列表。
         * <p>仅在启用溯源（如 {@code sourceTraceMethod=modelSourceTrace}）且有命中时不为空。</p>
         * <p>文章与正文中的 {@code [[n]]} 标记一一对应（索引从 1 开始）。</p>
         */
        private java.util.List<GenerateTraceability.News> news;
    }
}
```

```
"""
分步骤大纲写作示例（Python）。

核心流程（两步走）：
  1) OutlineGenerate：根据 prompt 生成大纲（树形结构）
  2) Writing       ：基于上一步生成的大纲，分段检索并写正文

接口文档：
  https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunWritingV2
"""
import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from alibabacloud_tea_openapi_sse import models as open_api_models
from alibabacloud_tea_openapi_sse.client import Client as OpenApiClient
from alibabacloud_tea_util_sse import models as open_api_util_models

# ============================== 环境配置 ==============================
endpoint = os.environ.get("DOMAIN", "aimiaobi.cn-beijing.aliyuncs.com")
# 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
# 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
workspace_id = os.environ.get("WORKSPACE_ID")

# ============================== 步骤 / 事件常量 ==============================
STEP_OUTLINE_GENERATE = "OutlineGenerate"
STEP_WRITING = "Writing"

EVT_TASK_FAILED = "task-failed"
EVT_OUTLINE_GENERATE = "task-outline-generate"
EVT_OUTLINE_GENERATE_REASONING = "task-outline-generate-reasoning"
EVT_OUTLINE_GENERATE_END = "task-outline-generate-end"
EVT_OUTLINE_SEARCH_START = "task-outline-search-start"
EVT_OUTLINE_SEARCH = "task-outline-search"

# 大纲写作专用固定值
WRITING_STYLE_OUTLINE = "outlineWriting"
WRITING_SCENE_OTHERS = "others"

# ============================== 客户端 ==============================
def _create_client() -> OpenApiClient:
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
    )
    return OpenApiClient(config)

def _create_sse_api_info(action: str) -> open_api_models.Params:
    return open_api_models.Params(
        action=action,
        version="2023-08-01",
        protocol="HTTPS",
        method="POST",
        auth_type="AK",
        style="RPC",
        pathname="",
        req_body_type="formData",
        body_type="sse",
    )

class SseClient:
    def __init__(self) -> None:
        self.endpoint = endpoint
        self._runtime = open_api_util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = _create_client()

    async def run_writing(self, body: Dict[str, Any]):
        request = open_api_models.OpenApiRequest(body=body)
        return self._client.call_sse_api_async(
            params=_create_sse_api_info("RunWritingV2"),
            request=request,
            runtime=self._runtime,
        )

# ============================== 工具方法 ==============================
def outline_to_tree_str(outline: Dict[str, Any], level: int = 0) -> str:
    """将单个大纲转为树形文本，便于在控制台直观查看大纲结构。"""
    indent = "  " * level
    text = ""
    name = (outline.get("Outline") or outline.get("outline") or "").strip()
    if name:
        symbol = "┌─ " if level == 0 else "├─ "
        text += f"{indent}{symbol}{name}\n"
    children = outline.get("Children") or outline.get("children") or []
    for child in children:
        text += outline_to_tree_str(child, level + 1)
    return text

def _is_outline_generate_event(event: str) -> bool:
    return event in (
        EVT_OUTLINE_GENERATE,
        EVT_OUTLINE_GENERATE_REASONING,
        EVT_OUTLINE_GENERATE_END,
    )

def _is_outline_search_event(event: str) -> bool:
    return event in (EVT_OUTLINE_SEARCH_START, EVT_OUTLINE_SEARCH)

def _print_outline_search(event: str, output: Dict[str, Any]) -> None:
    if event == EVT_OUTLINE_SEARCH_START:
        print(f"[大纲检索·开始] {output.get('Text', '')}")
        return
    sr = output.get("SearchResult")
    if not sr:
        return
    articles = sr.get("Articles") or []
    titles = ", ".join(a.get("Title", "") for a in articles)
    print(
        f"[大纲检索·命中] {sr.get('Outline', '')} "
        f"(Query={sr.get('Query', '')}, 共 {len(articles)} 篇): {titles}"
    )

# ============================== 核心调用 ==============================
def _build_body(
        prompt: Optional[str],
        step: str,
        outlines: Optional[List[Dict[str, Any]]],
) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "WorkspaceId": workspace_id,
        # 大纲写作固定使用 outlineWriting + others
        "WritingStyle": WRITING_STYLE_OUTLINE,
        "WritingScene": WRITING_SCENE_OTHERS,
        # 联网检索
        "UseSearch": True,
        # 溯源方式：modelSourceTrace —— 模型在正文片段尾部输出 [[n]] 引用标记，索引从 1 开始
        "SourceTraceMethod": "modelSourceTrace",
        "Step": step,
    }
    if prompt is not None:
        body["Prompt"] = prompt
    if outlines is not None:
        body["OutlineList"] = outlines
    return body

async def run_writing(
        client: SseClient,
        prompt: Optional[str],
        step: str,
        outlines: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """统一发起 RunWritingV2 调用，并按事件类型分流处理。

    返回结构：
      {
        "outlines": [...],   # OutlineGenerate 阶段刷新
        "text": "...",        # Writing 阶段最终正文
        "news": [...]         # 溯源命中的引用文章
      }
    """
    body = _build_body(prompt, step, outlines)
    result: Dict[str, Any] = {"outlines": None, "text": None, "news": None}

    async for item in await client.run_writing(body):
        try:
            data = json.loads(item.get("event").data)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"[解析失败] {e}")
            continue

        # 打印原始事件体（与 Java 版 JSONObject.toJSONString(item) 对齐）
        print(json.dumps(data, ensure_ascii=False))

        header = data.get("Header", {}) or {}
        payload = data.get("Payload", {}) or {}
        output = payload.get("Output", {}) or {}
        event = header.get("Event")

        # 任务失败：打印错误并中断
        if event == EVT_TASK_FAILED:
            print(
                f"[任务失败] ErrorCode={header.get('ErrorCode')}, "
                f"ErrorMessage={header.get('ErrorMessage')}"
            )
            break

        # 大纲事件：刷新大纲
        if _is_outline_generate_event(event):
            if event == EVT_OUTLINE_GENERATE_REASONING:
                print(f"[大纲推理] {output.get('Text', '')}")
            else:
                result["outlines"] = output.get("Outlines")

        # 大纲检索事件
        elif _is_outline_search_event(event):
            _print_outline_search(event, output)

        # 正文事件
        else:
            text = output.get("Text", "")
            if text:
                print(f"[正文片段] {json.dumps(text, ensure_ascii=False)}")
                result["text"] = text

        # 溯源信息
        traceability = output.get("GenerateTraceability")
        if traceability and traceability.get("News"):
            result["news"] = traceability.get("News")

    return result

# ============================== 全链路示例 ==============================
async def test_outline_writing():
    client = SseClient()
    prompt = "写一篇关于新能源汽车的文章，3000字左右"

    # 步骤一：生成大纲
    print("==================== 【步骤一】生成大纲 ====================")
    outline_result = await run_writing(client, prompt, STEP_OUTLINE_GENERATE)
    outlines = outline_result.get("outlines")
    if not outlines:
        print("未获取到大纲，跳过正文写作。")
        return

    print("大纲预览：")
    for outline in outlines:
        print(outline_to_tree_str(outline, 0), end="")

    # 步骤二：基于大纲写正文
    print("==================== 【步骤二】写正文 ====================")
    writing_result = await run_writing(client, prompt, STEP_WRITING, outlines=outlines)
    print(json.dumps(writing_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(test_outline_writing())
```

## 4、AI工具箱

AI工具箱包括内容续写、摘要生成、标题生成、内容缩写、内容扩写、关键词抽取等功能，最新实时能力可参考妙笔写作页面的AI工具箱。本节通过**实现摘要**生成场景来帮助您熟悉API的使用。

生成调用demo如下：

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunSummaryGenerateRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunSummaryGenerateResponseBody;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunWritingRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunWritingResponseBody;
import com.google.gson.Gson;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.List;

/**
 * packageName com.dayouz.lightapp
 *
 * @author dayouz
 * @version JDK 8
 * @className runStyleWriting
 * @date 2024/8/13
 * @description 摘要生成Demo
 */
public class RunSummaryGenerateTest {

    public static void main(String[] args) {
        StaticCredentialProvider provider = StaticCredentialProvider.create(Credential.builder()
                .accessKeyId(Constant.accessKeyId)
                .accessKeySecret(Constant.accessKeySecret)
                .build());

        AsyncClient client = AsyncClient.builder()
                .region("cn-beijing")
                .credentialsProvider(provider)
                .serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(ClientOverrideConfiguration.create().setProtocol("HTTPS").setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com"))
                .build();

        RunSummaryGenerateRequest request = RunSummaryGenerateRequest.builder()
                .workspaceId(Constant.workspaceId)
                .prompt("请为上述内容生成一段摘要，字数在100~200字以内。")
                .content("云服务器ECS（Elastic Compute Service）是阿里云提供的性能卓越、稳定可靠、弹性扩展的IaaS（Infrastructure as a Service）级别云计算服务。云服务器ECS免去了您采购IT硬件的前期准备，让您像使用水、电、天然气等公共资源一样便捷、高效地使用服务器，实现计算资源的即开即用和弹性伸缩。阿里云ECS持续提供创新型服务器，解决多种业务需求，助力您的业务发展。")
                .build();

        ResponseIterable<RunSummaryGenerateResponseBody> x = client.runSummaryGenerateWithResponseIterable(request);

        ResponseIterator<RunSummaryGenerateResponseBody> iterator = x.iterator();
        while (iterator.hasNext()) {
            System.out.println("----event----");
            RunSummaryGenerateResponseBody event = iterator.next();
            System.out.println(new Gson().toJson(event));
        }

        System.out.println("ALL***********************");
        System.out.println("请求成功的请求头值：");
        System.out.println(x.getStatusCode());
        System.out.println(x.getHeaders());
    }
}
```
