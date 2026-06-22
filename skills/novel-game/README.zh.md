# novel-game

> [English →](README.md)

将小说/故事改编为浏览器端的 H5 互动小说游戏（React SPA）——
含 AI 生成视频/图片素材、可选 TTS 旁白、程序化音频和分支剧情引擎。

## 功能

- **分支剧情引擎** — 多结局、flags 系统、档案收集
- **AI 素材生成** — 角色立绘和过场 CG，支持视频 (`bl video generate` / `bl video ref`) 或图片 (`bl image generate`)，可混合使用
- **可选 TTS 旁白** — 通过 `bl speech synthesize` 生成场景旁白和角色独白
- **程序化音频** — BGM 和音效完全用 Web Audio API 生成，零外部依赖
- **存档系统** — 自动存档 + 3 个手动存档槽位（localStorage）
- **移动端适配** — 竖屏优先、触控优化、安全区适配
- **多种 UI 风格** — 像素风 / 赛博朋克 / 水墨中国风 / 简约现代

## 依赖

- [阿里云百炼 CLI (`bl`)](https://bailian.aliyun.com/cli/install.md) — AI 素材生成（视频/图片/语音）
- Node.js + npx — React 项目初始化

## 使用

在 Claude Code（或其他支持 skill 的 agent）中输入：

```
/novel-game 把《三体》地球往事改编为互动小说，水墨风格，30分钟时长
```

Skill 将会：
1. 询问关键设计决策（游戏类型、UI 风格、时长、素材模式）
2. 设计分支剧情结构
3. 初始化 React 项目并实现所有组件
4. 通过 `bl` CLI 生成 AI 素材（视频/图片/语音）
5. 启动 dev server 在浏览器中测试

## 生成的项目结构

```
src/
├── components/       # UI 组件（TypeWriter、GameScene、ChoicePanel、SaveLoadPanel...）
├── data/             # 场景图、角色、档案、素材索引
├── hooks/            # useGameState（reducer + hash 路由 + 存档）、useAudio（Web Audio）
└── styles/           # 主题 CSS（赛博朋克、像素风、水墨、简约...）
scripts/
└── generate-assets.sh  # bl CLI 素材生成脚本（支持并行生成）
public/assets/          # 下载到本地的 AI 生成素材文件
```

## 工作原理

- **场景数据** (`story.js`) 定义场景图——每个场景含文本段落、带 flag 变更的分支选择、可选的过场/档案触发
- **游戏状态** 通过 `useReducer` 管理，hash 路由实现场景导航
- **角色立绘** 支持视频（5秒循环 720P）或图片（带呼吸动效），组件自动适配
- **过场** 支持视频（全屏播放）或图片（Ken Burns 缓动效果），自动适配
- **存档** 自动存档 + 3 个手动槽位，存入 localStorage
- **BGM** 使用固定 MIDI 音高数组 + 多声部叠加 + 卷积混响 + ADSR 包络
- **音效** 包括噪声脉冲打字音、扫频档案解锁音、琶音场景切换音
- **TTS 旁白**（可选）预生成的 MP3 文件在场景播放时自动播放
