# 应用视频理解和一键成片的最佳实践

本文介绍如何应用全妙的视频理解和一键成片能力，以实现长视频剪短视频和视频模仿。

## **需要开通的阿里云产品**

-   阿里云百炼 > 应用广场 > [影视传媒视频理解](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7065766471/p951303.png)
    
-   全妙-团队标准版或以上规格 > [一键成片](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_media&from=bailian#/home)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9918296371/p905387.png)
    
-   [云工作流](https://www.aliyun.com/product/aliware/fnf)
    
-   [函数计算](https://www.aliyun.com/product/fc)
    

## **长视频剪**短视频**工作流**

### **总体思路**

-   **素材**：一个长视频。
    
-   **目标**：剪出一个短视频。
    
-   **实现方法**：
    
    1.  请让[影视传媒视频理解](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)轻应用分析该长视频，并基于分析结果生成一个短视频脚本。
        
    2.  将生成的短视频脚本和长视频共同作为[一键成片](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_media&from=bailian#/home)的输入，生成一个短视频。
        
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9918296371/p905382.png)
    

### **操作步骤**

#### **创建函数计算函数**

需要创建2个函数计算函数，分别用于请求视频理解轻应用和全妙一键成片功能。

##### **1.1 视频理解函数**

创建一个事件函数，代码语言选择python3.10，函数运行时超时时间配置成600s。

1.  在代码编辑页面，在Terminal中安装视频理解轻应用的SDK。
    
    > **注意**：示例代码末尾的"."表示安装到当前目录，请确保其不被遗漏。
    

```
pip install alibabacloud-tea-openapi-sse==1.0.2 -t .
```

2.  代码示例参考如下，需要将[AK、SK](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)、[workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)替换为实际值，以确保代码正常运行并返回正确的结果。
    

```
# -*- coding: utf-8 -*-
import logging
import json
from alibabacloud_tea_openapi_sse.client import Client as OpenApiClient
from alibabacloud_tea_openapi_sse import models as open_api_models
from alibabacloud_tea_util_sse import models as util_models
import asyncio

# To enable the initializer feature (https://help.aliyun.com/document_detail/2513452.html)
# please implement the initializer function as below：
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')

class LightApp:
    def __init__(self, ak, sk, token, workspace_id, videoUrl, vlPrompt, llmPrompt) -> None:
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        self.access_key_id = ak
        self.access_key_secret = sk
        self.token = token
        self.videoUrl = videoUrl
        self.videoModelCustomPromptTemplate = vlPrompt
        self.modelCustomPromptTemplate = llmPrompt
        self.workspace_id = workspace_id
        # 以上字段请改成实际的值。
        self.endpoint = 'quanmiaolightapp.cn-beijing.aliyuncs.com'
        self._client = None
        self._api_info = self._create_api_info()
        self._runtime = util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = self._create_client(self.access_key_id, self.access_key_secret, self.token, self.endpoint)

    def _create_client(
            self,
            access_key_id: str,
            access_key_secret: str,
            token: str,
            endpoint: str,
    ) -> OpenApiClient:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=endpoint
        )
        return OpenApiClient(config)

    def _create_api_info(self) -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称
            action='RunVideoAnalysis',
            # 接口版本
            version='2024-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/'+self.workspace_id+'/quanmiao/lightapp/runVideoAnalysis',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='sse'
        )
        return params

    async def do_sse_query(self):
        body = {
            'videoUrl': self.videoUrl,
            "videoModelId":"qwen-vl-max",   # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            "videoModelCustomPromptTemplate": self.videoModelCustomPromptTemplate,
            "modelCustomPromptTemplate": self.modelCustomPromptTemplate
        }
        request = open_api_models.OpenApiRequest(
            body=body
        )
        sse_receiver = self._client.call_sse_api_async(params=self._api_info, request=request, runtime=self._runtime)
        return sse_receiver

# 接口调用
async def run(fc_event, context):
    creds = context.credentials
    event_obj = json.loads(fc_event)
    light_app = LightApp(creds.access_key_id, creds.access_key_secret, creds.security_token, creds.workspace_id, event_obj['videoUrl'], event_obj['vlPrompt'], event_obj['llmPrompt'])
    async for res in await light_app.do_sse_query():
        try:
            data = json.loads(res.get('event').data)
            header = data['header']
            event = header['event']
            if event == 'task-finished':
                print(data['payload']['output']['videoGenerateResult']['text'])
                return data['payload']['output']['videoGenerateResult']['text']
        except json.JSONDecodeError:
            print('------json.JSONDecodeError--------')
            print(res.get('headers'))
            print(res.get('event').data)
            print('------json.JSONDecodeError-end--------')
            continue
    print('------end--------')

def handler(event, context):
    # evt = json.loads(event)
    logger = logging.getLogger()
    logger.info(event)
    result = asyncio.run(run(event, context))
    return {'videoContent':result}
```

##### **1.2 一键成片函数**

创建一个事件函数，代码语言选择python3.10，函数运行时超时时间配置成600s。

1.  在代码编辑页面，在Terminal中安装视频理解轻应用的SDK。
    
    > **注意**：示例代码末尾的"."表示安装到当前目录，请确保其不被遗漏。
    

```
pip install alibabacloud-tea-openapi -t .
```

2.  代码示例参考如下，需要将[AK、SK](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)、[workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)替换为实际值，以确保代码正常运行并返回正确的结果。
    

```
# -*- coding: utf-8 -*-
import logging
import json
import time

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

class AiMiaoBi:
    def __init__(self, ak, sk, token, workspace_id) -> None:
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        self.access_key_id = ak
        self.access_key_secret = sk
        self.workspace_id = workspace_id
        # 以上字段请改成实际的值。
        self.endpoint = 'aimiaobi.cn-beijing.aliyuncs.com'
        self._client = None
        self.token = token
        self._submit_api_info = self._create_submit_api_info()
        self._get_status_api_info = self._create_get_status_api_info()
        self._runtime = util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = self._create_client(self.access_key_id, self.access_key_secret, self.token, self.endpoint)

    def _create_client(
            self,
            access_key_id: str,
            access_key_secret: str,
            token: str,
            endpoint: str,
    ) -> OpenApiClient:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=endpoint
        )
        return OpenApiClient(config)

    def _create_submit_api_info(self) -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称
            action='SubmitSmartClipTask',
            # 接口版本
            version='2023-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    def _create_get_status_api_info(self) -> open_api_models.Params:
        params = open_api_models.Params(
            # 接口名称
            action='GetSmartClipTask',
            # 接口版本
            version='2023-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    def do_submit(self, video_url, speech):
        input_config = {
                "VideoIds": [
                    {
                        "Type": "url",
                        "Id": video_url
                    }
                ],
                "SpeechTexts": [
                    speech
                ]
            }
        output_config = {
                "FileName": "test_{index}",
                "SaveToGeneratedContent": True
            }
        body = {
            "WorkspaceId": self.workspace_id,
            "InputConfig": json.dumps(input_config),
            "OutputConfig": json.dumps(output_config)
        }

        request = open_api_models.OpenApiRequest(
            body=body
        )

        response = self._client.call_api(params=self._submit_api_info, request=request, runtime=self._runtime)
        print(response)
        resp_body = response['body']
        task_id = resp_body['Data']['TaskId']
        return task_id

    def do_check_status(self, task_id):
        body = {
          "WorkspaceId": self.workspace_id,
          "TaskId": task_id
        }
        request = open_api_models.OpenApiRequest(
            body=body
        )

        response = self._client.call_api(params=self._get_status_api_info, request=request, runtime=self._runtime)
        print(response)
        resp_body = response['body']
        return resp_body

# 接口调用
def run(video_url, speech, context):
    creds = context.credentials
    ai_miaobi = AiMiaoBi(creds.access_key_id, creds.access_key_secret, creds.security_token, creds.workspace_id)
    task_id = ai_miaobi.do_submit(video_url, speech)
    max_wait_time = 1800  # 最大等待时间1800秒
    poll_interval = 15    # 每15秒轮询一次
    elapsed_time = 0
    while elapsed_time < max_wait_time:
        resp_body = ai_miaobi.do_check_status(task_id)
        status = resp_body['Data']['Status']
        if status == "SUCCESSED":
            output_url = resp_body['Data']['SubJobs'][0]['FileAttr']['TmpUrl']
            return output_url
        time.sleep(poll_interval)
        elapsed_time += poll_interval
    raise Exception(f"Task timeout after {max_wait_time} seconds")

def handler(event, context):
    evt = json.loads(event)
    logger = logging.getLogger()
    logger.info(event)
    outputUrl = run(evt['videoUrl'], evt['speech'], context)
    return {'outputUrl': outputUrl}
```

##### **1.3 支持多素材的一键成片函数**

```
# -*- coding: utf-8 -*-
import logging
import json
import time

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

class AiMiaoBi:
    def __init__(self, ak, sk, token, workspace_id) -> None:
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        self.access_key_id = ak
        self.access_key_secret = sk
        self.workspace_id = workspace_id
        # 以上字段请改成实际的值。
        self.endpoint = 'aimiaobi.cn-beijing.aliyuncs.com'
        self._client = None
        self.token = token
        self._submit_api_info = self._create_submit_api_info()
        self._get_status_api_info = self._create_get_status_api_info()
        self._runtime = util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._client = self._create_client(self.access_key_id, self.access_key_secret, self.token, self.endpoint)

    def _create_client(
            self,
            access_key_id: str,
            access_key_secret: str,
            token: str,
            endpoint: str,
    ) -> OpenApiClient:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint=endpoint
        )
        return OpenApiClient(config)

    def _create_submit_api_info(self) -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称
            action='SubmitSmartClipTask',
            # 接口版本
            version='2023-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    def _create_get_status_api_info(self) -> open_api_models.Params:
        params = open_api_models.Params(
            # 接口名称
            action='GetSmartClipTask',
            # 接口版本
            version='2023-08-01',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    def do_submit(self, video_material_urls, speech):
        input_config = {
                "VideoIds": [
                    {
                        "Type": "url",
                        "Id": video_url
                    }
                    for video_url in video_material_urls
                ],
                "SpeechTexts": [
                    speech
                ]
            }
        output_config = {
                "FileName": "test_{index}",
                "SaveToGeneratedContent": True
            }
        body = {
            "WorkspaceId": self.workspace_id,
            "InputConfig": json.dumps(input_config),
            "OutputConfig": json.dumps(output_config)
        }

        request = open_api_models.OpenApiRequest(
            body=body
        )

        response = self._client.call_api(params=self._submit_api_info, request=request, runtime=self._runtime)
        print(response)
        resp_body = response['body']
        task_id = resp_body['Data']['TaskId']
        return task_id

    def do_check_status(self, task_id):
        body = {
          "WorkspaceId": self.workspace_id,
          "TaskId": task_id
        }
        request = open_api_models.OpenApiRequest(
            body=body
        )

        response = self._client.call_api(params=self._get_status_api_info, request=request, runtime=self._runtime)
        print(response)
        resp_body = response['body']
        return resp_body

# 接口调用
def run(video_material_urls, speech, context):
    creds = context.credentials
    ai_miaobi = AiMiaoBi(creds.access_key_id, creds.access_key_secret, creds.security_token, creds.workspace_id)
    task_id = ai_miaobi.do_submit(video_material_urls, speech)
    max_wait_time = 1800  # 最大等待时间1800秒
    poll_interval = 15    # 每15秒轮询一次
    elapsed_time = 0
    while elapsed_time < max_wait_time:
        resp_body = ai_miaobi.do_check_status(task_id)
        status = resp_body['Data']['Status']
        if status == "SUCCESSED":
            output_url = resp_body['Data']['SubJobs'][0]['FileAttr']['TmpUrl']
            return output_url
        time.sleep(poll_interval)
        elapsed_time += poll_interval
    raise Exception(f"Task timeout after {max_wait_time} seconds")

def handler(event, context):
    evt = json.loads(event)
    logger = logging.getLogger()
    logger.info(event)
    outputUrl = run(evt['videoMaterialUrls'], evt['speech'], context)
    return {'outputUrl': outputUrl}
```

#### **创建云工作流**

[创建云工作流实例](https://help.aliyun.com/zh/document_detail/2399888.html)后，您可以直接复制以下YAML文件进行配置，以减少从头开始配置所需的工作量。

> 其中`${ALIUID}`、`${VIDEO_ANALYSIS_FUNCTION_NAME}`、`${VIDEO_CUT_FUNCTION_NAME}`需要替换成自己的账号ID和两个函数计算函数的名称。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9918296371/p905383.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9918296371/p905386.png)

支持一个原始素材的工作流：

```
Type: StateMachine
Name: video_edit
SpecVersion: v1
StartAt: 视频理解
States:
  - Type: Task
    Name: 视频理解
    Action: FC:InvokeFunction
    TaskMode: RequestComplete
    Parameters:
      invocationType: Sync
      resourceArn: acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_ANALYSIS_FUNCTION_NAME}/LATEST
      body:
        videoUrl.$: $Input.videoUrl
        vlPrompt.$: $Input.vlPrompt
        llmPrompt.$: $Input.llmPrompt
    OutputConstructor:
      returnID.$: uuid()
      videoContent.$: $Output.Body.videoContent
    Next: 一键成片
  - Type: Task
    Name: 一键成片
    Action: FC:InvokeFunction
    TaskMode: RequestComplete
    Parameters:
      invocationType: Sync
      resourceArn: acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_CUT_FUNCTION_NAME}/LATEST
      body:
        videoUrl.$: $Context.Execution.Input.videoUrl
        speech.$: $Input.videoContent
    OutputConstructor:
      outputUrl.$: $Output.Body.outputUrl
    Next: Succeed
  - Type: Succeed
    Name: Succeed
    End: true
```

支持多个原始素材的工作流：

```
Type: StateMachine
Name: video_learning
SpecVersion: v1
StartAt: 视频理解
States:
  - Type: Task
    Name: 视频理解
    Action: FC:InvokeFunction
    TaskMode: RequestComplete
    Parameters:
      invocationType: Sync
      resourceArn: acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_ANALYSIS_FUNCTION_NAME}/LATEST
      body:
        videoUrl.$: $Input.videoUrl
        vlPrompt.$: $Input.vlPrompt
        llmPrompt.$: $Input.llmPrompt
    OutputConstructor:
      returnID.$: uuid()
      videoContent.$: $Output.Body.videoContent
    Next: 一键成片
  - Type: Task
    Name: 一键成片
    Action: FC:InvokeFunction
    TaskMode: RequestComplete
    Parameters:
      invocationType: Sync
      resourceArn: acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_CUT_FUNCTION_NAME}/LATEST
      body:
        videoMaterialUrls.$: $Context.Execution.Input.videoMaterialUrls
        speech.$: $Input.videoContent
    OutputConstructor:
      outputUrl.$: $Output.Body.outputUrl
    Next: Succeed
  - Type: Succeed
    Name: Succeed
    End: true
```

##### **启动工作流执行**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9918296371/p905385.png)

单个素材的输入参数可以参考：

```
{
  "videoUrl": "https://abc.com/xyz.mp4",
  "vlPrompt": "# 角色\n你是一名视频分析师，擅长对各种视频片段进行理解。\n\n# 任务描述\n给你一个视频片段的多张关键帧图片，请你完成以下任务。\n- 输出每张图片的画面信息，包括人物、物体、动作、文字、字幕、镜头语言、一句话总结等。\n- 把每张图片的信息串联起来，生成视频的详细概述，还原该片段的剧情。\n\n# 限制\n- 分析范围严格限定于提供的视频子片段，不涉及视频之外的任何推测或背景信息。\n- 总结时需严格依据视频内容，不可添加个人臆测或创意性内容。\n- 保持对所有视频元素（尤其是文字和字幕）的高保真还原，避免信息遗漏或误解。\n\n# 输入数据\n## 视频片段ASR信息  (如果输入为空则忽略ASR信息)\n{videoAsrText}\n\n## 视频补充信息 (可能对你理解该片段有帮助，如果输入为空则忽略补充信息)\n{videoExtraInfo}\n\n# 输出格式\n直接按照任务目标里即可，先输出每张图片的描述，再串联起来输出整个视频片段的剧情。",
  "llmPrompt": "# 角色\n你是一个专业的视频标注专员，擅长结合视频镜头信息来分析处理各种视频任务。\n\n# 任务目标\n请你结合输入数据串联、还原出整个视频的详细剧情。\n\n# 限制\n1.如出现语法上错误，或逻辑不通，请直接修改\n2.在视频分镜中，如果包含台词，可能会出现说话者与其所说内容不匹配的情况。因此，必须根据剧情的进展，准确判断每段台词的真实说话者\n3.如果视频分镜中无台词，请根据视频音频文字为其匹配台词\n4.修改后的故事请适当保留视频分镜中对人物、场景的描写\n5.帮忙润色一下故事，使其更具逻辑性\n6.结合视频分镜中的人物外观特点，如果有外观相近的人物是同一个角色。因此，需要将不同分镜中的人物角色统一。\n\n# 输入数据\n## 资料一：视频分镜信息 (视频各镜头的视觉描述信息)\n{videoAnalysisText}\n\n## 资料二：视频ASR转录信息 (未标注出说话者，可能有错误和遗漏，如果没有输入ASR，则忽略此信息)\n{videoAsrText}\n\n## 资料三：视频补充信息 (如果输入为空则忽略补充信息)\n{videoExtraInfo}\n\n# 输出格式\n直接输出视频剧情，不要输出其他信息。"
}
```

多个素材的输入参数可以参考：

```
{
    "videoUrl": "https://goods-test1.oss-cn-hangzhou.aliyuncs.com/taishan.mp4?Expires=1733739990&OSSAccessKeyId=TMP.3KdZpAPcCaKGBXhrwXxJMpA3oeAKNKWjekat1PyfoscUaHeVDqJUu7HjEA9LoXWQrNupgJWJbZUSJ5nB4YUQomhfJX****&Signature=Hqex9xMHdrAjsLQWLoRx1O%2FEGRY%3D",
    "vlPrompt": "# 角色\n你是一名视频分析师，擅长对各种视频片段进行理解。\n\n# 任务描述\n给你一个视频片段的多张关键帧图片，请你完成以下任务。\n- 输出每张图片的画面信息，包括人物、物体、动作、文字、字幕、镜头语言、一句话总结等。\n- 把每张图片的信息串联起来，生成视频的详细概述，还原该片段的剧情。\n\n# 限制\n- 分析范围严格限定于提供的视频子片段，不涉及视频之外的任何推测或背景信息。\n- 总结时需严格依据视频内容，不可添加个人臆测或创意性内容。\n- 保持对所有视频元素（尤其是文字和字幕）的高保真还原，避免信息遗漏或误解。\n\n# 输入数据\n## 视频片段ASR信息  (如果输入为空则忽略ASR信息)\n{videoAsrText}\n\n## 视频补充信息 (可能对你理解该片段有帮助，如果输入为空则忽略补充信息)\n{videoExtraInfo}\n\n# 输出格式\n直接按照任务目标里即可，先输出每张图片的描述，再串联起来输出整个视频片段的剧情。",
    "llmPrompt": "# 角色\n你是一个专业的视频标注专员，擅长结合视频镜头信息来分析处理各种视频任务。\n\n# 任务目标\n请你结合输入数据串联、还原出整个视频的详细剧情。\n\n# 限制\n1.如出现语法上错误，或逻辑不通，请直接修改\n2.在视频分镜中，如果包含台词，可能会出现说话者与其所说内容不匹配的情况。因此，必须根据剧情的进展，准确判断每段台词的真实说话者\n3.如果视频分镜中无台词，请根据视频音频文字为其匹配台词\n4.修改后的故事请适当保留视频分镜中对人物、场景的描写\n5.帮忙润色一下故事，使其更具逻辑性\n6.结合视频分镜中的人物外观特点，如果有外观相近的人物是同一个角色。因此，需要将不同分镜中的人物角色统一。\n\n# 输入数据\n## 资料一：视频分镜信息 (视频各镜头的视觉描述信息)\n{videoAnalysisText}\n\n## 资料二：视频ASR转录信息 (未标注出说话者，可能有错误和遗漏，如果没有输入ASR，则忽略此信息)\n{videoAsrText}\n\n## 资料三：视频补充信息 (如果输入为空则忽略补充信息)\n{videoExtraInfo}\n\n# 输出格式\n直接输出视频剧情，不要输出其他信息。",
    "videoMaterialUrls": [
        "https://goods-test1.oss-cn-hangzhou.aliyuncs.com/huangshan.mp4?Expires=1733740025&OSSAccessKeyId=TMP.3KdZpAPcCaKGBXhrwXxJMpA3oeAKNKWjekat1PyfoscUaHeVDqJUu7HjEA9LoXWQrNupgJWJbZUSJ5nB4YUQomhfJX****&Signature=6sjMte8j6tRtNGe6bRks2uYd%2FPU%3D"
    ]
}
```

## **视频模仿工作流**

### **总体思路**

-   **素材**：一个范例视频和一些视频素材。
    
-   **目标**：模仿范例视频，将视频素材进行智能剪辑。
    
-   **实现方式**：
    
    1.  理解范例视频，学习视频结构及口播文案的内容风格。同时，深入理解视频素材的具体内容，明确手头所拥有的素材。
        
    2.  通过大模型参考范例视频的结构及素材视频的内容，创作一份新的待剪辑视频的口播文案。
        
    3.  使用一键成片功能进行素材的智能剪辑。
        
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9918296371/p905384.png)
    

### **工作流定义**

-   其中65行的`${API_KEY}`要替换成实际大模型的API-KEY。
    
-   `${ALIUID}`、 `${VIDEO_ANALYSIS_FUNCTION_NAME}`、 `${VIDEO_CUT_FUNCTION_NAME}`、 `${CONSTRUCT_PROMPT_FUNCTION_NAME}`需要替换成实际账号ID和三个函数计算函数名称。
    

```
Type: StateMachine
Name: video_learning
SpecVersion: v1
StartAt: Parallel
States:
  - Type: Parallel
    Name: Parallel
    Branches:
      - StartAt: 源视频理解
        States:
          - Type: Task
            Name: 源视频理解
            Action: FC:InvokeFunction
            TaskMode: RequestComplete
            Parameters:
              invocationType: Sync
              resourceArn: >-
                acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_ANALYSIS_FUNCTION_NAME}/LATEST
              body:
                videoUrl.$: $Input.sourceVideoUrl
                vlPrompt.$: $Input.sourceVlPrompt
                llmPrompt.$: $Input.sourceLlmPrompt
            OutputConstructor:
              returnID.$: uuid()
              sourceVideoContent.$: $Output.Body.videoContent
            End: true
      - StartAt: 目标视频理解
        States:
          - Type: Task
            Name: 目标视频理解
            Action: FC:InvokeFunction
            TaskMode: RequestComplete
            Parameters:
              invocationType: Sync
              body:
                videoUrl.$: $Input.targetVideoUrl
                vlPrompt.$: $Input.targetVlPrompt
                llmPrompt.$: $Input.targetLlmPrompt
              resourceArn: >-
                acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_ANALYSIS_FUNCTION_NAME}/LATEST
            OutputConstructor:
              returnID.$: uuid()
              targetVideoContent.$: $Output.Body.videoContent
            End: true
    Next: Prompt拼接
  - Type: Task
    Name: Prompt拼接
    Action: FC:InvokeFunction
    TaskMode: RequestComplete
    Parameters:
      invocationType: Sync
      body:
        sourceVideoContent.$: $Input.Branch0.sourceVideoContent
        targetVideoContent.$: $Input.Branch1.targetVideoContent
      resourceArn: acs:fc:cn-shanghai:${ALIUID}:functions/${CONSTRUCT_PROMPT_FUNCTION_NAME}/LATEST
    OutputConstructor:
      messages.$: $Output.Body.messages
    Next: 生成新视频口播
  - Type: Task
    Name: 生成新视频口播
    Action: DashScope:QwenTextGeneration
    TaskMode: RequestComplete
    Parameters:
      model: qwen-max
      api_key: ${API_KEY}
      enable_search: false
      max_tokens: 1024
      top_p: 0.8
      temperature: 0.5
      messages.$: $Input.messages
    OutputConstructor:
      speech.$: $Output.output.choices[0].message.content
    Next: 一键成片
  - Type: Task
    Name: 一键成片
    Action: FC:InvokeFunction
    TaskMode: RequestComplete
    Parameters:
      invocationType: Sync
      resourceArn: acs:fc:cn-shanghai:${ALIUID}:functions/${VIDEO_CUT_FUNCTION_NAME}/LATEST
      body:
        videoMaterialUrls.$: $Context.Execution.Input.videoMaterialUrls
        speech.$: $Input.speech
    OutputConstructor:
      outputUrl.$: $Output.Body.outputUrl
    Next: Succeed
  - Type: Succeed
    Name: Succeed
    End: true
```

### **构建prompt函数**

创建一个事件函数，代码语言选择python3.10。

```
# -*- coding: utf-8 -*-
import logging
import json

# To enable the initializer feature (https://help.aliyun.com/document_detail/2513452.html)
# please implement the initializer function as below：
# def initializer(context):
#   logger = logging.getLogger()
#   logger.info('initializing')

def handler(event, context):
    evt = json.loads(event)
    logger = logging.getLogger()
    prompt = '''
    你是一名专业视频内容编辑。
    你的任务是学习【素材视频】的视频结构，然后结合【目标视频】的内容，写一篇口播文案，用来将【目标视频】重新剪辑后进行播报。
    
    【素材视频】的视频结构如下：
    {sourceVideoContent}

    【目标视频】的内容如下：
    {targetVideoContent}
    
    输出要求：
    输出对【目标视频】理解后重新剪辑的口播文案，要求字数在150字左右，文案内容采用解说形式，只输出文案内容
    '''.format(sourceVideoContent=evt['sourceVideoContent'], targetVideoContent=evt['targetVideoContent'])
    return {"messages": [{"role":"user","content":prompt}]}
```

## **产品相关文档**

### **计费文档**

视频理解：[影视传媒视频理解计费](https://help.aliyun.com/zh/model-studio/film-and-television-media-video-understanding-billing)

妙笔（包含一键成片）：[计费说明（妙笔和妙策）](https://help.aliyun.com/zh/model-studio/miaobi-billing)

### **API文档**

视频理解：[影视传媒视频理解](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-dir-film-and-television-media-video-understanding/)

一键成片：[妙笔-一键成片](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/)

## **介绍视频**
