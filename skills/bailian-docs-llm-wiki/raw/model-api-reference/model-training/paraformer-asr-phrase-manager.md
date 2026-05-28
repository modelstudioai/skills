# paraformer热词

**说明**

支持的领域 / 任务：audio（音频） / asr（语音识别）

在语音识别服务中，如果您的业务领域有部分词汇默认识别效果不够好，可以考虑使用热词功能，将这些词添加到词表从而改善识别结果。

## **热词简介**

热词通过热词列表的形式在SDK中使用，热词列表是一个以热词文本为Key，热词权重为Value的字典。热词列表最大支持设置500个热词，热词文本规则如下：纯中文热词不超过10个汉字，纯英文或者中英文混合热词，按空格分词后，不超过5个词；对于热词权重规则如下：有效的热词权重取值范围为\[1, 5\]和\[-6, -1\]区间内的整数值。如果想提高某个热词的识别概率，则可以设置\[1, 5\]范围内的权重，权重越大概率越高；如果想降低某个热词的识别概率，则可以设置\[-6, -1\]范围内的权重，权重越小概率越低。

## **支持的模型**

**模型名**

**模型简介**

paraformer-realtime-v1

Paraformer中文实时语音识别模型，支持视频直播、会议等实时场景下的语音识别。仅支持16kHz采样率的音频。

paraformer-realtime-8k-v1

Paraformer中文实时语音识别模型，支持8kHz电话客服等场景下的实时语音识别。

