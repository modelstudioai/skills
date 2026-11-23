# Qwen Code

在 Qwen Code 中使用阿里云百炼模型。

## 快速接入

选择你使用的客户端，完成配置。

#### CLI

1.  1
    
    连接服务商
    
    运行 `qwen`，首次使用时选择 **Alibaba ModelStudio**，然后按提示选择计费方案。
    
2.  2
    
    选择地域
    
    Region 选择 **China (Beijing)**。
    
3.  3
    
    输入 API Key
    
    #### Token Plan
    
    使用 Token Plan API Key：
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    
    #### 按量计费
    
    使用 [控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)的百炼 API Key。
    
    #### Coding Plan
    
    使用 [控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)的 Coding Plan API Key。
    
4.  4
    
    验证
    
    ```
    qwen -p "你好"
    ```
    

#### 桌面版

1.  1
    
    打开模型设置
    
    点击左下角 **更多** > **设置** > **模型**，点击 **\+ 增加模型**。
    
2.  2
    
    选择供应商
    
    类型选择 **Alibaba ModelStudio**，供应商选择 **Token Plan**、**Coding Plan** 或 **Standard API Key**，地域选择 **China (Beijing)**。
    
3.  3
    
    输入 API Key
    
    -   Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
    -   Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
    -   Coding Plan：使用 [Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)
    -   Standard API Key：使用 [百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
    
4.  4
    
    选择模型并保存
    
    模型 ID 已预置，按需保留或添加。点击 **保存**，在模型列表中选择新添加的模型。
    

#### IDE 插件

1.  1
    
    安装插件
    
    在所用 IDE 的扩展市场安装 **Qwen Code Companion**。
    
2.  2
    
    配置模型
    
    按[通过配置文件接入](#qc-config-file-h)写入所选计费方案的配置。
    
3.  3
    
    打开 Qwen Code
    
    点击 Qwen 图标，或在命令面板运行 `Qwen Code: Open`。
    

## 通过配置文件接入

除了上述方式，也可以通过配置文件接入。

1.  1
    
    打开或新建配置文件
    
    -   macOS / Linux：`~/.qwen/settings.json`
    -   Windows：`C:\Users\<用户名>\.qwen\settings.json`
    
2.  2
    
    写入配置
    
    #### Token Plan 个人版
    
    在[控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) Token Plan API Key，替换 `YOUR_API_KEY`。
    
    ```
    {
      "$version": 4,
      "env": {
        "BAILIAN_TOKEN_PLAN_API_KEY": "YOUR_API_KEY"
      },
      "modelProviders": {
        "openai": [
          {
            "id": "auto",
            "name": "Token Plan auto",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen4-max-preview",
            "name": "Qwen4.0 Max Preview",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen4-max",
            "name": "Qwen4 Max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen3.8-max",
            "name": "Qwen3.8 Max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen3.8-flash",
            "name": "Qwen3.8 Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen3.7-max",
            "name": "Qwen3.7 Max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen3.7-plus",
            "name": "Qwen3.7 Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen3.6-flash",
            "name": "Qwen3.6 Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen-image-3.0-pro",
            "name": "Qwen Image 3.0 Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen-audio-3.0-tts-plus",
            "name": "Qwen Audio 3.0 TTS Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen-audio-3.0-realtime-plus",
            "name": "Qwen Audio 3.0 Realtime Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "qwen-audio-3.0-asr-flash",
            "name": "Qwen Audio 3.0 ASR Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "wan2.7-image",
            "name": "Wan2.7 Image",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "wan2.7-image-pro",
            "name": "Wan2.7 Image Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "wan3.0-video",
            "name": "Wan3.0 Video",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4.1-flash",
            "name": "DeepSeek V4.1 Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4.1-flash-1017",
            "name": "DeepSeek V4.1 Flash 1017",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4-pro",
            "name": "DeepSeek V4 Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4-pro-0813",
            "name": "DeepSeek V4 Pro 0813",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4-flash-0731",
            "name": "DeepSeek V4 Flash 0731",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "glm-5.3",
            "name": "GLM-5.3",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "glm-5.2",
            "name": "GLM-5.2",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "happyhorse-1.1-i2v",
            "name": "HappyHorse 1.1 I2V",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "happyhorse-1.1-t2v",
            "name": "HappyHorse 1.1 T2V",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "happyhorse-1.1-r2v",
            "name": "HappyHorse 1.1 R2V",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "decision-model-preview",
            "name": "Decision Model Preview",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_API_KEY"
          }
        ]
      },
      "security": {
        "auth": {
          "selectedType": "openai"
        }
      },
      "model": {
        "name": "auto"
      }
    }
    ```
    
    #### Token Plan 团队版
    
    在[团队管理](raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)中为成员分配席位并生成 Token Plan API Key，替换 `YOUR_API_KEY`。
    
    ```
    {
      "$version": 4,
      "env": {
        "BAILIAN_TOKEN_PLAN_TEAM_API_KEY": "YOUR_API_KEY"
      },
      "modelProviders": {
        "openai": [
          {
            "id": "auto",
            "name": "Token Plan auto",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen4-max-preview",
            "name": "Qwen4.0 Max Preview",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen4-max",
            "name": "Qwen4 Max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen3.8-max",
            "name": "Qwen3.8 Max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen3.8-flash",
            "name": "Qwen3.8 Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen3.7-max",
            "name": "Qwen3.7 Max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen3.7-plus",
            "name": "Qwen3.7 Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen3.6-plus",
            "name": "Qwen3.6 Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen3.6-flash",
            "name": "Qwen3.6 Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen-image-2.0",
            "name": "Qwen Image 2.0",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen-image-2.0-pro",
            "name": "Qwen Image 2.0 Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen-image-3.0-pro",
            "name": "Qwen Image 3.0 Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen-audio-3.0-tts-plus",
            "name": "Qwen Audio 3.0 TTS Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen-audio-3.0-realtime-plus",
            "name": "Qwen Audio 3.0 Realtime Plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "qwen-audio-3.0-asr-flash",
            "name": "Qwen Audio 3.0 ASR Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "wan2.7-image",
            "name": "Wan2.7 Image",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "wan2.7-image-pro",
            "name": "Wan2.7 Image Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "wan3.0-video",
            "name": "Wan3.0 Video",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "deepseek-v4.1-flash",
            "name": "DeepSeek V4.1 Flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "deepseek-v4.1-flash-1017",
            "name": "DeepSeek V4.1 Flash 1017",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "deepseek-v4-pro",
            "name": "DeepSeek V4 Pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "deepseek-v4-pro-0813",
            "name": "DeepSeek V4 Pro 0813",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "deepseek-v4-flash-0731",
            "name": "DeepSeek V4 Flash 0731",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "kimi-k2.7-code",
            "name": "Kimi K2.7 Code",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "kimi-k2.6",
            "name": "Kimi K2.6",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "glm-5.3",
            "name": "GLM-5.3",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "glm-5.2",
            "name": "GLM-5.2",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "glm-5.1",
            "name": "GLM-5.1",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "glm-5",
            "name": "GLM-5",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "MiniMax-M2.5",
            "name": "MiniMax M2.5",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "happyhorse-1.1-i2v",
            "name": "HappyHorse 1.1 I2V",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "happyhorse-1.1-t2v",
            "name": "HappyHorse 1.1 T2V",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          },
          {
            "id": "happyhorse-1.1-r2v",
            "name": "HappyHorse 1.1 R2V",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_TOKEN_PLAN_TEAM_API_KEY"
          }
        ]
      },
      "security": {
        "auth": {
          "selectedType": "openai"
        }
      },
      "model": {
        "name": "auto"
      }
    }
    ```
    
    #### 按量计费
    
    在[控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)百炼 API Key，替换 `YOUR_API_KEY`，并将 `{WorkspaceId}` 替换为 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。示例为华北2（北京）地域的最新模型，其他模型见[支持的模型](raw/model-user-guide/get-started-with-models/models.md)。
    
    ```
    {
      "$version": 4,
      "env": {
        "BAILIAN_API_KEY": "YOUR_API_KEY"
      },
      "modelProviders": {
        "openai": [
          {
            "id": "qwen3.8-max",
            "name": "Qwen3.8 Max",
            "baseUrl": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_API_KEY"
          },
          {
            "id": "qwen3.7-plus",
            "name": "Qwen3.7 Plus",
            "baseUrl": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_API_KEY"
          },
          {
            "id": "qwen3.8-flash",
            "name": "Qwen3.8 Flash",
            "baseUrl": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_API_KEY"
          },
          {
            "id": "deepseek-v4-pro-0813",
            "name": "DeepSeek V4 Pro 0813",
            "baseUrl": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_API_KEY"
          },
          {
            "id": "deepseek-v4.1-flash",
            "name": "DeepSeek V4.1 Flash",
            "baseUrl": "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "BAILIAN_API_KEY"
          }
        ]
      },
      "security": {
        "auth": {
          "selectedType": "openai"
        }
      },
      "model": {
        "name": "qwen3.8-max"
      }
    }
    ```
    
    #### Coding Plan
    
    在[控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) Coding Plan API Key，替换 `YOUR_API_KEY`。
    
    ```
    {
      "$version": 4,
      "env": {
        "BAILIAN_CODING_PLAN_API_KEY": "YOUR_API_KEY"
      },
      "modelProviders": {
        "openai": [
          {
            "id": "qwen3.7-plus",
            "name": "Qwen3.7 Plus",
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "envKey": "BAILIAN_CODING_PLAN_API_KEY"
          },
          {
            "id": "qwen3.6-plus",
            "name": "Qwen3.6 Plus",
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "envKey": "BAILIAN_CODING_PLAN_API_KEY"
          },
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5",
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "envKey": "BAILIAN_CODING_PLAN_API_KEY"
          },
          {
            "id": "glm-5",
            "name": "GLM-5",
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "envKey": "BAILIAN_CODING_PLAN_API_KEY"
          },
          {
            "id": "MiniMax-M2.5",
            "name": "MiniMax M2.5",
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "envKey": "BAILIAN_CODING_PLAN_API_KEY"
          },
          {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5 Plus",
            "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
            "envKey": "BAILIAN_CODING_PLAN_API_KEY"
          }
        ]
      },
      "security": {
        "auth": {
          "selectedType": "openai"
        }
      },
      "model": {
        "name": "qwen3.7-plus"
      }
    }
    ```
    
    **说明**使用 qwen4-max-preview 时，默认输出上限 32768；长输出可在模型条目内设置 `generationConfig.samplingParams.max_tokens`。
    
    **说明**使用 qwen4-max 时，默认输出上限 32768；长输出可在模型条目内设置 `generationConfig.samplingParams.max_tokens`。qwen4-max 的上下文长度为 1M Token；非思考模式最大输出 131,072 Token，思考与最终回答合计最大 262,144 Token；默认 reasoning\_effort=high，thinking\_budget=131072。
    

**说明**`env` 中的变量名必须与模型条目的 `envKey` 一致；`security.auth.selectedType` 保持 `openai`，`$version` 保持 `4`。

## 接入百炼 CLI

[百炼 CLI](https://bailian.console.aliyun.com/cli) 安装时会把 Skill 注册到 `~/.qwen/skills/bailian-cli/`，Qwen Code 可在对话中调用百炼能力。使用前请安装 [Node.js](https://nodejs.org/zh-cn/download) 18+。

1.  1
    
    安装百炼 CLI
    
    ```
    请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli
    ```
    
2.  2
    
    配置 API Key
    
    在[控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh) API Key，然后告诉 Qwen Code：
    
    ```
    配置我的 API Key 是：sk-xxxxxxxxxxxxx
    ```
    
    **警告**API Key 为敏感凭证，请勿泄露。对话中粘贴明文 API Key 可能被会话记录留存，建议通过 `settings.json` 或环境变量配置。
    
3.  3
    
    开始使用
    
    ```
    帮我生成 6 张亚马逊电商主图，产品是白色无线蓝牙耳机。
    ```
    

## 了解更多

更多命令、子智能体、MCP、Skills 和示例，见 [Qwen Code 官方文档](https://qwenlm.github.io/qwen-code-docs/zh/users/overview/)和[官方示例](https://qwenlm.github.io/qwen-code-docs/zh/showcase/)。

## 错误码

配置过程中遇到报错，参考对应计费方案的常见问题文档：

-   Token Plan：[Token Plan 常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq#tpt-h-errors)
-   按量计费：[错误码](raw/model-api-reference/preparations/error-code.md)
-   Coding Plan：[Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq#e07ad90b4f3l0)

## 常见问题

如何按量计费接入节省计划与资源包？

按量计费接入方式不变，使用百炼通用 API Key 和 Base URL。购买节省计划或资源包后自动生效，调用费用按抵扣顺序自动抵扣。详情参见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h2-usage)。

配置完成后找不到想要的模型怎么办？

按以下顺序处理：

1.  升级 Qwen Code 到最新版本。
2.  仍找不到时，在 `~/.qwen/settings.json` 的 `modelProviders.openai` 中手动新增模型配置，然后重启 Qwen Code。配置方法见[通过配置文件接入](#qc-config-file-h)。

Windows 安装后无法识别 qwen 命令怎么办？

关闭并重新打开 `cmd` 使环境变量生效，再运行 `qwen --version` 确认安装。
