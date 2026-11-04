# 智能纪要前端应用示例

本文介绍如何通过开源的JS SDK，快速搭建智能纪要前端应用示例（Demo）。

## 重要提示

1.  **API 密钥安全**: 切勿将 API Key 硬编码或提交到代码仓库，建议使用环境变量进行管理。
2.  **浏览器权限**: 实时录音功能需要用户授权浏览器麦克风权限。
3.  **网络要求**: 项目运行需要访问阿里云百炼服务，请确保网络通畅。
4.  **重要说明**: **本项目中的依赖包均未发布到公共 npm 仓库。如需二次开发或发布，请自行重命名包名。**

## 功能特性

该 SDK 包含构建智能纪要应用的以下核心功能：

**功能**

**说明**

音视频文件处理

持上传音视频文件，进行语音转写、说话人分离，并生成摘要、章节速览等智能纪要。

实时录音

支持从麦克风实时采集音频，进行实时语音识别、翻译，并在结束后生成完整智能纪要。

纪要整理

支持对已完成的任务进行二次AI分析，如摘要优化、问答提取等。

[**在线体验 Live Demo**](https://www.aliyun.com/exp/tingwu-agent)

点击上方链接体验完整功能，或通过下方截图了解核心特性。

智能纪要Web界面示例**：**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8859485671/p1031107.png)

## 快速入门

### 1\. 前提条件

在开始之前，请确保您已完成以下准备工作：

步骤

操作说明

获取地址

1

**注册阿里云账号**

[阿里云官网](https://www.aliyun.com/)

2

**开通百炼模型服务**

[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)

3

**获取 API Key**

[API Key 管理](https://bailian.console.aliyun.com/?tab=model#/api-key)

4

**创建应用并获取 App ID**

[应用管理](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-meeting-summary)

**详细获取步骤** **API Key 获取步骤：**

1.  登录 [阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)。
2.  在左侧导航栏选择“API-KEY”。
3.  点击“创建新的 API Key”。
4.  复制生成的 API Key。

**App ID 获取步骤：**

1.  登录 [阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-meeting-summary)。
    
2.  点击“创建应用”以生成您的应用。
    
3.  在应用卡片上找到并复制“应用 ID”。
    
    1.  ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8859485671/p1034158.png)

### 2\. 项目配置与启动

请按照以下步骤启动项目：

#### 环境要求

-   **Node.js**: 版本 ≥ 18.0.0
-   **包管理器**: npm

#### 启动步骤

1.  **下载项目**：下载离线文件获取项目代码。

离线文件：[tingwu-web.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260209/dxivsw/tingwu-web.zip)

1.  **安装依赖**

```
cd tingwu-web
npm install
```

2.  **配置 API 密钥（重要！）**
    
    编辑 `.env` 文件，将以下占位符（xxxxx）替换为您的实际值，请务必将 `.env` 文件添加到项目的 `.gitignore` 文件中，以防密钥泄露。：
    

```
#TODO 修改成自己的API_KEY和APP_ID
REACT_APP_API_KEY=xxxxx
REACT_APP_APP_ID=xxxxx
```

3.  **启动开发服务器**

```
npm run start
```

4.  **查看效果**
    
    在浏览器中打开：[http://localhost:3000](http://localhost:3000)
    
    项目将自动在浏览器中打开并显示前端界面。
    

## API 使用指南

### 功能使用示例

**注意：**本SDK不负责文件上传，您需要自行将文件上传至您的服务器或对象存储（OSS），然后将文件的公开访问URL提供给SDK。

#### 音视频文件上传

**功能**: 上传音频或视频文件，自动进行语音识别和内容转录。

**使用须知**:

-   支持单轨或双轨的mp3、wav、m4a、wma、aac、ogg、amr、flac、aiff格式的音频文件和mp4、wmv、m4v、flv、rmvb、dat、mov、mkv、webm、avi、mpeg、3gp、ogg格式的视频文件。
-   文件大小不超过6GB。
-   音频时长不超过6小时。
-   音频采样率8K/16K/24K/48K。

**使用流程**:

1.  点击“选择文件”按钮，选择本地的音频/视频文件。
2.  将文件上传到您自己的业务服务器或OSS。
3.  调用 `createTask` 接口创建任务。请将代码中的 `appId` 替换为您的实际值，并根据需求自定义 `parameters` 和 `analysis` 参数。
4.  调用 `getTask` 接口查询任务解析状态。参数中的 `dataId` 来自上一步 `createTask` 接口的返回值。

**代码示例**:

```
const { output, code } = await createTaskAPI({
input: {
 task: "createTask",
 type: "offline",
 fileUrl, //文件上传到自己业务的 oss或服务器 后得到的文件链接
 appId: "你的APP_ID",
},
parameters: {
 transcription: {
   diarizationEnabled: true,
   diarizationSpeakerCount: 0,
   translationEnabled: false,
 },
 analysis: {},
},
});
```

#### 实时录音

**功能**: 进行实时语音识别，实现边说边转录。

**使用须知**:

-   支持的输入格式：PCM（无压缩的PCM或WAV文件）、OPUS、SPEEX、MP3、AAC格式，16 bit采样位数、单声道（mono）。
-   支持的音频采样率：16000 Hz、8000Hz。
-   支持的单次记录时长：24小时。

**使用流程**

1.  开始录音前，请校验并确保浏览器麦克风权限已开启。
    
2.  调用 `createTask` 接口创建实时任务。请替换 `appId` 并按需配置参数。
    
    **代码示例**:
    

```
const requestParams = {
input: {
 task: "createTask",
 type: "realtime",
 format: "pcm",
 sampleRate: 16000,
 appId: "你的APP_ID",
},
parameters: {
 transcription: {
   model: language,
   diarizationEnabled: true,
   diarizationSpeakerCount: 0,
   translationTargetLang: "zh",
   translationEnabled: true,
 },
 analysis: {},
},
};
```

3.建立 WebSocket 连接。本示例包含心跳及重连机制（最多重试3次）。

4.WSS链接获取方案：1) 服务端返回完整链接；2) 前端拼接链接，服务端返回临时Token。本示例采用方案2，因临时Token有效期短，每次重连时需重新获取。

