# Environment

运行环境定义工具调用的执行沙箱与预装依赖。环境独立于智能体管理，可被多个会话复用。

## 生命周期

-   更新接口采用**全量替换**语义，缺省字段视为清空；已绑定该环境的运行中会话使用绑定时的快照，不受更新影响。
    
-   归档为软操作，`archived_at` 被填入归档时间；归档后默认不出现在列表中，仍可被查询，已绑定会话继续可用。
    
-   删除为硬操作，环境配置一并清除，不可恢复。
    

## 环境操作

**操作**

**端点**

**说明**

[创建 Environment](https://help.aliyun.com/zh/model-studio/environment-create)

`POST /environments`

创建运行环境，指定沙箱类型与预装依赖

[获取 Environment](https://help.aliyun.com/zh/model-studio/environment-get)

`GET /environments/{environment_id}`

获取环境详情

[列出 Environment](https://help.aliyun.com/zh/model-studio/environment-list)

`GET /environments`

分页列出工作空间下的环境，默认不含已归档

[更新 Environment](https://help.aliyun.com/zh/model-studio/environment-update)

`POST /environments/{environment_id}`

全量替换更新；运行中会话使用绑定快照，不受影响

[归档 Environment](https://help.aliyun.com/zh/model-studio/environment-archive)

`POST /environments/{environment_id}/archive`

软归档；默认不再出现在列表中，已绑定会话仍可用

[删除 Environment](https://help.aliyun.com/zh/model-studio/environment-delete)

`DELETE /environments/{environment_id}`

硬删除；配置一并清除，不可恢复