paraformer-v1 [![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9651150861/p614224.png)](https://modelscope.cn/models/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/)

Paraformer中英文语音识别模型，支持16kHz及以上采样率的音频或视频语音识别。

paraformer-8k-v1

Paraformer中文语音识别模型，支持8kHz电话语音识别。

paraformer-mtl-v1

Paraformer多语言语音识别模型，支持16kHz及以上采样率的音频或视频语音识别。

支持的语种/方言包括：中文普通话、中文方言（粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话）、英语、日语、韩语、西班牙语、印尼语、法语、德语、意大利语、马来语。

## **前提条件**

-   已开通服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。建议您[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，从而避免在代码里显示配置API Key，降低泄漏风险。
    
-   已安装最新版SDK：[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## **热词管理**

在Java和Python中使用`AsrPhraseManager`类来管理热词的创建，更新，删除，查询等功能。

`AsrPhraseManager`的导入方式如下：

Python

```
from dashscope.audio.asr import AsrPhraseManager
```

Java

```
import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseManager;
```

### 创建热词

同步调用的形式提交一个创建热词请求。

-   接口
    
    Python
    
    ```
    def create_phrases(cls,
                       model: str,
                       phrases: Dict[str, Any],
                       training_type: str = 'compile_asr_phrase',
                       **kwargs)
    ```
    
    Java
    
    ```
    AsrPhraseStatusResult CreatePhrases(AsrPhraseParam param)
          throws ApiException, NoApiKeyException, InputRequiredException
    ```
    
-   参数说明
    
    对于Java SDK，将使用一个AsrPhraseParam对象作为参数，其方法和参数如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    param
    
    AsrPhraseParam
    
    创建热词的配置参数，见上文关于AsrPhraseParam类型的描述，CreatePhrases调用不需要填写pageNo和pageSize字段，但是要求添加model，phraseList字段。
    
    对于Python SDK，其参数说明如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    model
    
    str
    
    指定的Paraformer模型名，关于如何进行模型选择，请参考：[支持的模型](#cc235e90699kg)。
    
    phrases
    
    Dict\[str, Any\]
    
    热词列表。
    
    training\_type
    
    str
    
    固定为compile\_asr\_phrase。
    
-   返回示例
    
    对于Java SDK，将返回一个AsrPhraseStatusResult对象，对于Python SDK，将返回一个Dict，AsrPhraseStatusResult成员通过对应get方法获取，成员名称和Python SDK基本一致，仅命名方式不同（Java为驼峰式）。
    
    ```
    {
    	"status_code": 200,
    	"request_id": "2b815cfe-793f-9f3c-b528-5ade0a2d498e",
    	"code": null,
    	"message": "",
    	"output": {
    		"job_id": "ft-202309261539-2af1",
    		"status": "SUCCEEDED",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    		"training_type": "compile_asr_phrase",
    		"create_time": "2023-09-26 15:39:07"
    	},
    	"usage": null,
    	"job_id": "ft-202309261539-2af1",
    	"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    	"finetuned_outputs": null,
    	"training_type": null,
    	"create_time": "2023-09-26 15:39:07",
    	"output_type": null,
    	"model": null
    }
    ```
    
-   调用范例
    
    Python
    
    ```
    # coding=utf-8
    
    import dashscope
    from dashscope.audio.asr import AsrPhraseManager
    
    dashscope.api_key='your-dashscope-api-key'
    
    phrases = {'通义千问': 5}
    
    result = AsrPhraseManager.create_phrases(model='paraformer-realtime-v1',
                                             phrases=phrases)
    if result.output is not None and result.output['finetuned_output'] is not None:
        print('job_id:%s, finetuned_output:%s' %
              (result.output['job_id'], result.output['finetuned_output']))
    else:
        print('Error: ', str(result))
    ```
    
    Java
    
    ```
    package com.alibaba.test;
    
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseManager;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseParam;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseStatusResult;
    import com.alibaba.dashscope.audio.asr.recognition.Recognition;
    import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
    import com.alibaba.dashscope.utils.Constants;
    import java.util.Collections;
    
    class Test {
      
      public static void main(String[] args) {
        AsrPhraseParam param = AsrPhraseParam.builder()
                .model("your-model")
                .phraseList(Collections.singletonMap("通义千问", 5))
                .apiKey("your-dashscope-api-key")
                .build();
    
        AsrPhraseStatusResult createResult = null;
        try {
          createResult = AsrPhraseManager.CreatePhrases(param);
          if (createResult.getOutput() != null && createResult.getOutput().getFineTunedOutput() != null) {
            System.out.println("job_id: " + createResult.getOutput().getJobId() + ", finetuned_output: " + createResult.getOutput().getFineTunedOutput());
          } else {
            System.out.println("Error: " + createResult);
          }
        } catch (Exception e) {
          throw new RuntimeException(e);
        }
      }
    }
    ```
    

### 查询热词

该接口将以同步调用的形式提交一个查询热词请求。

-   接口
    
    Python
    
    ```
    def query_phrases(cls, phrase_id: str, **kwargs)
    ```
    
    Java
    
    ```
    AsrPhraseStatusResult QueryPhrase(AsrPhraseParam param, String phraseId)
          throws ApiException, NoApiKeyException, InputRequiredException
    ```
    
-   参数配置
    
    对于Java SDK，将使用一个AsrPhraseParam对象作为参数，其方法和参数如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    param
    
    AsrPhraseParam
    
    创建热词的配置参数，见上文关于AsrPhraseParam类型的描述，对于QueryPhrase调用，不需要填phraseLIst及pageNo和pageSize字段。
    
    phraseId
    
    String
    
    调用CreatePhrases，UpdatePhrases, QueryPhrase等接口返回的AsrPhraseStatusOutput对象后，通过该对象的getFineTunedOutput返回的热词ID，String类型。调用ListPhrases时，使用AsrPhraseStatusOutput对象的getFinetunedOutputs接口将返回所有热词信息的列表，然后使用AsrPhraseInfo的getFineTunedOutput即可获取对应热词的热词ID。
    
    对于Python SDK，参数说明如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    phrase\_id
    
    str
    
    调用create\_phrases，update\_phrases, query\_phrases等接口返回的Dict对象，通过finetuned\_output访问对应phrase\_id
    
-   返回示例
    
    ```
    {
    	"status_code": 200,
    	"request_id": "19ee9c5f-173b-9fed-8e61-40bc53f1eea7",
    	"code": null,
    	"message": "",
    	"output": {
    		"create_time": "2023-09-26 15:39:08",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    		"job_id": "ft-202309261539-2af1",
    		"model": "paraformer-realtime-v1",
    		"output_type": "custom_resource"
    	},
    	"usage": null,
    	"job_id": "ft-202309261539-2af1",
    	"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    	"finetuned_outputs": null,
    	"training_type": null,
    	"create_time": "2023-09-26 15:39:08",
    	"output_type": "custom_resource",
    	"model": "paraformer-realtime-v1"
    }
    ```
    
-   调用示例
    
    Python
    
    ```
    # coding=utf-8
    
    import dashscope
    from dashscope.audio.asr import AsrPhraseManager
    
    dashscope.api_key='your-dashscope-api-key'
    
    result = AsrPhraseManager.query_phrases(phrase_id='phrase-id')
    if result.output is not None:
        print('query phrases: ', result.output)
    else:
        print('Error: ', str(result))
    ```
    
    Java
    
    ```
    package com.alibaba.test;
    
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseManager;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseParam;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseStatusResult;
    import com.alibaba.dashscope.audio.asr.recognition.Recognition;
    import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
    import com.alibaba.dashscope.utils.Constants;
    
    class Test {
      
      public static void main(String[] args) {
        AsrPhraseParam param = AsrPhraseParam.builder()
                .model("your-model")
                .apiKey("your-dashscope-api-key")
                .build();
    
        AsrPhraseStatusResult result = null;
        try {
          result = AsrPhraseManager.QueryPhrase(param, "phrase-id");
          if (result.getOutput() != null) {
            System.out.println("query phrases: " + result.getOutput());
          } else {
            System.out.println("Error: " + result);
          }
        } catch (Exception e) {
          throw new RuntimeException(e);
        }
      }
    }
    ```
    

### 更新热词

该接口将以同步调用的形式提交一个更新热词请求。

-   接口
    
    Python
    
    ```
    def update_phrases(cls,
                       model: str,
                       phrase_id: str,
                       phrases: Dict[str, Any],
                       training_type: str = 'compile_asr_phrase',
                       **kwargs)
    ```
    
    Java
    
    ```
    AsrPhraseStatusResult UpdatePhrases(AsrPhraseParam param, String phraseId)
          throws ApiException, NoApiKeyException, InputRequiredException
    ```
    
-   参数配置
    
    对于Java SDK，将使用一个AsrPhraseParam对象作为参数，其方法和参数如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    param
    
    AsrPhraseParam
    
    创建热词的配置参数，见上文关于AsrPhraseParam类型的描述，对于UpdatePhrase调用，不需要填pageNo和pageSize字段。
    
    phraseId
    
    String
    
    调用CreatePhrases，UpdatePhrases, QueryPhrase等接口返回的AsrPhraseStatusOutput对象后，通过该对象的getFineTunedOutput返回的热词ID，String类型。调用ListPhrases时，使用AsrPhraseStatusOutput对象的getFinetunedOutputs接口将返回所有热词信息的列表，然后使用AsrPhraseInfo的getFineTunedOutput即可获取对应热词的热词ID。
    
    对于Python SDK，其参数如下：
    
    **参数**
    
    **类型**
    
    **默认值**
    
    **说明**
    
    model
    
    _str_
    
    \-
    
    指定用于音视频文件转写的Paraformer模型名，关于如何进行模型选择，请参考：[支持的模型](#cc235e90699kg)。
    
    phrase\_id
    
    str
    
    \-
    
    调用create\_phrases，update\_phrases, query\_phrases等接口返回的Dict对象，通过finetuned\_output访问对应phrase\_id。
    
    phrases
    
    _Dict\[str, Any\]_
    
    \-
    
    热词列表，是一个Dict类型对象，其中键为热词文本，值为热词对应权重。对于热词要求请参考下方重要一栏。
    
    training\_type
    
    str
    
    compile\_asr\_phrase
    
    固定为compile\_asr\_phrase
    
-   返回示例
    
    ```
    {
    	"status_code": 200,
    	"request_id": "8c8d64e3-5198-9624-99cd-e9dcf7eb22f6",
    	"code": null,
    	"message": "",
    	"output": {
    		"job_id": "ft-202309261543-b0ae",
    		"status": "SUCCEEDED",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    		"training_type": "compile_asr_phrase",
    		"create_time": "2023-09-26 15:43:09"
    	},
    	"usage": null,
    	"job_id": "ft-202309261543-b0ae",
    	"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    	"finetuned_outputs": null,
    	"training_type": null,
    	"create_time": "2023-09-26 15:43:09",
    	"output_type": null,
    	"model": null
    }
    ```
    
-   调用示例
    
    Python
    
    ```
    # coding=utf-8
    
    import dashscope
    from dashscope.audio.asr import AsrPhraseManager
    
    dashscope.api_key='your-dashscope-api-key'
    
    phrases = {'通义千问': 2}
    
    result = AsrPhraseManager.update_phrases(model='paraformer-realtime-v1',
                                             phrase_id='phrase-id',
                                             phrases=phrases)
    if result.output is not None:
        print('update phrases: ', result.output)
    else:
        print('Error: ', str(result))
    ```
    
    Java
    
    ```
    package com.alibaba.test;
    
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseManager;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseParam;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseStatusResult;
    import com.alibaba.dashscope.audio.asr.recognition.Recognition;
    import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
    import com.alibaba.dashscope.utils.Constants;
    import java.util.Collections;
    
    class Test {
      
      public static void main(String[] args) {
        AsrPhraseParam param = AsrPhraseParam.builder()
          .model("your-model")
          .phraseList(Collections.singletonMap("通义千问", 2))
          .apiKey("your-dashscope-api-key")
          .build();
    
        AsrPhraseStatusResult result = null;
        try {
          result = AsrPhraseManager.UpdatePhrases(param, "phrase-id");
          if (result.getOutput() != null) {
            System.out.println("update phrases: " + result.getOutput());
          } else {
            System.out.println("err: " + result);
          }
        } catch (Exception e) {
          throw new RuntimeException(e);
        }
      }
    }
    ```
    

### 删除热词

该接口将以同步调用的形式提交一个热词删除请求。

-   接口
    
    Python
    
    ```
    def delete_phrases(cls, phrase_id: str,
                       **kwargs)
    ```
    
    Java
    
    ```
    AsrPhraseStatusResult DeletePhrase(AsrPhraseParam param, String phraseId)
          throws ApiException, NoApiKeyException, InputRequiredException
    ```
    
-   参数配置
    
    对于Java SDK，将使用一个AsrPhraseParam对象作为参数，其方法和参数如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    param
    
    AsrPhraseParam
    
    创建热词的配置参数，见上文关于AsrPhraseParam类型的描述，对于DeletePhrase调用，不需要填phraseList, pageNo和pageSize字段。
    
    phraseId
    
    String
    
    调用CreatePhrases，UpdatePhrases, QueryPhrase等接口返回的AsrPhraseStatusOutput对象后，通过该对象的getFineTunedOutput返回的热词ID，String类型。调用ListPhrases时，使用AsrPhraseStatusOutput对象的getFinetunedOutputs接口将返回所有热词信息的列表，然后使用AsrPhraseInfo的getFineTunedOutput即可获取对应热词的热词ID。
    
    对于Python SDK，其参数如下：
    
    **参数**
    
    **类型**
    
    **默认值**
    
    **说明**
    
    phrase\_id
    
    str
    
    \-
    
    调用create\_phrases，update\_phrases, query\_phrases等接口返回的Dict对象，通过finetuned\_output访问对应phrase\_id。
    
-   返回示例
    
    ```
    {
    	"status_code": 200,
    	"request_id": "00bb0287-2593-94a3-8e21-93c90f5e9dd8",
    	"code": null,
    	"message": "",
    	"output": {
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1"
    	},
    	"usage": null,
    	"job_id": null,
    	"finetuned_output": "paraformer-realtime-v1-ft-202309261539-2af1",
    	"finetuned_outputs": null,
    	"training_type": null,
    	"create_time": null,
    	"output_type": null,
    	"model": null
    }
    ```
    
-   调用示例
    
    Python
    
    ```
    # coding=utf-8
    
    import dashscope
    from dashscope.audio.asr import AsrPhraseManager
    
    dashscope.api_key='your-dashscope-api-key'
    
    result = AsrPhraseManager.delete_phrases(phrase_id='phrase-id')
    if result.output is not None:
        print('delete phrases: ', result.output)
    else:
        print('Error: ', str(result))
    ```
    
    Java
    
    ```
    package com.alibaba.test;
    
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseManager;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseParam;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseStatusResult;
    import com.alibaba.dashscope.audio.asr.recognition.Recognition;
    import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
    import com.alibaba.dashscope.utils.Constants;
    
    class Test {
      
      public static void main(String[] args) {
        AsrPhraseParam param = AsrPhraseParam.builder()
                .model("your-model")
                .apiKey("your-dashscope-api-key")
                .build();
    
        AsrPhraseStatusResult result = null;
        try {
          result = AsrPhraseManager.DeletePhrase(param, "phrase-id");
          if (result.getOutput() != null) {
            System.out.println("delete phrases: " + result.getOutput());
          } else {
            System.out.println("Error: " + result);
          }
        } catch (Exception e) {
          throw new RuntimeException(e);
        }
      }
    }
    ```
    

### 列表形式返回所有热词

该接口将以同步调用的形式提交一个返回所有热词的请求。

-   接口
    
    Python
    
    ```
    def list_phrases(cls,
                     page: int = 1,
                     page_size: int = 10,
                     **kwargs)
    ```
    
    Java
    
    ```
    AsrPhraseStatusResult ListPhrases(AsrPhraseParam param)
          throws ApiException, NoApiKeyException, InputRequiredException
    ```
    
-   参数配置
    
    对于Java SDK，将使用一个AsrPhraseParam对象作为参数，其方法和参数如下：
    
    **参数**
    
    **类型**
    
    **说明**
    
    param
    
    AsrPhraseParam
    
    创建热词的配置参数，见上文关于AsrPhraseParam类型的描述，对于ListPhrases调用，不需要填phraseList字段。
    
    phraseId
    
    String
    
    调用CreatePhrases，UpdatePhrases, QueryPhrase等接口返回的AsrPhraseStatusOutput对象后，通过该对象的getFineTunedOutput返回的热词ID，String类型。调用ListPhrases时，使用AsrPhraseStatusOutput对象的getFinetunedOutputs接口将返回所有热词信息的列表，然后使用AsrPhraseInfo的getFineTunedOutput即可获取对应热词的热词ID。
    
    对于Python SDK，其参数如下：
    
    **参数**
    
    **类型**
    
    **默认值**
    
    **说明**
    
    page
    
    int
    
    1
    
    当请求是list\_phrases有效，用于查询第几页列表，默认1
    
    page\_size
    
    int
    
    10
    
    当请求是list\_phrases有效，用于设置分页大小，默认10
    
-   返回示例
    
    ```
    {
    	"status_code": 200,
    	"request_id": "95f969ef-bcbc-9bb5-b05d-4caed9326409",
    	"code": null,
    	"message": "",
    	"output": {
    		"page_no": 1,
    		"page_size": 5,
    		"total": 61,
    		"finetuned_outputs": [{
    			"create_time": "2023-09-26 15:32:20",
    			"finetuned_output": "paraformer-realtime-v1-ft-202309261532-93bf",
    			"job_id": "ft-202309261532-93bf",
    			"model": "paraformer-realtime-v1",
    			"output_type": "custom_resource"
    		}, {
    			"create_time": "2023-09-26 15:32:18",
    			"finetuned_output": "paraformer-realtime-v1-ft-202309261532-7b51",
    			"job_id": "ft-202309261532-7b51",
    			"model": "paraformer-realtime-v1",
    			"output_type": "custom_resource"
    		}, {
    			"create_time": "2023-09-26 15:32:17",
    			"finetuned_output": "paraformer-realtime-v1-ft-202309261532-8bbc",
    			"job_id": "ft-202309261532-cef0",
    			"model": "paraformer-realtime-v1",
    			"output_type": "custom_resource"
    		}, {
    			"create_time": "2023-09-26 15:32:16",
    			"finetuned_output": "paraformer-realtime-v1-ft-202309261532-fc6a",
    			"job_id": "ft-202309261532-fc6a",
    			"model": "paraformer-realtime-v1",
    			"output_type": "custom_resource"
    		}, {
    			"create_time": "2023-09-26 15:31:56",
    			"finetuned_output": "paraformer-realtime-v1-ft-202309261531-e92d",
    			"job_id": "ft-202309261531-e92d",
    			"model": "paraformer-realtime-v1",
    			"output_type": "custom_resource"
    		}]
    	},
    	"usage": null,
    	"job_id": null,
    	"finetuned_output": null,
    	"finetuned_outputs": [{
    		"create_time": "2023-09-26 15:32:20",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261532-93bf",
    		"job_id": "ft-202309261532-93bf",
    		"model": "paraformer-realtime-v1",
    		"output_type": "custom_resource"
    	}, {
    		"create_time": "2023-09-26 15:32:18",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261532-7b51",
    		"job_id": "ft-202309261532-7b51",
    		"model": "paraformer-realtime-v1",
    		"output_type": "custom_resource"
    	}, {
    		"create_time": "2023-09-26 15:32:17",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261532-8bbc",
    		"job_id": "ft-202309261532-cef0",
    		"model": "paraformer-realtime-v1",
    		"output_type": "custom_resource"
    	}, {
    		"create_time": "2023-09-26 15:32:16",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261532-fc6a",
    		"job_id": "ft-202309261532-fc6a",
    		"model": "paraformer-realtime-v1",
    		"output_type": "custom_resource"
    	}, {
    		"create_time": "2023-09-26 15:31:56",
    		"finetuned_output": "paraformer-realtime-v1-ft-202309261531-e92d",
    		"job_id": "ft-202309261531-e92d",
    		"model": "paraformer-realtime-v1",
    		"output_type": "custom_resource"
    	}],
    	"training_type": null,
    	"create_time": null,
    	"output_type": null,
    	"model": null
    }
    ```
    
-   调用示例
    
    Python
    
    ```
    # coding=utf-8
    
    import dashscope
    from dashscope.audio.asr import AsrPhraseManager
    
    dashscope.api_key='your-dashscope-api-key'
    
    result = AsrPhraseManager.list_phrases()   
    if result.output is not None:
        print('list phrases: ', result.output)
    else:
        print('Error: ', str(result))
    ```
    
    Java
    
    ```
    package com.alibaba.test;
    
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseManager;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseParam;
    import com.alibaba.dashscope.audio.asr.phrase.AsrPhraseStatusResult;
    import com.alibaba.dashscope.audio.asr.recognition.Recognition;
    import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
    import com.alibaba.dashscope.utils.Constants;
    
    class Test {
      
      public static void main(String[] args) {
        AsrPhraseParam param = AsrPhraseParam.builder()
                .model("your-model")
                .apiKey("your-dashscope-api-key")
                .build();
    
        AsrPhraseStatusResult result = null;
        try {
          result = AsrPhraseManager.ListPhrases(param);
          if (result.getOutput() != null) {
            System.out.println("list phrases: " + result.getOutput());
          } else {
            System.out.println("Error: " + result);
          }
        } catch (Exception e) {
          throw new RuntimeException(e);
        }
      }
    }
    ```
