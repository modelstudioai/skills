# 常见问题

图像API接口的通用问题汇总，包含接口调试、模型计费与限流、接口高频报错等。

本文涉及的图像模型有：文生图V1和V2、涂鸦作画、图像局部重绘、Cosplay动漫人物生成、人像风格重绘、虚拟模特、鞋靴模特、图像画面扩展、人物实例分割、图像擦除补全、创意海报生成、图像背景生成、图配文。

## **本地调试接口**

图像API均支持HTTP调用。下面以文生图API为例展示本地调试HTTP接口的流程。

1.  需要[开通模型服务并获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
2.  在图像API文档中找到`curl`命令。
    

**示例：文生图curl命令**

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-t2i-turbo",
    "input": {
        "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
    },
    "parameters": {
        "size": "1024*1024",
        "n": 1
    }
}'
```

3.  若操作系统为macOS或Linux，可在终端执行curl命令。
    
4.  若操作系统为Windows，可使用Postman、Apifox等接口平台发送HTTP请求。
    

> 注意：使用接口平台发送请求时，需要将curl命令`Bearer $DASHSCOPE_API_KEY`中的`$DASHSCOPE_API_KEY`替换为真实API\_KEY，比如`Bearer sk-xxxxxx`。

## **模型计费与限流**

**模型计费示例**

> 注：表格中图像模型1、图像模型2仅用作示例说明，不是真实的模型名称。

**模型名称**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**计费单价**

**限流（主账号与RAM子账号共用）**

**任务下发接口QPS限制**

**同时处理中任务数量**

图像模型1

500张

限时免费

2

1

图像模型2

500张

0.02元/张

2

1

**免费额度**

-   额度说明：免费额度是指模型成功生成的输出图片数量。输入图片及模型处理失败的情况不占用免费额度。
    
-   领取方式：开通阿里云百炼大模型服务后自动发放，有效期90天。
    
-   使用账号：阿里云主账号与其RAM子账号共享免费额度。
    
-   更多详情请参见[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    

**限时免费**

-   当计费为“限时免费”时，表示该模型处于公测阶段，免费额度用尽后不可使用。
    

**计费说明**

-   当计费有明确单价时，如0.02元/张，表示该模型已商业化，免费额度用尽或过期后需付费使用。
    
-   计费项：只对模型成功生成的输出图片进行收费，其余情况暂不计费。
    
-   付费方式：由阿里云主账号统一付费。RAM子账号不能独立计量计费，必须由所属的主账号付费。如果您需要查询账单信息，请前往阿里云控制台[账单概览](https://billing-cost.console.aliyun.com/finance/month-bill/account)。
    
-   充值途径：您可以在阿里云控制台[费用与成本](https://billing-cost.console.aliyun.com/home?spm=a2c4g.11186623.0.0.2d543048F4KRQP)页面进行充值。
    
-   模型调用情况：您可以前往阿里云百炼平台的[模型观测](https://bailian.console.aliyun.com/#/model-telemetry)查看模型调用量及调用次数。
    
-   更多计费问题请参见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。
    

**限流**

-   限流说明：阿里云主账号与其RAM子账号共享限流限制。
    

## **接口报错**

### **图像无法下载或下载失败**

**报错场景**：当使用您自己的图片链接（非文档示例图片链接）请求接口时，报错提示“下载图片失败，请检查图片url”。

```
{
    "request_id": "657f0d1b-76d0-9e3e-b6d6-xxxxxx",
    "output": {
        "task_id": "5e6fa974-9a25-4271-8659-xxxxxx",
        "task_status": "FAILED",
        "code": "BadRequest.InputDownloadFailed",
        "message": "Reference image download failed, please check image url."
    }
}
```

**可能原因**：输入的图片URL链接存在错误、无法访问或下载权限受限等问题，导致模型服务无法成功下载图片。

**解决方案**：请确保图片URL链接完整，并能够支持公网访问。您可以将图片上传至可供公网访问的自建存储服务，或选择上传至OSS等云存储服务。请务必确保图片URL能够支持公网访问。

### **创建任务接口的curl命令执行失败**

**报错场景**：如果您在文档中复制创建任务接口的curl命令，执行后报错。下面以图像背景生成模型的curl命令为例。

**示例：图像背景生成-创建任务接口curl命令**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx-background-generation-v2",
    "input": {
        "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
        "ref_image_url": "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg",
        "ref_prompt": "山脉和晚霞",
        "reference_edge": {
            "foreground_edge": [
                "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/huaban_soft_edge/6cdd13941cef1b11d885aea1717b983ae566b8efc9094-vcsvxa_fw658webp.png",
                "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/2c36cc4b7da027279e87311dac48fc2d5d784b1e72c0e-x4f1wC_fw658webp.png"
            ],
            "background_edge": [
                "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/0718a9741e07c52ca5506e75c4f2b99e22fff68a4c7d3-P9WGLr_fw658webp.png"
            ],
            "foreground_edge_prompt": [
                "粉色桃花",
                "可爱小狗"
            ],
            "background_edge_prompt": [
                "树叶"
            ]
        }
    },
    "parameters": {
        "n": 4,
        "ref_prompt_weight": 0.5,
        "model_version": "v3"
    }
}'
```

报错信息显示“请求Body格式无效”。

```
{
    "request_id": "d306ae65-3f6d-9d6c-acfb-xxxxxx",
    "code": "InvalidParameter",
    "message": "Required body invalid, please check the request body format."
}
```

**可能原因**：创建任务接口的请求Body中存在中文字符。如果执行curl命令的客户端不支持解析中文，可能会导致请求Body解析异常，从而引发报错。

**解决方案**：macOS或者Linux系统用户直接在终端执行curl命令即可。Windows用户建议使用HTTP接口平台发送请求，如Postman、Apifox等。

### **海外调用API接口显示资源下载超时**

**报错场景**：您在海外调用接口，且图片资源存储于非中国内地地域，较大概率出现资源下载超时报错，报错信息如下所示。

```
Download the media resource timed out during the data inspection process
```

**主要原因**：非中国内地地区存在不稳定因素，因此在下载图片时会导致超时情况。

**解决方案**：请将图片资源存储在中国内地的地域，并配置加速。注意，当前不支持配置主账号的图片下载超时时间。
