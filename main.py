from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import discord
from discord.ext import commands
import os

if not os.path.exists('scrims'):
    os.mkdir('scrims')


#VARIABLES
prefix = '-'
token = ''

bot = commands.Bot(command_prefix=prefix)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True, unique=True)
    elo = Column('elo', Integer)

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

@bot.event
async def on_ready():
    print('Bot has been connected to discord.')

@bot.event
async def on_message(message):
    if message.content.lower() == '{}elo'.format(prefix):
        user = session.query(User).filter_by(id=message.author.id).first()
        embed=discord.Embed(title="Elo", description="{}'s current elo is {}.".format(message.author.mention, user.elo), color=0xb0ad1c)
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.command()
async def scrim(ctx):
    embed=discord.Embed(title="A new scrimmage is starting", description="To join team one react with 👍\nTo join team two react with 👎", color=0xb0ad1c)
    message = await ctx.channel.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')
    open('scrims/{}.txt'.format(message.id), 'w+').close()
    

@bot.event
async def on_reaction_add(reaction, user):
    if user.id != 700485181869523054:
        if not reaction.message.channel.name == 'scrim':
            if reaction.emoji == '👍':
                file = open('scrims/{}.txt'.format(reaction.message.id), 'r')
                data = file.readlines()
                file.close()
                data = [i.replace('\n','') for i in data]
                data = [i.split('=') for i in data]
                for i in data:
                    if i[1] == str(user.id):
                        exists = True
                try:
                    exists
                except:
                    file = open('scrims/{}.txt'.format(reaction.message.id), 'a')
                    file.write('1={}\n'.format(user.id))
                    file.close()
                file = open('scrims/{}.txt'.format(reaction.message.id), 'r')
                data = file.readlines()
                file.close()
                data = [i.replace('\n','') for i in data]
                data = [i.split('=') for i in data]
                team_1_count = 0
                team_2_count = 0
                for i in data:
                    if i[0] == '1':
                        team_1_count += 1
                    elif i[0] == '2':
                        team_2_count += 1
                if team_1_count >= 5 and team_2_count >= 5:
                    await reaction.message.delete()
                    channel = await user.guild.create_text_channel('scrim')
                    await channel.set_permissions(discord.utils.get(user.guild.roles, name='@everyone'), read_messages=False, read_message_history=False)
                    team_two_role = await user.guild.create_role(name='Team 2')
                    team_one_role = await user.guild.create_role(name='Team 1')
                    await channel.set_permissions(team_one_role, read_messages=True, read_message_history=True, send_messages=True)
                    await channel.set_permissions(team_two_role, read_messages=True, read_message_history=True, send_messages=True)
                    team_one_channel = await user.guild.create_voice_channel('Team 1')
                    await team_one_channel.set_permissions(discord.utils.get(user.guild.roles, name='@everyone'), connect=False)
                    await team_one_channel.set_permissions(team_one_role, connect=True)

                    team_two_channel = await user.guild.create_voice_channel('Team 2')
                    await team_two_channel.set_permissions(discord.utils.get(user.guild.roles, name='@everyone'), connect=False)
                    await team_two_channel.set_permissions(team_two_role, connect=True)
                    file = open('scrims/{}.txt'.format(reaction.message.id), 'r')
                    data = file.readlines()
                    file.close()
                    data = [i.replace('\n','') for i in data]
                    data = [i.split('=') for i in data]
                    for i in data:
                        if i[0] == '1':
                            await discord.utils.get(user.guild.members, id=int(i[1])).add_roles(team_one_role)
                        elif i[0] == '2':
                            await discord.utils.get(user.guild.members, id=int(i[1])).add_roles(team_two_role)
                    embed=discord.Embed(title="Who won?", description="Once the scrimmage has been completed, please react with which team won.", color=0xb0ad1c)
                    message = await channel.send(embed=embed)
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')
                    file = open('scrims/{}-roles.txt'.format(message.id), 'w+')
                    file.write('{}\n{}\n{}\n{}'.format(team_one_role.id, team_two_role.id, team_one_channel.id, team_two_channel.id))
                    file.close()
                    os.remove('scrims/{}.txt'.format(reaction.message.id))
            elif reaction.emoji == '👎':
                file = open('scrims/{}.txt'.format(reaction.message.id), 'r')
                data = file.readlines()
                file.close()
                data = [i.replace('\n','') for i in data]
                data = [i.split('=') for i in data]
                for i in data:
                    if i[1] == str(user.id):
                        exists = True
                try:
                    exists
                except:
                    file = open('scrims/{}.txt'.format(reaction.message.id), 'a')
                    file.write('2={}\n'.format(user.id))
                    file.close()
                file = open('scrims/{}.txt'.format(reaction.message.id), 'r')
                data = file.readlines()
                file.close()
                data = [i.replace('\n','') for i in data]
                data = [i.split('=') for i in data]
                team_1_count = 0
                team_2_count = 0
                for i in data:
                    if i[0] == '1':
                        team_1_count += 1
                    elif i[0] == '2':
                        team_2_count += 1
                if team_1_count >= 5 and team_2_count >= 5:
                    await reaction.message.delete()
                    channel = await user.guild.create_text_channel('scrim')
                    await channel.set_permissions(discord.utils.get(user.guild.roles, name='@everyone'), read_messages=False, read_message_history=False)
                    team_two_role = await user.guild.create_role(name='Team 2')
                    team_one_role = await user.guild.create_role(name='Team 1')
                    await channel.set_permissions(team_one_role, read_messages=True, read_message_history=True, send_messages=True)
                    await channel.set_permissions(team_two_role, read_messages=True, read_message_history=True, send_messages=True)
                    team_one_channel = await user.guild.create_voice_channel('Team 1')
                    await team_one_channel.set_permissions(discord.utils.get(user.guild.roles, name='@everyone'), connect=False)
                    await team_one_channel.set_permissions(team_one_role, connect=True)

                    team_two_channel = await user.guild.create_voice_channel('Team 2')
                    await team_two_channel.set_permissions(discord.utils.get(user.guild.roles, name='@everyone'), connect=False)
                    await team_two_channel.set_permissions(team_two_role, connect=True)
                    file = open('scrims/{}.txt'.format(reaction.message.id), 'r')
                    data = file.readlines()
                    file.close()
                    data = [i.replace('\n','') for i in data]
                    data = [i.split('=') for i in data]
                    for i in data:
                        if i[0] == '1':
                            await discord.utils.get(user.guild.members, id=int(i[1])).add_roles(team_one_role)
                        elif i[0] == '2':
                            await discord.utils.get(user.guild.members, id=int(i[1])).add_roles(team_two_role)
                    embed=discord.Embed(title="Who won?", description="Once the scrimmage has been completed, please react with which team won.", color=0xb0ad1c)
                    message = await channel.send(embed=embed)
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')
                    file = open('scrims/{}-roles.txt'.format(message.id), 'w+')
                    file.write('{}\n{}\n{}\n{}'.format(team_one_role.id, team_two_role.id, team_one_channel.id, team_two_channel.id))
                    file.close()
                    os.remove('scrims/{}.txt'.format(reaction.message.id))
        else:
            if reaction.emoji == '👍':
                file = open('scrims/{}-roles.txt'.format(reaction.message.id), 'r')
                data = file.readlines()
                file.close()
                data = [i.replace('\n','') for i in data]
                team_one_role = discord.utils.get(user.guild.roles, id=int(data[0]))
                team_two_role = discord.utils.get(user.guild.roles, id=int(data[1]))
                team_one_channel = bot.get_channel(int(data[2]))
                team_two_channel = bot.get_channel(int(data[3]))
                for i in user.guild.members:
                    if team_one_role in i.roles:
                        try:
                            user_ = session.query(User).filter_by(id=i.id).first()
                            user__ = User(id=i.id, elo=user_.elo + 75)

                            session.delete(user_)
                            session.commit()

                            session.add(user__)
                            session.commit()
                        except:
                            user__ = User(id=i.id, elo=75)
                            session.add(user__)
                            session.commit()
                
                for i in user.guild.members:
                    if team_two_role in i.roles:
                        try:
                            user_ = session.query(User).filter_by(id=i.id).first()
                            if user_.elo > 50:
                                user__ = User(id=i.id, elo=user_.elo - 50)
                            else:
                                user__ = User(id=i.id, elo=0)

                            session.delete(user_)
                            session.commit()
                            session.add(user__)
                            session.commit()
                        except:
                            user__ = User(id=i.id, elo=0)
                            session.add(user__)
                            session.commit()

                await reaction.message.channel.delete()
                await team_one_role.delete()
                await team_two_role.delete()
                await team_one_channel.delete()
                await team_two_channel.delete()
                os.remove('scrims/{}-roles.txt'.format(reaction.message.id))
            elif reaction.emoji == '👎':
                file = open('scrims/{}-roles.txt'.format(reaction.message.id), 'r')
                data = file.readlines()
                file.close()
                data = [i.replace('\n','') for i in data]
                team_one_role = discord.utils.get(user.guild.roles, id=int(data[0]))
                team_two_role = discord.utils.get(user.guild.roles, id=int(data[1]))
                team_one_channel = bot.get_channel(int(data[2]))
                team_two_channel = bot.get_channel(int(data[3]))
                for i in user.guild.members:
                    if team_two_role in i.roles:
                        try:
                            user_ = session.query(User).filter_by(id=i.id).first()
                            user__ = User(id=i.id, elo=user_.elo + 75)

                            session.delete(user_)
                            session.commit()

                            session.add(user__)
                            session.commit()
                        except:
                            user__ = User(id=i.id, elo=75)
                            session.add(user__)
                            session.commit()
                
                for i in user.guild.members:
                    if team_one_role in i.roles:
                        try:
                            user_ = session.query(User).filter_by(id=i.id).first()
                            if user_.elo > 50:
                                user__ = User(id=i.id, elo=user_.elo - 50)
                            else:
                                user__ = User(id=i.id, elo=0)

                            session.delete(user_)
                            session.commit()

                            session.add(user__)
                            session.commit()
                        except:
                            user__ = User(id=i.id, elo=0)
                            session.add(user__)
                            session.commit()
                await reaction.message.channel.delete()
                await team_one_role.delete()
                await team_two_role.delete()
                await team_one_channel.delete()
                await team_two_channel.delete()
                os.remove('scrims/{}-roles.txt'.format(reaction.message.id))

