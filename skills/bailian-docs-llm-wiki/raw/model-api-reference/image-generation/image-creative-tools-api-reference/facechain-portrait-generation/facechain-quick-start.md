# 快速开始

**重要**

-   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   人物写真生成API调用需"[申请体验](https://bailian.console.aliyun.com/model/market/detail/facechain-generation)"并通过后才可使用，否则API调用将返回错误状态码。

## 万相

**说明**支持的领域 / 任务：aigc

人物写真2.0支持人物形象训练lora模式和人物形象免训练trainfree模式。

1）人物形象训练lora模式：基于人物形象训练模型已经得到的人物形象lora，可以继续通过人物生成写真模型完成该形象的高保真写真生成，支持多种预设风格，包括证件照、商务写真、复古风、夏日运动等风格，同时支持客户自定义风格模板上传方式生成自定义人物写真照。

2）人物形象免训练trainfree模式【推荐】：同时上传一组包含用户正脸单人照（至少一张）和客户自定义风格模板，通过人物生成写真模型直接一键免训练极速生成人物写真照，仅支持客户自定义风格模板上传方式免训练trainfree生成写真。

人物形象训练lora方式说明：

-   人物形象训练lora方式流程图：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792558.png)

关于该接口功能的示例图如下：

-   输入图像

![640.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7295738961/p731277.png)

-   生成结果（商务写真）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792562.png)

-   预设风格模板

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792563.png)

-   客户自定义模板：
-   输入图像

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792561.png)

-   自定义模板

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792565.jpeg)

-   生成结果

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792564.jpeg)

人物形象免训练trainfree方式说明：

-   人物形象免训练trainfree方式流程图：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792566.png)

人物形象免训练trainfree方式上，基于内置强大的人物写真照预训练大模型技术，实现人物写真扩散模型的图像极速生成能力，一键免训练极速生成人物写真照，并叠加一系列后处理能力，实现兼具相似度、真实感、美观度的写真生成能力，人物写真可以实现高度个性化、高品质、高丰富度、极速出图能力。

关于该接口功能的示例图如下：

-   输入图像

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792568.jpeg)

-   自定义模板

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792569.jpeg)

-   生成结果

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0399433171/p792567.jpeg)

## 快速开始

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

## 功能介绍

### 使用流程

