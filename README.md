# Dialyn ZZZ Pet

《绝区零》Dialyn（琉音）的 Q 版 ChatGPT Work / Codex Pet 项目。角色保留黑白双辫、金瞳、紫色电话、青绿色饰绳与金色环刃，并针对小尺寸桌面宠物显示进行了简化。

![动作预览](assets/previews/all-states.gif)

## 当前状态

- v2 spritesheet：1536 × 2288 px
- 单格：192 × 208 px
- 73 个动作帧
- 9 个标准状态
- 16 个观察方向
- ChatGPT Pets 上传前校验：通过

最终可上传文件：`assets/final/dialyn-spritesheet-v2.png`

## 目录

- `assets/final/`：最终 spritesheet
- `assets/source/rows/`：最后采用的动作与方向源图
- `assets/previews/`：GIF、MP4、接触表和方向检查图
- `assets/reference/`：角色参考与统一造型基准
- `qa/`：结构、动作、透明边缘和方向连续性报告
- `docs/`：后续修改记录与制作说明
- `HANDOFF.md`：交给下一位 Codex 的当前状态与后续步骤

## 后续调整

每次修改建议创建一个新分支，例如：

```bash
git switch -c tweak/phone-pose
```

修改后保留旧版本，在 `assets/final/` 中导出新的 v2 spritesheet，并重新生成预览与 QA 报告。具体可改项目见 [`docs/adjustment-notes.md`](docs/adjustment-notes.md)。

## 版权说明

本仓库是非商业同人项目。《绝区零》及 Dialyn（琉音）角色相关权利归其各自权利人所有。仓库中的原创编排、制作记录与验证数据不授予对原角色素材的再许可权。
