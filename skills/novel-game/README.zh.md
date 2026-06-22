# novel-game

> [English version →](README.md)

将小说/故事改编为浏览器端的 H5 互动小说游戏（React SPA）——
含 AI 生成的动态角色立绘、过场动画、程序化音频和分支剧情引擎。

## 功能

- **分支剧情引擎** — 多结局、flags 系统、档案收集
- **AI 素材生成** — 通过 `bl video generate` / `bl video ref` 生成角色立绘和过场动画
- **LLM 辅助创作** — 通过 `bl text chat` 辅助剧情提取、场景文本生成、视频 prompt 编写
- **程序化音频** — Web Audio API 生成 BGM 和音效，零外部依赖
- **多种 UI 风格** — 像素风 / 赛博朋克 / 水墨中国风 / 简约现代

## 依赖

- [阿里云百炼 CLI (`bl`)](https://bailian.aliyun.com/cli/install.md) — AI 素材生成和 LLM 调用
- Node.js + npx — React 项目初始化

## 使用

在 Claude Code（或其他支持 skill 的 agent）中输入：

```
/novel-game 把《三体》改编为互动小说游戏，赛博朋克风格，30分钟时长
```

skill 会自动：
1. 确认关键设计决策（游戏类型、UI 风格、时长、AI 素材）
2. 设计分支剧情结构
3. 搭建 React 项目及全部组件
4. 通过 `bl` CLI 生成 AI 视频素材（立绘 + 过场动画）
5. 启动 dev server 在浏览器中测试

## 生成的项目结构

```
src/
├── components/       # UI 组件（TypeWriter、GameScene、ChoicePanel 等）
├── data/             # 场景图、角色数据、档案数据
├── hooks/            # useGameState（reducer + hash 路由）、useAudio（Web Audio）
└── styles/           # 主题样式（赛博朋克、像素风、水墨风等）
scripts/
└── generate-assets.sh  # bl CLI 素材生成脚本
public/assets/          # 下载到本地的 AI 生成视频文件
```

## 工作原理

- **场景数据**（`story.js`）定义场景图——每个场景包含文本段落、带 flag 变更的选择项、可选的过场动画/档案触发
- **游戏状态** 通过 `useReducer` 管理，结合 hash 路由实现场景导航
- **角色立绘** 为 5 秒循环视频（720P），在侧边栏展示；视频不可用时回退为文字首字占位
- **过场动画** 为 5 秒 1080P 视频，在关键剧情节点以全屏覆盖层播放
- **BGM** 使用固定 MIDI 音高数组，多声部叠加、卷积混响、ADSR 包络
- **音效** 包含噪声脉冲打字音、扫频+和弦档案解锁音、琶音场景转场音
