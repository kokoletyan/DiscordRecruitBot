import discord
from discord.ext import commands
from discord.message import Message
from keep_alive import keep_alive
import os
import asyncio

intent = discord.Intents.default()
intent.message_content = True
client = commands.Bot(command_prefix='/', intents=intent)


@client.event
async def on_ready():
  print('ログインしました')


@client.command()
async def boshu(ctx, about="募集", cnt=3):
  hostuser = str(ctx.author.display_name + "@" + ctx.author.name)
  cnt = int(cnt)
  dispcnt = int(cnt)
  reaction_member = [">>>"]
  rect_message = discord.message.Embed(title=about,
                                       description=f"募集主：{hostuser}\n",
                                       colour=0x1e90ff)
  rect_message.add_field(name=f"あと{dispcnt}人 募集中\n", value=None, inline=True)
  msg = await ctx.send("@everyone")
  msg = await ctx.send(embed=rect_message)
  #投票の欄
  await msg.add_reaction('🖐')
  await msg.add_reaction('❌')
  await msg.add_reaction('🚫')

  def check(reaction, user):
    emoji = str(reaction.emoji)
    if user.bot == True:  # botは無視
      pass
    else:
      return emoji == '🖐' or emoji == '❌' or emoji == '🚫'

  while len(reaction_member) <= cnt:
    try:
      reaction, user = await client.wait_for('reaction_add',
                                             timeout=float(43200.0),
                                             check=check)
    except asyncio.TimeoutError:
      rect_message = discord.message.Embed(title=about,
                                           description=f"募集主：{hostuser}\n",
                                           colour=0x1e90ff)
      rect_message.add_field(name="募集を締め切りました",
                             value='\n'.join(reaction_member),
                             inline=True)
      await msg.edit(embed=rect_message)
      await msg.clear_reactions()
      break
    else:
      if str(reaction.emoji) == '🖐':
        add_member = user.display_name + "@" + user.name
        if add_member in reaction_member:
          pass
        else:
          reaction_member.append(add_member)
          dispcnt -= 1
          if dispcnt != 0:
            rect_message = discord.message.Embed(
                title=about, description=f"募集主：{hostuser}\n", colour=0x1e90ff)
            rect_message.add_field(name=f"あと__{dispcnt}__人 募集中\n",
                                   value='\n'.join(reaction_member),
                                   inline=True)
            await msg.edit(embed=rect_message)
          elif dispcnt == 0:
            rect_message = discord.message.Embed(
                title=about, description=f"募集主：{hostuser}\n", colour=0x1e90ff)
            rect_message.add_field(name="募集を締め切りました",
                                   value='\n'.join(reaction_member),
                                   inline=True)
            await msg.edit(embed=rect_message)
            await msg.clear_reactions()
            break

      elif str(reaction.emoji) == '❌':
        delete_member = user.display_name + "@" + user.name
        if delete_member in reaction_member:
          reaction_member.remove(delete_member)
          dispcnt += 1
          rect_message = discord.message.Embed(title=about,
                                               description=f"募集主：{hostuser}\n",
                                               colour=0x1e90ff)
          rect_message.add_field(name=f"あと__{dispcnt}__人 募集中\n",
                                 value='\n'.join(reaction_member),
                                 inline=True)
          await msg.edit(embed=rect_message)
        else:
          pass
      elif str(reaction.emoji) == '🚫':
        cancel_user = user.display_name + "@" + user.name
        if cancel_user == hostuser:
          rect_message = discord.message.Embed(title=about,
                                               description=f"募集主：{hostuser}\n",
                                               colour=0x1e90ff)
          rect_message.add_field(name="募集を締め切りました",
                                 value='\n'.join(reaction_member),
                                 inline=True)
          await msg.edit(embed=rect_message)
          await msg.clear_reactions()
          break
        else:
          pass
    # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
    await msg.remove_reaction(str(reaction.emoji), user)


@client.command()
async def boshuhelp(ctxh):
  embed = discord.message.Embed(title="使用方法",
                                description="",
                                color=discord.Colour.red())
  embed.description = "注意 : 募集文に\".\"や\"/\"を含めないでください\n" \
                      "募集：\n" + \
                      "/boshu メンバー募集12時から！ 5\n" \
                      "3人募集：\n" + \
                      "/boshu メンバー募集12時から！\n" + \
                      "※3人の場合は募集文の後ろの数字はなくても問題ありません\n" + \
                      "募集に参加する：🖐\n" + \
                      "参加をやめる：❌\n" + \
                      "募集を中止する：🚫（募集主のみ中止できます。また、12時間経つと自動で中止されます。）"
  await ctxh.send(embed=embed)


keep_alive()
#TOKEN = os.environ['RECRUIT_TOKEN']
try:
  client.run("MTEyODIxNTQ5NjE4MTk0ODQ0Ng.G5FQn6.uGZAuKMkX859k97aR42Mxdo0YfIAU4yBRP02c0")
except:
  os.system("kill 1")
