# 声音复刻Java SDK参考

本文介绍声音复刻的Java SDK使用方法。

**用户指南：**[声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)。

## **服务地址**

SDK默认使用**北京地域**的服务端点。如需切换到其他地域，需在初始化前修改 `Constants.baseHttpApiUrl`。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`https://dashscope.aliyuncs.com/api/v1`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`https://dashscope-intl.aliyuncs.com/api/v1`

**切换到新加坡地域**：

```
import com.alibaba.dashscope.common.Constants;

// 在代码开头设置
Constants.baseHttpApiUrl = "https://dashscope-intl.aliyuncs.com/api/v1";
```

**注意**：

-   不同地域的 API Key 不同，请确保使用对应地域的 API Key
    
-   地域配置为全局设置，影响所有 DashScope SDK 的 API 调用
    

## **VoiceEnrollmentService 类**

**包路径**：`com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService`

**功能**：管理CosyVoice复刻音色的生命周期（创建、查询、更新、删除）

### **构造方法**

```
public VoiceEnrollmentService(String apiKey)
```

**参数说明**：

**参数**

**类型**

**说明**

apiKey

String

API Key

### **createVoice() - 创建音色**

**方法签名**：

```
public Voice createVoice(String targetModel, String prefix, String url, VoiceEnrollmentParam customParam) throws NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

targetModel

String

是

驱动音色的语音合成模型。必须与后续调用语音合成接口时使用的模型一致，否则合成会失败。

prefix

String

是

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-{prefix}-{唯一标识}`。

url

String

是

用于复刻音色的音频文件URL，要求公网可访问。

customParam

[VoiceEnrollmentParam](#h3-vj1s7t3u)

否

自定义参数，可指定languageHints、maxPromptAudioLength等。

**返回值**：`Voice` 对象，通过 `getVoiceId()` 方法获取音色ID。

### **listVoice() - 查询音色列表**

**方法签名**：

```
public Voice[] listVoice(String prefix, int pageIndex, int pageSize) throws NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

prefix

String

否

按音色名称前缀筛选。

pageIndex

int

否

页码索引，从0开始。

pageSize

int

否

每页数据条数。

**返回值**：`Voice[]` 音色数组。

### **queryVoice() - 查询音色详情**

**方法签名**：

```
public Voice queryVoice(String voiceId) throws NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

voiceId

String

是

要查询的音色ID。

**返回值**：`Voice` 对象。

### **updateVoice() - 更新音色**

**方法签名**：

```
public void updateVoice(String voiceId, String url, VoiceEnrollmentParam customParam) throws NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

voiceId

String

是

要更新的音色ID。

url

String

是

新的音频文件URL。

customParam

VoiceEnrollmentParam

否

自定义参数。

### **deleteVoice() - 删除音色**

**方法签名**：

```
public void deleteVoice(String voiceId) throws NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

voiceId

String

是

要删除的音色ID。

## **VoiceEnrollmentParam 类**

**包路径**：`com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentParam`

通过Builder模式构建参数对象。

**方法**

**类型**

**说明**

model(String)

String

声音复刻模型，固定为"voice-enrollment"。

languageHints(List<String>)

List<String>

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash、v3-plus和v3-flash模型支持。

辅助模型识别样本音频的语种，从而更准确地提取音色特征，提升复刻效果。若设置的语种与实际音频语种不符（例如为中文音频设置 `en`），系统将忽略该设置并自动检测语种。

此参数为数组，但当前版本仅处理第一个元素。

取值范围（因模型而异）：

-   cosyvoice-v3-plus：
    
    -   zh：中文
        
    -   en：英文
        
    -   fr：法语
        
    -   de：德语
        
    -   ja：日语
        
    -   ko：韩语
        
    -   ru：俄语
        
-   cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash：
    
    -   zh：中文
        
    -   en：英文
        
    -   fr：法语
        
    -   de：德语
        
    -   ja：日语
        
    -   ko：韩语
        
    -   ru：俄语
        
    -   pt：葡萄牙语
        
    -   th：泰语
        
    -   id：印尼语
        
    -   vi：越南语
        

默认值：\["zh"\]。

maxPromptAudioLength(Float)

Float

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash和v3-flash模型支持。

音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：\[3.0, 30.0\]。时间越长效果越好。

默认值：10.0。

parameter(String, Object)

Object

设置[扩展参数](#a18b66cba924j)，如 parameter("enable\_preprocess", false)。

### **扩展参数**

**参数名**

**类型**

**必填**

**说明**

enable\_preprocess

boolean

否

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash和v3-flash模型支持。

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

## **示例代码**

### **创建音色**

```
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentParam;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String targetModel = "cosyvoice-v3-plus";
        String prefix = "myvoice";
        String fileUrl = "https://your-audio-file-url";
        String cloneModelName = "voice-enrollment";

        try {
            VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
            Voice myVoice = service.createVoice(
                    targetModel,
                    prefix,
                    fileUrl,
                    VoiceEnrollmentParam.builder()
                            .model(cloneModelName)
                            .languageHints(Collections.singletonList("zh"))
                            // .maxPromptAudioLength(10.0f)
                            // .parameter("enable_preprocess", false)
                            .build());

            logger.info("Voice creation submitted. Request ID: {}", service.getLastRequestId());
            logger.info("Generated Voice ID: {}", myVoice.getVoiceId());
        } catch (Exception e) {
            logger.error("Failed to create voice", e);
        }
    }
}
```

### **查询音色列表**

需要引入第三方库`com.google.gson.Gson`。

```
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.Gson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");  // 如果您没有配置环境变量，请在此处用您的API-KEY进行替换
    private static String prefix = "myvoice"; // 请按实际情况进行替换
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args)
            throws NoApiKeyException, InputRequiredException {
        VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
        // 查询音色
        Voice[] voices = service.listVoice(prefix, 0, 10);
        logger.info("List successful. Request ID: {}", service.getLastRequestId());
        logger.info("Voices Details: {}", new Gson().toJson(voices));
    }
}
```

### **查询特定音色**

需要引入第三方库`com.google.gson.Gson`。

```
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.Gson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");  // 如果您没有配置环境变量，请在此处用您的API-KEY进行替换
    private static String voiceId = "cosyvoice-v3-plus-myvoice-xxx"; // 请按实际情况进行替换
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args)
            throws NoApiKeyException, InputRequiredException {
        VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
        Voice voice = service.queryVoice(voiceId);

        logger.info("Query successful. Request ID: {}", service.getLastRequestId());
        logger.info("Voice Details: {}", new Gson().toJson(voice));
    }
}
```

### **更新音色**

```
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");  // 如果您没有配置环境变量，请在此处用您的API-KEY进行替换
    private static String fileUrl = "https://your-audio-file-url";  // 请按实际情况进行替换
    private static String voiceId = "cosyvoice-v3-plus-myvoice-xxx"; // 请按实际情况进行替换
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args)
            throws NoApiKeyException, InputRequiredException {
        VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
        // 更新音色
        service.updateVoice(voiceId, fileUrl);
        logger.info("Update submitted. Request ID: {}", service.getLastRequestId());
    }
}
```

### **删除音色**

```
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");  // 如果您没有配置环境变量，请在此处用您的API-KEY进行替换
    private static String voiceId = "cosyvoice-v3-plus-myvoice-xxx"; // 请按实际情况进行替换
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args)
            throws NoApiKeyException, InputRequiredException {
        VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
        // 删除音色
        service.deleteVoice(voiceId);
        logger.info("Deletion submitted. Request ID: {}", service.getLastRequestId());
    }
}
```
