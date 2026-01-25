# demo-reaction-bot

使用这个项目测试Telegram机器人的Reaction功能。

在 python-telegram-bot ≥ v20.0 中，Telegram 把“消息表情反应”抽象成了 ReactionType，其中：`telegram.ReactionTypeEmoji`表示 普通 emoji 反应，比如 👍 👎 ❤️ 😂 等。

监听`MessageReactionUpdated`，通过`update.message_reaction`来获取信息。

```python
reaction_update = update.message_reaction

reaction_update.chat           # 群组
reaction_update.message_id     # 被反应的消息 ID
reaction_update.user           # 点反应的人
reaction_update.new_reaction   # 新增的反应列表
reaction_update.old_reaction   # 原来的反应列表
```