@bot.command()
async def elo(ctx, member: discord.Member):
    try:
        user = session.query(User).filter_by(id=member.id).first()
        embed=discord.Embed(title="Elo", description="{}'s current elo is {}.".format(member.mention, user.elo), color=0xb0ad1c)
        await ctx.channel.send(embed=embed)
    except:
        embed=discord.Embed(title="Elo", description="{}'s current elo is {}.".format(member.mention, '0'), color=0xb0ad1c)
        await ctx.channel.send(embed=embed)

@bot.command()
async def startscrim(ctx, messageId: int):
    message = await ctx.message.channel.fetch_message(messageId)
    await message.delete()
    channel = await ctx.guild.create_text_channel('scrim')
    await channel.set_permissions(discord.utils.get(ctx.guild.roles, name='@everyone'), read_messages=False, read_message_history=False)
    team_two_role = await ctx.guild.create_role(name='Team 2')
    team_one_role = await ctx.guild.create_role(name='Team 1')
    await channel.set_permissions(team_one_role, read_messages=True, read_message_history=True, send_messages=True)
    await channel.set_permissions(team_two_role, read_messages=True, read_message_history=True, send_messages=True)
    team_one_channel = await ctx.guild.create_voice_channel('Team 1')
    await team_one_channel.set_permissions(discord.utils.get(ctx.guild.roles, name='@everyone'), connect=False)
    await team_one_channel.set_permissions(team_one_role, connect=True)

    team_two_channel = await ctx.guild.create_voice_channel('Team 2')
    await team_two_channel.set_permissions(discord.utils.get(ctx.guild.roles, name='@everyone'), connect=False)
    await team_two_channel.set_permissions(team_two_role, connect=True)
    file = open('scrims/{}.txt'.format(messageId), 'r')
    data = file.readlines()
    file.close()
    data = [i.replace('\n','') for i in data]
    data = [i.split('=') for i in data]
    for i in data:
        if i[0] == '1':
            await discord.utils.get(ctx.guild.members, id=int(i[1])).add_roles(team_one_role)
        elif i[0] == '2':
            await discord.utils.get(ctx.guild.members, id=int(i[1])).add_roles(team_two_role)
    embed=discord.Embed(title="Who won?", description="Once the scrimmage has been completed, please react with which team won.", color=0xb0ad1c)
    message = await channel.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')
    file = open('scrims/{}-roles.txt'.format(message.id), 'w+')
    file.write('{}\n{}\n{}\n{}'.format(team_one_role.id, team_two_role.id, team_one_channel.id, team_two_channel.id))
    file.close()
    os.remove('scrims/{}.txt'.format(messageId))


bot.run(token)