1.  开通大模型服务平台，获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
2.  点击“[申请体验](https://bailian.console.aliyun.com/model/market/detail/facechain-generation)”申请FaceChain人物写真生成体验权限，并获得通过；
3.  开发调用人物图像检测API，进行用户上传图像的质量校验，非必选链路，可以用于产品中进行前置校验，及时提醒用户更换质量不合格的图像。详情参考[人物图像检测API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)；
4.  图像文件打包，上传并管理文件，详情参考[百炼文件管理 API](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service)；
5.  开发调用人物形象训练API，进行自定义人物的模型定制，并获得定制模型ID。详情参考[人物形象训练API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)；
6.  基于已经训练完成的定制模型ID，开发调用人物写真生成API，选择目标风格模板，发起请求并获得写真结果。详情参考[人物写真生成API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)；

## 示例代码

**说明**以下代码演示了如何使用facechain提供的原生api来进行人物形象训练以及使用训练产生的资源来生成人物写真，运行下述代码时：

-   需要使用您的API-KEY替换示例中的YOUR\_DASHSCOPE\_API\_KEY，代码才能正常运行。
-   安装相关依赖
-   请注意，您需要按照代码中注释的提示，替换相关文件路径

如果您手头暂时没有合适的照片，您可以下载我们提供的样片：[sample1](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)、[sample2](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample2.jpg)、[sample3](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample3.jpg)

### 依赖及代码

```
<dependency>
  <groupId>com.alibaba</groupId>
  <artifactId>fastjson</artifactId>
  <version>the-latest-version2</version>
</dependency>
```
```
package com.alibaba.jing.demo;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

public class FacechainDemo {
    private static final String API_KEY = "YOUR_DASHSCOPE_API_KEY";

    private static final String REQUEST_FORMAT = "{\n"
        + "    \"model\": \"facechain-generation\",\n"
        + "    \"input\": {\n"
        + "        \"description\": \"sample\"\n"
        + "    },\n"
        + "    \"parameters\": {\n"
        + "        \"style\": \"f_business_male\",\n"
        + "        \"size\": \"768*1024\",\n"
        + "        \"n\": 4\n"
        + "    },\n"
        + "    \"resources\": [\n"
        + "        {\n"
        + "            \"resource_id\": \"%s\",\n"
        + "            \"resource_type\": \"facelora\"\n"
        + "        }\n"
        + "    ]\n"
        + "}";

    public static void main(String[] args) throws Exception {
        List<String> sourceFileLocalPaths = new ArrayList<>();
        //以两张本地照片打包为本地zip文件为例
        sourceFileLocalPaths.add("此处替换为您的图片文件本地path，例如 /home/admin/sample/sample1.jpeg");
        sourceFileLocalPaths.add("此处替换为您的图片文件本地path，例如 /home/admin/sample/sample2.jpeg");
        String targetZipFileLocalPath = "此处替换为您希望输出的本地zip包path，例如/home/admin/sample/sample.zip";
        //文件打包
        zipFiles(sourceFileLocalPaths, targetZipFileLocalPath);
        //上传文件至dashscope平台
        JSONObject uploadResponse = uploadFile(targetZipFileLocalPath);
        //获取上传文件后生成的file_id
        String fileId = uploadResponse.getJSONObject("data").getJSONArray("uploaded_files").getJSONObject(0).getString(
            "file_id");
        //发起训练任务
        JSONObject finetuneRequest = new JSONObject();
        //固定值
        finetuneRequest.put("model", "facechain-finetune");
        JSONArray fileIds = new JSONArray();
        fileIds.add(fileId);
        finetuneRequest.put("training_file_ids", fileIds);
        JSONObject createFinetuneResponse = sendPostRequest("https://dashscope.aliyuncs.com/api/v1/fine-tunes",
            finetuneRequest.toJSONString());
        //获取创建的训练任务的任务ID
        String jobId = createFinetuneResponse.getJSONObject("output").getString("job_id");
        //轮询任务至成功
        String queryJobUrl = "https://dashscope.aliyuncs.com/api/v1/fine-tunes/" + jobId;
        String finetunedOutput = null;
        do {
            JSONObject jobQueryResponse = sendGetRequest(queryJobUrl);
            String jobStatus = jobQueryResponse.getJSONObject("output").getString("status");
            if ("SUCCEEDED".equals(jobStatus)) {
                finetunedOutput = jobQueryResponse.getJSONObject("output").getString("finetuned_output");
            } else if ("FAILED".equals(jobStatus)) {
                throw new Exception("the job is failed");
            } else {
                System.out.println("the job " + jobId + " is now " + jobStatus);
                Thread.sleep(10 * 1000);
            }
        } while (Objects.isNull(finetunedOutput));
        //finetuned_output即为
        System.out.println("got the facechian resourceId:" + finetunedOutput);
        //使用训练产生的finetuned_output作为resource调用推理服务，由于推理需要时间较长，此处实际为创建一个异步任务
        String genPotraitRequestString = String.format(REQUEST_FORMAT, finetunedOutput);
        String genPotraitUrl = "https://dashscope.aliyuncs.com/api/v1/services/aigc/album/gen_potrait";
        JSONObject genPotraitTaskResponse = sendPostRequest(genPotraitUrl, genPotraitRequestString);
        //获取推理任务的ID
        String taskId = genPotraitTaskResponse.getJSONObject("output").getString("task_id");
        //轮询推理结果
        String taskQueryUrl = "https://dashscope.aliyuncs.com/api/v1/tasks/" + taskId;
        JSONArray resultImageUrls = null;
        do {
            JSONObject taskQueryResponse = sendGetRequest(taskQueryUrl);
            String jobStatus = taskQueryResponse.getJSONObject("output").getString("task_status");
            if ("SUCCEEDED".equals(jobStatus)) {
                resultImageUrls = taskQueryResponse.getJSONObject("output").getJSONArray("results");
            } else if ("FAILED".equals(jobStatus)) {
                throw new Exception("the task is failed");
            } else {
                System.out.println("the task " + taskId + " is now " + jobStatus);
                Thread.sleep(10 * 1000);
            }
        } while (Objects.isNull(resultImageUrls));
        //此处和获取合成的
        System.out.println("the image urls is :" + resultImageUrls.toJSONString());
    }

    private static void zipFiles(List<String> sourceFileLocalPaths, String targetZipFileLocalPath) {
        try {
            FileOutputStream fos = new FileOutputStream(targetZipFileLocalPath);
            ZipOutputStream zos = new ZipOutputStream(fos);
            byte[] buffer = new byte[1024];

            for (String sourceFile : sourceFileLocalPaths) {
                File file = new File(sourceFile);
                FileInputStream fis = new FileInputStream(file);
                zos.putNextEntry(new ZipEntry(file.getName()));

                int length;
                while ((length = fis.read(buffer)) > 0) {
                    zos.write(buffer, 0, length);
                }

                fis.close();
                zos.closeEntry();
            }

            zos.close();
            System.out.println("Files compressed successfully!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static JSONObject uploadFile(String fileToUpload) {
        StringBuilder responseBuilder = new StringBuilder();
        try {
            URL url = new URL("https://dashscope.aliyuncs.com/api/v1/files");
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            // 设置请求头
            conn.setRequestProperty("Authorization", API_KEY);
            conn.setRequestProperty("Content-Type",
                "multipart/form-data; boundary=---------------------------1234567890");
            // 创建文件流
            File file = new File(fileToUpload);
            FileInputStream fis = new FileInputStream(file);
            // 获取输出流
            OutputStream os = conn.getOutputStream();
            // 写入请求体
            os.write(("-----------------------------1234567890\r\n" +
                "Content-Disposition: form-data; name=\"files\"; filename=\"" + file.getName() + "\"\r\n" +
                "Content-Type: application/octet-stream\r\n" +
                "\r\n").getBytes());

            // 写入文件内容
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }

            // 写入请求结束标志
            os.write(("\r\n-----------------------------1234567890--\r\n").getBytes());

            // 关闭流
            fis.close();
            os.flush();
            os.close();

            // 获取响应码
            int responseCode = conn.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                System.out.println("File upload succeeded");
                // 读取响应体
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String line;
                while ((line = br.readLine()) != null) {
                    responseBuilder.append(line);
                }
                br.close();
            } else {
                System.out.println("File upload failed with response code: " + responseCode);
                // 读取响应体
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
                String line;
                while ((line = br.readLine()) != null) {
                    responseBuilder.append(line);
                }
                br.close();
            }
            System.out.println("File uploaded finished,response=" + responseBuilder.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
        return JSONObject.parseObject(responseBuilder.toString());
    }

    public static JSONObject sendPostRequest(String url, String jsonBody) {
        StringBuilder responseBuilder = new StringBuilder();
        try {
            URL requestUrl = new URL(url);
            HttpURLConnection conn = (HttpURLConnection)requestUrl.openConnection();
            conn.setRequestMethod("POST");

            // 设置请求头
            conn.setRequestProperty("Authorization", API_KEY);
            conn.setRequestProperty("X-DashScope-Async", "enable");//此header仅对调用写真api时生效
            conn.setRequestProperty("Content-Type", "application/json");

            // 设置请求体
            conn.setDoOutput(true);
            DataOutputStream os = new DataOutputStream(conn.getOutputStream());
            os.writeBytes(jsonBody);
            os.flush();
            os.close();

            // 获取响应码
            int responseCode = conn.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 读取响应体
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String line;
                while ((line = br.readLine()) != null) {
                    responseBuilder.append(line);
                }
                br.close();
            } else {
                System.out.println("HTTP POST request failed with response code: " + responseCode);
                // 读取响应体
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
                String line;
                while ((line = br.readLine()) != null) {
                    responseBuilder.append(line);
                }
                br.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("post request response is " + responseBuilder.toString());
        return JSONObject.parseObject(responseBuilder.toString());
    }

    public static JSONObject sendGetRequest(String url) {
        StringBuilder responseBuilder = new StringBuilder();
        try {
            URL requestUrl = new URL(url);
            HttpURLConnection conn = (HttpURLConnection)requestUrl.openConnection();
            conn.setRequestMethod("GET");
            // 设置请求头
            conn.setRequestProperty("Authorization", API_KEY);
            conn.setRequestProperty("Content-Type", "application/json");
            // 获取响应码
            int responseCode = conn.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 读取响应体
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String line;
                while ((line = br.readLine()) != null) {
                    responseBuilder.append(line);
                }
                br.close();
            } else {
                System.out.println("HTTP GET request failed with response code: " + responseCode);
                // 读取响应体
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
                String line;
                while ((line = br.readLine()) != null) {
                    responseBuilder.append(line);
                }
                br.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("get request response is " + responseBuilder.toString());
        return JSONObject.parseObject(responseBuilder.toString());
    }
}
```

## 了解更多

有关facechain人物写真生成API的详细调用文档可前往[人物图像检测API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)、[人物形象训练API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)、[人物写真生成API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)页面进行了解。
