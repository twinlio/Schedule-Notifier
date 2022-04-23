import requests
import schedule
import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime
import ast
from keep_alive import keep_alive

api_link = "https://ash-hs-schedule-api.twinlio.repl.co/today/"


t_v = requests.get('https://ash-hs-schedule-api.twinlio.repl.co/todayvar/').text
today_var = datetime.strptime(t_v, '%Y-%m-%d %H:%M')


pe_schedule = ast.literal_eval(requests.get('https://ash-hs-schedule-api.twinlio.repl.co/peschedule/').text)

def readschedule():
    with open("today.txt", "r") as f:
        read = f.read()
        output_list = ast.literal_eval(read)
    return output_list



client = commands.Bot(command_prefix='-')





@client.command(aliases=['schedule', 's'])
async def schedulecommand(ctx):
    embed = discord.Embed(title=f"Schedule for {today_var}", description=" ", color=0x00ff00)
    schedule_list = readschedule()
    try:
      day = schedule_list[0][4]
      pe_day = pe_schedule[int(day)]
      embed.set_footer(text=f'PE Schedule: {pe_day}')
    except:
      ...
    if schedule_list == ['[]']:
        embed2 = discord.Embed(title=f"Schedule for {today_var}", description="----------------------------", color=0x00ff00)
        embed2.add_field(name="No events are schedule for today.", value="=)", inline=False)
        await ctx.send(embed=embed2)
        return
    for i in schedule_list:
        if i != ['end']:
            if type(i) == str:
                if i != '[]':
                    embed.add_field(name=i, value="----------------------------", inline=False)
                else:
                    embed = discord.Embed(title=f"Schedule for {today_var}", description="----------------------------", color=0x00ff00)
            else:
                i_0 = i[0]
                i_2 = i[2]
                i_3 = i[3]
                embed.add_field(name=i_0, value=f"{i_2} - {i_3}", inline=False)
    if today_var != datetime.today().date():
        await ctx.send("This is not todays schedule!")
    await ctx.send(embed=embed)


def getstatus():
    number = 0
    string = ""
    end = ""
    p_blocks = ["A", "B", "C", "D", "E", "F", "G", "H"]
    schedule = readschedule()
    for i in schedule:
        if i != ['end']:
            if i[1] in p_blocks:
                number += 1
                string = string + i[1]
            elif "Flex" in i[1]:
                number += 1
                end = " :: " + i[1]
    if number > 0:
        return string + end
    else:
        return "Nothing scheduled! =)"




@client.command()
async def setstatus(ctx, arg1=None, arg2=None, arg3=None):
    if arg1 == None and arg2 == None and arg3 == None:
        status = getstatus()
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
    else:
        if arg3 == None:
            name = f"{arg1} :: {arg2}"
        else:
            name = f"{arg1} :: {arg2} {arg3}"
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=name))      




client.remove_command("help")
@client.command(aliases=['h'])
async def help(ctx):
    embedVar = discord.Embed(title="List of Commands", description="   ", color=0x00ff00)
    embedVar.add_field(name="-s", value="See the schedule of the day or the next day.", inline=False)
    await ctx.send(embed=embedVar)




def update_list():
        global today_var
        today = requests.get(api_link).text
        t_v = requests.get('https://ash-hs-schedule-api.twinlio.repl.co/todayvar/').text
        today_var = datetime.strptime(t_v, '%Y-%m-%d %H:%M').date()
        with open("today.txt", "a") as f:
            f.truncate(0)
            f.write(today)
        status = getstatus()
        client.loop.create_task(client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=status)))

@client.event
async def on_ready():
    print(f'Connected to bot {client.user}')
    print('----------------------------------------')
    update_list()
    schedule.every(20).minutes.do(update_list)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)



@client.command()
async def pe(ctx):
    pe_schedule = {1:"Health Day", 2:"Sport Unit Day", 3:"Wellness Day", 4:"Sport Unit Day", 5:"Sport Unit Day", 6:"Wellness Day", 7:"Sport Unit Day", 8:"Health Day"}
    schedule = readschedule()
    if 'Day' in schedule and '/180' in schedule:
        day_info = schedule[0]
        
    else:
        await ctx.send('No information for this day was found.')


# Running the bot
keep_alive()
client.run(os.environ['BOTTOKEN'])