5.调用 `getTask` 接口查询任务解析状态。参数中的 `dataId` 来自 `createTask` 接口的返回值。

### 获取与展示结果

#### 智能纪要内容

**功能**: 查看完整的转录结果、摘要、问答、思维导图等AI分析内容。

**包含内容**:

-   **转录文本**: 完整的语音转文字结果。
-   **说话人分离**: 区分不同说话人的发言内容。
-   **智能摘要**: 自动生成会议内容摘要。
-   **问答回顾**: 提取关键问题和答案。
-   **章节速览**: 按时间或内容分段浏览纪要。
-   **翻译功能**: 支持多语言翻译（需在任务创建时开启）。

## 开发者参考

### 系统架构图

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8859485671/p1034440.png)

-   详细内容可以查看项目文件，其路径为「./tingwu-web/docs/ARCHITECTURE.md」

### 项目结构

```
tingwu-web/
├── packages/
│   ├── tingwu-example/     # 示例应用（主要启动入口）
│   ├── tingwu/service/     # API 服务层
│   ├── tingwu-components/  # 组件库
│   ├── tingwu/core/       # 核心逻辑
│   ├── tingwu/summary/       # 听悟智能纪要详情页
│   ├── tingwu/home/       # 开启智能纪要的配置页
│   └── ...                # 其他包
```

### 主要命令

-   `npm run start`: 启动开发服务器
-   `npm run build`: 构建生产版本
-   `npm run lint`: 运行代码检查
-   `npm run test`: 运行测试

## 重要提示

1.  **API 密钥安全**: 切勿将 API Key 硬编码或提交到代码仓库，建议使用环境变量进行管理。
2.  **浏览器权限**: 实时录音功能需要用户授权浏览器麦克风权限。
3.  **网络要求**: 项目运行需要访问阿里云百炼服务，请确保网络通畅。
