# API 开发指南

本文介绍如何使用 AgentScope-AI 从零开始开发、上传和部署高代码应用的 API 服务。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6792415871/CAEQaxiBgMDoh.XA3RkiIGQ3ODMyNThlYzJiNDRmM2E4NzQxNTBmOTQzZGQxOGY46098517_20260106202118.816.svg)

## 环境准备

1.  Python 开发环境要求`python >= 3.10`。
2.  为了能够将 Python 代码上传并部署到阿里云百炼，安装 [AgentScope-AI](https://github.com/agentscope-ai) 的相关依赖，用于向阿里云百炼上传代码包：

```
pip install agentscope-runtime==1.0.0
pip install "agentscope-runtime[deployment]==1.0.0"
```

## 开发规范

1.  Python 后端程序必须提供`GET /health`接口。若该接口无法调用，百炼将判定程序启动失败。

```
@app.get("/health")
def health_check():
    return "OK"
```

2.  Python 后端程序的入口文件**必须**为`main.py`。
3.  对话接口路径，默认使用`/process`，协议可参考 [Agent API 协议规范](https://runtime.agentscope.io/zh/protocol.html?spm=a2ty02.30260277.d_app-center.1.a70474a1x8Ajdg)。
4.  开发参考代码包：[mcp\_server\_with\_chat.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260106/yqdvue/mcp_server_with_chat.zip)。

## 应用观测植入

通过使用 AgentScope-runtime 包提供的`@trace`装饰器，可以自动上报日志，统计耗时。

针对大模型调用函数的装饰器示例：

```
from agentscope_runtime.engine.tracing import trace, TraceType
@trace(trace_type=TraceType.LLM, trace_name="llm_func")
def llm_func():
  pass
```

示例输出：

```
{"time": "2025-08-13 11:23:41.808", "step": "llm_func_start", "model": "", "user_id": "", "code": "", "message": "", "task_id": "", "request_id": "", "context": {}, "interval": {"type": "llm_func_start", "cost": 0}, "ds_service_id": "test_id", "ds_service_name": "test_name"}
{"time": "2025-08-13 11:23:41.808", "step": "llm_func_end", "model": "", "user_id": "", "code": "", "message": "", "task_id": "", "request_id": "", "context": {}, "interval": {"type": "llm_func_end", "cost": "0.000"}, "ds_service_id": "test_id", "ds_service_name": "test_name"}
```

如需自定义日志上报、支持流式输出函数、设置日志公共属性等功能，请参考： [AgentScope-runtime 的 Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/blob/main/src/agentscope_runtime/engine/tracing/README.md)。

-   如果使用`AgentScope-AI`上传构建好的`.whl` 软件包，需要添加`--telemetry enable`来开启应用观测功能。

```
runtime-fc-deploy --deploy-name 我的第一个高代码应用  --whl-path <PATH_TO_YOUR_NEW_WHL_FILE> --telemetry enable
```

应用运行后，可在[阿里云百炼-应用观测](https://bailian.console.aliyun.com/?tab=app#/app-observe)页面查看收集到的相关信息。

应用观测页面顶部展示**调用次数**、**LLM Token总量**、**平均延时**、**平均首包时长**等统计概览，下方为调用记录表格，包含**节点类型**、**名称**、**输入**、**输出**、**调用时间**、**延时**、**Token量**、**状态**等列，可查看每次调用的详细信息及运行状态。

## 应用上传

1.  获取并配置以下环境变量（以 Linux 系统为例）
    
    1.  获取阿里云的 [AccessKey（AK 和 SK）](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)，用于上传软件包时的鉴权。
    2.  （**可选**）获取阿里云百炼的 [Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，以`llm-`开头，用于指定存储高代码应用的百炼业务空间，不设置将使用默认业务空间。
    3.  将以上获取到的内容配置为环境变量：

```
export ALIBABA_CLOUD_ACCESS_KEY_ID=LTAI************            #替换为阿里云AccessKey(AK)
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=****************        #替换为阿里云SecretKey(SK)
export MODELSTUDIO_WORKSPACE_ID=llm-****************           #可选，替换为百炼的业务空间ID，该空间将部署高代码应用，不设置将使用默认业务空间
```

2.  使用`AgentScope-AI`上传构建好的`.whl` 软件包，并自动部署到阿里云百炼。
    
    > `--telemetry enable`用于打开可观测能力，并需要结合 AgentScope 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-bricks/blob/main/src/agentscope_bricks/utils/tracing_utils/README.md)进行应用开发。
    

```
runtime-fc-deploy --deploy-name 我的第一个高代码应用  --whl-path <PATH_TO_YOUR_NEW_WHL_FILE> --telemetry enable
```

部署成功后会打印出 应用名、百炼业务空间、访问应用的控制台链接、应用 ID。

```
Built wheel at: /Users/<username>/Desktop/workspace/develop/.agentscope_runtime_builds/build-<build_id>/dist/agentdev_starter_36a13f34-0.1.17
Artifact URL: https://tmp-code-deploy-<workspace>.oss-cn-hangzhou.aliyuncs.com/agentdev_starter_36a13f34-0.1.1758618690-py3-none-any.whl?x-oss-expires=...
Resource Name: 我的第一个百炼高代码应用
Workspace: llm-<workspace_id>
Deploy Result
Console URL: https://bailian.console.aliyun.com/?tab=app#/app-center
Deploy ID: <deploy_id>
```

3.  前往[阿里云百炼-应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，等待应用发布。应用发布后将会根据部署时长，产生较少的费用。（<0.1元/小时）

## 应用测试

建议前往[阿里云百炼-应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，在应用详情页测试并查看构建、部署、调用日志。

## 应用更新

当高代码应用需要更新时，可以使用 AgentScope-AI 的更新命令重新上传`.whl` 软件包。软件包上传成功后，高代码应用将自动更新并重新部署运行。

1.  前往[阿里云百炼-应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，复制应用 ID。
    
2.  在本地使用以下命令，上传更新的本地`.whl` 软件包。
    
    > 应用更新后，应用将重新构建、部署。
    

```
runtime-fc-deploy --update <HIGH_CODE_APP_ID> --whl-path <PATH_TO_YOUR_NEW_WHL_FILE>
```

更新成功。

```
% runtime-fc-deploy --update d8a48e627a6d49338faef50fdfaf2ef9 --whl-path ./agentdev_starter_e61c4e2f-0.1.0-py3-none-any.whl
INFO:agentscope_runtime.engine.deployers.modelstudio_deployer:Uploading wheel to OSS and generating presigned URL
INFO:agentscope_runtime.engine.deployers.modelstudio_deployer:Triggering ModelStudio Full-Code deploy for None
Built wheel at: /Users/<username>/Desktop/test/agentdev_starter_e61c4e2f-0.1.0-py3-none-any.whl
Artifact URL: https://tmp-code-deploy-llm-enpaqbwxdsmnlfpq.oss-cn-hangzhou.aliyuncs.com/agentdev_starter_e61c4e2f-0.1.0-py3-none-any.whl?x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-date=20250922T085339Z&x-oss-expires=10799&x-oss-credential=YOUR_ACCESS_KEY_ID&x-oss-signature=YOUR_SIGNATURE
Deploy ID: 44ccb27c-2918-4a64-aa6a-8a0970d88ffb
Resource Name: None
Workspace: llm-enpaqbwxdsmnlfpq
Console Url: https://pre-bailian.console.aliyun.com/?tab=app#/app-center/high-code-detail/d8a48e627a6d49338faef50fdfaf2ef9
```

## 常见问题

### RAM 账号最小化授权

RAM 账号需要**最小化**赋权使用高代码应用时，可以基于以下规则创建高代码应用的[自定义权限策略](https://help.aliyun.com/zh/ram/create-a-custom-policy#section-kwn-gu8-48m)。

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sfm:ApplyTempStorageLease",
        "fc:ListTriggers",
        "fc:GetFunction",
        "fc:GetFunctionCode",
        "fc:UpdateFunction",
        "log:GetProject",
        "log:GetLogStore",
        "log:GetIndex"
      ],
      "Resource": "*"
    }
  ]
}
```

### 上传失败了如何排查？

1.  请检查阿里云的 AK/SK 与 阿里云百炼的 Workspace ID 是否属于同一个账号。
    
2.  请检查是否在百炼控制台上部署过一次高代码应用，在控制台部署过程中将引导您开通部署高代码所必要的阿里云权限、资源等。
    
3.  请尝试使用一个干净的`python >= 3.10`的环境，比如使用 `Python` 的 `venv` 命令创建一个干净的虚拟环境：
    
    1.  创建环境：

```
python --version
python -m venv venv
```

2.  加载环境

```
# Linux / macOS
source venv/bin/activate
# Windows (CMD)
venv\Scripts\activate.bat
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

4.  上传时代码运行报错 “**RAM user is not assigned to any workspace in Bailian**”，请联系阿里云[主账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)的拥有者进行以下操作：
    
    1.  由阿里云[主账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)为阿里云[子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)）在 [RAM 控制台](https://ram.console.aliyun.com/users) 添加 **AliyunBailianDataFullAccess** 权限。
    2.  为子账号（RAM用户）在[百炼账号管理页面](https://bailian.console.aliyun.com/?tab=globalset#/user_management/user_management)添加**特定业务空间**的**智能体-操作**权限。

### 控制台一直显示部署中（超过 5 分钟）或部署失败可能是什么原因？

1.  Python 后端程序的`GET /health` 接口无法调用，导致百炼认为程序启动失败。
2.  Python 后端程序的入口文件必须为`main.py`。
3.  可以前往高代码应用详情页中，查看具体的运行日志。

### 如何避免依赖包更新导致应用构建失败？

建议在 `requirements.txt` 中使用 `==` 固定依赖版本，避免使用 `>=` 等范围约束符。使用 `>=` 时，每次构建可能拉取到不同版本的依赖包，导致应用行为不一致甚至构建失败。

**示例：**
```
# 推荐：固定版本，确保每次构建结果一致
flask==3.0.3
dashscope==1.20.14

# 不推荐：范围约束，可能因依赖包更新导致构建失败
flask>=3.0.0
dashscope>=1.20.0
```

您可以在本地调试通过后，使用 `pip freeze` 命令导出当前环境的精确版本：

```
pip freeze > requirements.txt
```

### API 调用报错`Invalid API-key Provided`?

说明高代码应用的环境变量中未正确配置百炼的 API Key， 获取方式请参考：[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)。
