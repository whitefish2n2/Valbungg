import asyncio
import json
import random
import threading
import time
from code import interact
from contextlib import nullcontext
from idlelib.autoexpand import AutoExpand
from os.path import curdir
from queue import Queue
from typing import Optional
from weakref import KeyedRef
from collections import deque

import discord
import re as regex
import requests
from aiohttp.web_response import Response
from discord import Interaction
from discord.ext import commands
from discord import app_commands
from discord import Member
from discord.ext.commands import param
from lxml.doctestcompare import strip
from pycomcigan import *
from pycomcigan.timetable import TimeTableData
from urllib3 import request

import DISCORD_token
from DISCORD_token import Token, guild_id, channel3_id, niceApiKey
from dpyConsole import Console
from datetime import datetime, timedelta, tzinfo
import codecs
import psycopg2
from enum import Enum
from typing import Optional

#크롤링
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#유튜브 다운로드 및 mp3 변환,실행
from discord import FFmpegPCMAudio
import yt_dlp
from discord import FFmpegAudio
from discord import FFmpegOpusAudio

#pycomsigan(컴시간)
import pycomcigan


MY_GUILD = discord.Object(guild_id)
#랜덤 색상 리스트
colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080,
          0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
black_list = {1,}
hasaeng = DISCORD_token.hasaeng

class Client(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
intents.message_content = True
client = Client(intents=intents)
my_console = Console(client)
key = niceApiKey
db = psycopg2.connect("host=localhost dbname=valbungg user=node password=1234 port=5432")
cur = db.cursor()


#클라이언트 onready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("나도 이거"))
    print('클라이언트 로그인 완료')
    print('------------------------------------------------------')

@client.event
async def on_guild_join(guild):
    print('Bot has been added to a new server')
    print(f'List of servers the bot is in: {guild.name}')
    client.tree.copy_global_to(guild=discord.Object(guild.id))
    await client.tree.fetch_commands(guild=discord.Object(guild.id))
    await client.tree.sync(guild=discord.Object(guild.id))
keyword_list = {"업데이트","안녕",}
@client.event
async def on_message(ctx):
    if ctx.author.id == 1345676526154158131 and ctx.content.__len__() == 2:
        r = requests.get(f'https://maple.gg/u/{ctx.content}')
        if r.status_code != 200:
            r = requests.get(f'https://maple.gg/u/{ctx.content}')
            await asyncio.sleep(0.2)
            if r.status_code != 200:
                await ctx.channel.send(f"그것은 존재하지 않는 녜힁입니다!!>>@!>!>!@!@지금 즉시 생성 절차를 밟으세요")
                return
            else:
                await ctx.channel.send(f'이미 있는 녜힁이에요.\nhttps://maple.gg/u/{ctx.content}')
                return
        await ctx.channel.send(f'이미 있는 녜힁이에요.\nhttps://maple.gg/u/{ctx.content}')
        return
    if (not (str(ctx.content).__contains__("발붕아"))) or ctx.author.id == client.user.id:
        return
    if ctx.content == '발붕아':
        rand = random.randint(1, 3)
        if (rand == 1):
            await ctx.channel.send('왜 불러')
        elif (rand == 2):
            await ctx.channel.send('뭐')
        elif (rand == 3):
            await ctx.channel.send('발붕이 여기 있음')
    elif ctx.content == '발붕아 업데이트':
        try:
            if ctx.author.guild_permissions.administrator == True or ctx.author.id == hasaeng:
                await ctx.channel.send("명령어 업데이트를 시도합니다..")
                client.tree.copy_global_to(guild=discord.Object(ctx.guild.id))
                await client.tree.fetch_commands(guild=discord.Object(ctx.guild.id))
                await client.tree.sync(guild=discord.Object(ctx.guild.id))
                await ctx.channel.send("명령어 업데이트 완료")
            else:
                await ctx.channel.send("권한 없는 것이 어딜")
        except Exception as e:
            await ctx.channel.send("전아무것도몰루겟수요ㅜㅜ")
            print(e)
    elif str(ctx.content).startswith('발붕아 '):
        if black_list.__contains__(ctx.author.id) or keyword_list.__contains__(str(ctx.content).replace('발붕아 ', '')):
            return
        cur.execute("SELECT * FROM edu WHERE input = %s", ((str(ctx.content).replace('발붕아 ', '')),))
        r = cur.fetchall()
        if r.__len__() != 0:
            rand = random.randint(0, r.__len__() - 1)
            await ctx.channel.send(
                f"{r[rand][1]}\n-# {'<@' + str(r[rand][2]) + '>' if ctx.channel.guild.get_member(r[rand][2]) else r[rand][3]} 교수님이 심혈을 기울여 가르치셨습니다.",
                allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.channel.send('그런 말 배운 적 없다')

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='등록', description='발붕이 서버에 riot id를 등록합니다.')
@app_commands.rename(riot_id='riot_id')
@app_commands.describe(riot_id='라이엇 아이디')
async def command(interaction: discord.Interaction, riot_id: str):
    await interaction.response.send_message(riot_id)

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='급식', description='급식표 내놔 ("오늘","내일",YYMMDD)로 입력 가능')
@app_commands.rename(day='yymmdd')
@app_commands.describe(day='날짜(YYMMDD)')
async def command(interaction: discord.Interaction, day: str):
    if(black_list.__contains__(interaction.user.id)):
        await interaction.response.send_message("나 너 싫어")
        return
    if (day == 'YYMMDD'):
        await interaction.response.send_message("님아; YYMMDD라 했다고 진짜 YYMMDD를 넣으시면 어떡해요;")
    try:
        result = checkSchool(interaction)
        if result[UserInfo.school_id.value] == "키보토스":
            re = random.randint(0, 1000)
            card1 = "파란 종이" if re < 785 else "노란 종이" if re < 970 else "분홍 종이" if re < 993 else "픽업 획득할 확률을 요딴데에 쓰셨군요!"
            re = random.randint(0, 1000)
            card2 = "파란 종이" if re < 785 else "노란 종이" if re < 970 else "분홍 종이" if re < 993 else "픽업 획득할 확률을 요딴데에 쓰셨군요!"
            re = random.randint(0, 1000)
            card3 = "파란 종이" if re < 785 else "노란 종이" if re < 970 else "분홍 종이" if re < 993 else "픽업 획득할 확률을 요딴데에 쓰셨군요!"
            embed = discord.Embed(title=f"{result[1]} {day} 급식",
                                  description=f"## 조식\n{card1}\n## 중식\n{card2}\n## 석식\n{card3}",
                                  color=random.choice(colors))
            await interaction.response.send_message(embed=embed)
            return
        if (result is None):
            Exception("wrong result")
        response = GetMeal(day, result[UserInfo.school_code.value], result[UserInfo.education_center_code.value])
        print(response)
        if response == {"RESULT": {"CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다."}}:
            embed = discord.Embed(title=f"{result[UserInfo.school_id.value]} {day} 급식", description=f"당일 급식이 없습니다.")
            await interaction.response.send_message(embed=embed)
        else:
            string = ''
            kal = 0
            for i in range(response["mealServiceDietInfo"][0]["head"][0]["list_total_count"]):
                thisKal = float(response["mealServiceDietInfo"][1]["row"][i]["CAL_INFO"].replace(" Kcal", ""))
                kal += thisKal
                string += (f'## {response["mealServiceDietInfo"][1]["row"][i]["MMEAL_SC_NM"]}\n'
                           f'{response["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"]}\n'
                           f'### **칼로리: *{thisKal} Kcal***\n')
                string = string.replace("<br/>", "\n")
                string = regex.sub(r'\((\d+\.?)+\)', '', string)
            string += f"### 당일 총 칼로리 : *{kal.__round__(1)} Kcal*\n"
            embed = discord.Embed(title=f"{result[UserInfo.school_id.value]} {day} 급식",
                                  description=string,
                                  color=random.choice(colors))
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message("오류가 발생했습니다. 학교 등록을 완료했는지 확인해주세요.")


def GetMeal(day: str, school_code: str, edu_center_code: str) -> list:
    if day == '오늘':
        day = datetime.today().strftime("%Y%m%d")
    elif day == '내일':
        day = (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")
    response = requests.get(f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}"
                            f"Index=1&pSize=10&ATPT_OFCDC_SC_CODE={edu_center_code}&SD_SCHUL_CODE={school_code}&MLSV_YMD={day}&Type=json")
    if response.status_code == 200:
        list = json.loads(response.text)
        return list
    else:
        return Exception


@client.tree.command(name='n글자닉네임', description='랜덤 n글자 닉네임을 짓습니다.')
async def command(interaction: discord.Interaction, n: int):
    if (n < 1 or n > 9):
        await interaction.response.send_message('끔찍한 닉네임을 원하시는군요. 나가~')
        return
    response = requests.get(f"http://localhost:8080/shake?Length={n}")
    r = requests.get(f'https://maple.gg/u/{response.text}')
    if r.status_code != 200:
        await asyncio.sleep(0.2)
        r = requests.get(f'https://maple.gg/u/{response.text}')
        if r.status_code != 200:
            await interaction.response.send_message(f"{response.text}, 그것은 존재하지 않는 녜힁입니다!!>>@!>!>!@!@지금 즉시 생성 절차를 밟으세요")
        return
    await interaction.response.send_message(f'이미 있는 녜힁이에요.\nhttps://maple.gg/u/{response.text}')
    return
@client.tree.command(name='블랙리스트', description='맘에 안드는 저 새끼를 영원히 발붕이에게 접근하지 못하게 하기')
async def command(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id == hasaeng:
        black_list.add(user.id)
        try:
            cur.execute("DELETE FROM edu WHERE user_id = %s;", (user.id,))
            db.commit()
            await interaction.response.send_message(f"{user.display_name}을 발붕이에 접근 못 하게 해요")
        except Exception as e:
            print(e + "망!!@#!@#!@#!@#!@#")
            await interaction.response.send_message(f"봐준다")
    else:
        await interaction.response.send_message("ㄲㅈ")

@client.tree.command(name='방학까지', description='방학까지 남은 일수를 알려줍니다.')
async def command(interaction: discord.Interaction):
    today = datetime.today()
    dif = get_diff_time(today, datetime(today.year, 12, 20, 11, 30, 0))
    if dif.days < 0:
        await interaction.response.send_message("우효~")
        return
    elif dif.days == 0 and int(int(dif.seconds) / 3600) == 0 and int(int(dif.seconds % 3600) / 60) == 0:
        print(f"{int(int(dif.seconds) / 3600)} {int(int(dif.seconds % 3600) / 60)}")
        await interaction.response.send_message(
            f'```방학은 12 월 20 일 이고, 방학까지 {int((dif.seconds % 3600) % 60)}초 남았다!```')
    elif dif.days == 0 and int(dif.seconds) / 3600 == 0:
        await interaction.response.send_message(
            f'```방학은 12 월 20 일 이고, 방학까지 {int((dif.seconds % 3600) / 60)}분 {(int)((dif.seconds % 3600) % 60)}초 남았다!```')
    elif dif.days == 0:
        await interaction.response.send_message(
            f'```방학은 12 월 20 일 이고, 방학까지 {int(dif.seconds / 3600)}시간 {int((dif.seconds % 3600) / 60)}분 {int((dif.seconds % 3600) % 60)}초 남았다!```')
    else:
        await interaction.response.send_message(
            f'```방학은 12 월 20 일 이고, 방학까지 {dif.days}일 {int(dif.seconds / 3600)}시간 {int((dif.seconds % 3600) / 60)}분 {int((dif.seconds % 3600) % 60)}초 남았다!```')

class days(Enum):
    월요일=1
    화요일=2
    수요일=3
    목요일=4
    금요일=5
class week(Enum):
    이번주=0
    다음주=1
def getCurrentDay():
    print(datetime.today())
    return days(datetime.today().weekday()+1)

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='시간표', description='지정일의 시간표를 알려줍니다.')
async def command(interaction: discord.Interaction, 요일: days = None, 주: week = week.이번주 ):
    try:
        if 요일 == None:
            요일=getCurrentDay()
        info = checkSchool(interaction)
        if info[UserInfo.school_id.value] == "키보토스":
            embed = discord.Embed(title=f"{info[UserInfo.school_id.value]} {요일.name} 시간표",
                                  description="**1교시**\n총력전\n**2교시**\n총력전\n**3교시**\n총력전\n**4교시**\n총력전\n",
                                  color=random.choice(colors))
            await interaction.response.send_message(embed=embed)
            return
        timetable:TimeTable = TimeTable(info[UserInfo.school_id.value], week_num= 주.value)
        t:timetable= timetable.timetable[info[UserInfo.grade.value]][info[UserInfo.class_number.value]][요일.value]
        for e in timetable.timetable[info[UserInfo.grade.value]][info[UserInfo.class_number.value]]:
            print(e)

        print(t)
        new_table = []
        for v in t:
            ve:TimeTableData = v
            if not ve.subject:continue
            if ve.original:
                valString = f'{ve.subject} ({ve.teacher})' + (f'\n-# (<=> {ve.original.subject} 와(과) 변경)')
            else:
                valString = f'{ve.subject} ({ve.teacher})'
            valString = valString.replace('*', '○')
            new_table.append(valString)
        result = ""
        i = 0
        for v in new_table:
            i+=1
            if v == "()": return
            result += '**' + str(i) + '교시\n**' + v + '\n'
        embed = discord.Embed(title=f"{info[UserInfo.school_id.value]} {info[UserInfo.grade.value]}학년 {info[UserInfo.class_number.value]}반 {'다음주' if 주.value == 1 else ''} {요일.name} 시간표",
                              description=result,
                              color=random.choice(colors))
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)

    """
    if (black_list.__contains__(interaction.user.id)):
        await interaction.response.send_message("나 너 싫어")
        return
    try:
        string = ''
        if day == '오늘':
            day = datetime.today().strftime("%Y%m%d")
        elif day == '내일':
            day = (datetime.today() + timedelta(days=1)).strftime("%Y%m%d")
        info = checkSchool(interaction)
        if (info[UserInfo.school_id.value] == "키보토스"):
            embed = discord.Embed(title=f"{info[UserInfo.school_id.value]} {day} 시간표",
                                  description="**1교시**\n총력전\n**2교시**\n총력전\n**3교시**\n총력전\n**4교시**\n총력전\n",
                                  color=random.choice(colors))
            await interaction.response.send_message(embed=embed)
            return
        print(info[5])
        print(day)
        r = requests.get(
            f"https://open.neis.go.kr/hub/hisTimetable?KEY={key}"
            f"&TYPE=json"
            f"&ATPT_OFCDC_SC_CODE={info[UserInfo.education_center_code.value]}"
            f"&SD_SCHUL_CODE={info[UserInfo.school_code.value]}"
            f"&ALL_TI_YMD={day}"
            f"&GRADE={info[UserInfo.grade.value]}"
            f"&CLASS_NM={info[UserInfo.class_number.value]}")
        print(f"https://open.neis.go.kr/hub/hisTimetable?KEY={key}"
              f"&TYPE=json"
              f"&ATPT_OFCDC_SC_CODE={info[UserInfo.education_center_code.value]}"
              f"&SD_SCHUL_CODE={info[UserInfo.school_code.value]}"
              f"&ALL_TI_YMD={day}"
              f"&GRADE={info[UserInfo.grade.value]}"
              f"&CLASS_NM={info[UserInfo.class_number.value]}")
        res = json.loads(r.text)
        print(r.status_code)
        if res == {'RESULT': {'CODE': 'INFO-200', 'MESSAGE': '해당하는 데이터가 없습니다.'}}:
            await interaction.response.send_message("데이터가 없습니다. 당교에서 시간표를 입력하지 않았거나, 학년 또는 반이 잘못되었을 수도 있습니다.")
        print(res)
        timetable = res['hisTimetable'][1]['row']
        print(timetable)
        temp_perio = -1
        for input in timetable:
            if (temp_perio == input['PERIO']):
                continue;
            print(input)
            if str(input['CLASS_NM']) != str(info[UserInfo.class_number.value]):
                break
            string += '**' + input['PERIO'] + '교시\n**' + input['ITRT_CNTNT'] + '\n'
            print(input['PERIO'])
            temp_perio = input['PERIO']
        print(string)
        embed = discord.Embed(title=f"{info[UserInfo.school_id.value]} {info[UserInfo.grade.value]}"
                                    f"-{info[UserInfo.class_number.value]} {day} 시간표",
                              description=string,
                              color=random.choice(colors))
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message("시간표 불러오기에 실패하였습니다. 학년 반이 제대로 등록되어있는지 확인하여주세요.")
"""
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name="학교탈출까지", description="학교 탈출까지 남은 시간을 알려줍니다.")
async def command(interaction: discord.Interaction):
    today = datetime.today()
    if today.hour > 20 & today.minute > 30:
        await interaction.response.send_message("탈출했다!!!")
    dif = get_diff_time(today, datetime(today.year, today.month, today.day, 20, 30, 0))
    await interaction.response.send_message(
        f"```학교 탈출까지 {(int)(dif.seconds / 3600)}시간 {(int)((dif.seconds % 3600) / 60)}분 {(int)((dif.seconds % 3600) % 60)}초 남았다! ```")


def get_diff_time(anchor: datetime, target: datetime) -> timedelta:
    return (target - anchor)


#인사
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='안녕', description='발붕이와 인사하기~')
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message("뭐요")


class education_center(Enum):
    전체 = "null",
    서울특별시 = "1",
    부산광역시 = "2",
    대전광역시 = '3',
    대구광역시 = '4',
    인천광역시 = '5',
    광주광역시 = '6',
    울산광역시 = '7',
    세종특별자치시 = '8',
    경기도 = '9',
    강원특별자치도 = '10',
    충청북도 = '11',
    충청남도 = '12'
    전북특별자치도 = '13',
    전라남도 = '14',
    제주특별자치도 = '15'


# 학교 등록
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='학교등록', description='자신의 학교에 대한 정보를 등록합니다.(급식 서비스, 학사일정 서비스에 사용됩니다.)')
async def command_connect_school(interaction: discord.Interaction, 교명: str, grade: int,
                                 class_number: int, 지역: education_center = education_center.전체):
    if (교명.__len__() > 1 and 교명[교명.__len__() - 1] == 교명[교명.__len__() - 2]):
        교명 = list(교명)
        교명[교명.__len__() - 1] = ''
        교명 = ''.join(교명)
    try:
        ex = school_connect(지역.name if 지역.name != education_center.전체.name else '', interaction.user.id, 교명, grade,
                            class_number)
        if ex is not None: raise ex
        await interaction.response.send_message("학교 등록에 성공하였습니다. /학교정보확인 으로 학교 정보를 확인할 수 있습니다.")
    except Exception as e:
        await interaction.response.send_message("학교 등록에 실패하였습니다. 교명 또는 소속 교육청을 제대로 입력하였는지 확인해주세요.")


def school_connect(region: str, user_id: int, school_name: str, grade: int, class_number: int):
    if (school_name == "키보토스"):
        cur.execute(
            "UPDATE userinfo SET school_id = %s, grade = %d, class = %d, school_code  = %s, education_center_code = %s WHERE user_id = %s; ",
            (school_name, grade, class_number, '696969', 'kibo54', user_id,))
        db.commit()
        return
    try:
        response = json.loads(requests.get(f"https://open.neis.go.kr/hub/schoolInfo?KEY={key}&Type=json&SCHUL_NM="
                                           f"{school_name}&LCTN_SC_NM={region}").text)
        print(school_name, region)
        if 'Result' in response: return Exception()
        try:
            print(response)
            school_code = response['schoolInfo'][1]['row'][0]['SD_SCHUL_CODE']
            school_name = response['schoolInfo'][1]['row'][0]['SCHUL_NM']
            edu_center_code = response['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_CODE']
        except Exception as e:
            return e
        print(response)
        cur.execute(
            "INSERT INTO userinfo (user_id,school_id,grade,class,school_code,education_center_code) VALUES (%s,%s,%s,%s,%s,%s);",
            (user_id, school_name, grade, class_number, school_code, edu_center_code))
    except Exception as e:
        db.rollback()
        response = json.loads(requests.get(f"https://open.neis.go.kr/hub/schoolInfo?KEY={key}&Type=json&SCHUL_NM="
                                           f"{school_name}&LCTN_SC_NM={region}&").text)
        try:
            school_code = response['schoolInfo'][1]['row'][0]['SD_SCHUL_CODE']
            school_name = response['schoolInfo'][1]['row'][0]['SCHUL_NM']
            edu_center_code = response['schoolInfo'][1]['row'][0]['ATPT_OFCDC_SC_CODE']
        except Exception as e:
            print(e)
            db.rollback()
            return e
        try:
            cur.execute(
                "UPDATE userinfo SET school_id = %s, grade = %s, class = %s, school_code  = %s, education_center_code = %s WHERE user_id = %s; ",
                (school_name, grade, class_number, school_code, edu_center_code, user_id,))
            print('updated')
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            return e
    db.commit()
    cur.execute("SELECT * FROM userinfo")
    results = cur.fetchall()
    print(results)


"""
class YoutubePlayer(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current_player = None
        self.max_queue_size = 100
    async def play_next(self, ctx):
        if len(self.queue) > 0:
            await self.skip(ctx)
    @commands.command(aliases=["다음"])
    async def skip(self, ctx):
        if not ctx.voice_client:
            await ctx.send("봇이 음성 채널에 연결되어 있지 않습니다.")
            return

        if not self.queue:
            await ctx.send("다음 재생할 곡이 대기열에 없습니다.\n음악을 계속 재생하시려면 음악을 추가해주세요.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        try:
            current_url, current_title = self.queue.pop(0)

            async with ctx.typing():
                self.current_player = await yt_dlp.from_url(current_url, loop=self.bot.loop, stream=True)

                ctx.voice_client.play(self.current_player, after=lambda _: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

                await ctx.send(f'지금 재생 중: {self.current_player.title}')

    except Exception as e:
        await ctx.send(f"재생 중 오류가 발생했습니다: {str(e)}")
        print(f"재생 오류: {e}")
@app_commands.rename(song_name="곡명(URL 또는 곡명)")
async def play_song(interaction: discord.Interaction, song_name: str):
    url = f"https://www.youtube.com/results?search_query={song_name}"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()

    video_info = soup.find("a", attrs={"id": "video-title"})
    title = video_info.get("title")
    href = video_info.get("href")
"""

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='학교정보확인', description='현재 등록된 학교 정보를 확인합니다. /학교등록으로 학교를 등록할 수 있습니다.')
async def check_school_command(interaction: discord.Interaction):
    try:
        result = checkSchool(interaction)
        if (result is None):
            Exception("wrong result")
        embed = discord.Embed(title=f"{interaction.user.display_name}님의 등록된 학교 정보",
                              description=f"## 교명\n{result[UserInfo.school_id.value]}\n## 학반\n{'미등록' if result[UserInfo.grade.value] is None or result[UserInfo.class_number.value] is None else str(result[UserInfo.grade.value]) + '학년 ' + str(result[UserInfo.class_number.value]) + '반'}",
                              color=random.choice(colors))
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message("정보 로딩에 실패했습니다. 학교 정보가 제대로 등록되었는지 확인해주세요.")
        print(e)


class UserInfo(Enum):
    user_id = 0
    school_id = 3
    grade = 1
    class_number = 2
    school_code = 5
    education_center_code = 4


def checkSchool(interaction: discord.Interaction) -> tuple:
    try:
        cur.execute("SELECT * FROM userinfo WHERE user_id = %s;", (interaction.user.id,))
        results = cur.fetchall()
        print(results)
        print(type(results))
        return results[0]
    except Exception as e:
        db.rollback()
        print(e)
        return None


@client.tree.command(name='등록해제', description='발붕이 서버에 등록된 riot id를 지웁니다.')
async def command(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.user.name)

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='업데이트', description='발붕이 / 명령어 세팅을 업데이트합니다.')
async def command(interaction: discord.Interaction):
    try:
        if (interaction.user.guild_permissions.administrator == True or interaction.user.id == 796381848233836574):
            await interaction.response.send_message("명령어 업데이트를 시도합니다..")
            client.tree.copy_global_to(guild=discord.Object(interaction.guild_id))
            await client.tree.sync(guild=discord.Object(interaction.guild_id))
            await interaction.channel.send("명령어 업데이트 완료")
        else:
            await interaction.response.send_message("권한 없는 것이 어딜")
    except:
        await interaction.response.send_message("전아무것도몰루겟수요ㅜㅜ")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='업데이트_owner', description='발붕이 / 명령어 세팅을 업데이트합니다.')
async def command(interaction: discord.Interaction, server_id: str):
    try:
        if (interaction.user.id != 796381848233836574):
            await interaction.response.send_message("주인님만이 사용 가능한 명령어.")
            return Exception
        else:
            await interaction.response.send_message("명령어 업데이트를 시도합니다..")
            client.tree.copy_global_to(guild=discord.Object(server_id))
            await client.tree.sync(guild=discord.Object(server_id))
            await interaction.channel.send("명령어 업데이트 완료")
    except:
        await interaction.response.send_message("전아무것도몰루겟수요ㅜㅜ")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='기억해', description='발붕이에게 언어란 걸 가르치다')
async def command(interaction: discord.Interaction, input: str, output: str):
    if (black_list.__contains__(interaction.user.id)):
        await interaction.response.send_message("나 너 싫어")
        return
    if output.count('|') > 5 or output.__contains__("https://") or output.__contains__(
            "http://") or output.__contains__("](http") or len(input) > 300 or len(output) > 300 or output.__contains__(
            '​') or input.__contains__('​'):
        await interaction.response.send_message("불순한 의도 차단")
        return
    try:
        cur.execute("INSERT INTO edu (input,output,user_id,nickname) VALUES(%s,%s,%s,%s);",
                    (input, output, interaction.user.id, interaction.user.name))
        db.commit()
        await interaction.response.send_message(f"`발붕아 {input}` 이라고 말하면 `{output}` 이라고 답해요",
                                                allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        db.rollback()
        print(e)
        await interaction.response.send_message("전아무것도몰루겟수요ㅜㅜ")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='잊어', description='교육을 잘 못 시킨 것 같다.')
async def command(interaction: discord.Interaction, input: str = ''):
    try:
        if input != '':
            cur.execute("SELECT * from edu where user_id = %s AND input = %s;", (interaction.user.id, input))
            r = cur.fetchall()
            cur.execute("DELETE FROM edu WHERE user_id = %s AND input = %s;", (interaction.user.id, input))
            string = '```'
            if r:
                for i in r:
                    string += f"{i[0]} (이)라 물으면 {i[1]}\n"
                string += '```\n을 잊어버렷'
                await interaction.response.send_message(string)
            else:
                await interaction.response.send_message("그런 거 안 배웠는데요")
        else:
            cur.execute("SELECT * from edu where user_id = %s;", (interaction.user.id,))
            r = cur.fetchall()
            cur.execute("DELETE FROM edu WHERE user_id = %s;", (interaction.user.id,))
            string = '```'
            if r:
                for i in r:
                    string += f"{i[0]} (이)라 물으면 {i[1]}\n"
                string += '```\n을 잊어버렷'
                await interaction.response.send_message(string, allowed_mentions=discord.AllowedMentions.none())
            else:
                await interaction.response.send_message("님한테 배운게 없는데요")
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        await interaction.response.send_message("전아무것도몰루겟수요ㅜㅜ")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='복습', description='내가 뭘 가르쳤더라')
async def command(interaction: discord.Interaction, input: str = ''):
    try:
        if input == '':
            cur.execute("SELECT * FROM edu WHERE user_id = %s;", (interaction.user.id,))
            r = cur.fetchall()
        else:
            cur.execute("SELECT * FROM edu WHERE user_id = %s AND input = %s;", (interaction.user.id, input))
            r = cur.fetchall()
        string = '```'
        if r:
            for i in r:
                string += f"{i[0]} (이)라 물으면 {i[1]}\n"
            string += '```\n을 배웠어요'
            await interaction.response.send_message(string)
        else:
            await interaction.response.send_message("그런 거 안 배웠는데요")
    except Exception as e:
        db.rollback()
        print(e)
        await interaction.response.send_message("전아무것도몰루겟수요ㅜㅜ")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='나가', description='발붕이를 종료합니다(개발자 전용)')
@commands.is_owner()
async def command(interaction: discord.Interaction):
    if (interaction.user.id == 796381848233836574):
        await interaction.response.send_message("넹 꺼질게용")
        exit()
    else:
        await interaction.response.send_message("너나 나가")
        await interaction.channel.guild.get_member(interaction.user.id).timeout(timedelta(minutes=2))

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@client.tree.command(name='헤드샷률', description='헤드샷 비율을 알려줍니다.')
async def command(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.user.name)

@client.tree.command(name='밴', description="분 단위 밴합니다.")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.User, time: int):
    try:
        if interaction.user.guild_permissions.administrator == True or interaction.user.id == 796381848233836574:
            await interaction.response.send_message(f"{user.mention} 너 {time}분 밴",
                                                    allowed_mentions=discord.AllowedMentions(users=False))
            duration = timedelta(minutes=time)
            await interaction.guild.get_member(user.id).timeout(duration, reason="나가")
        else:
            await interaction.response.send_message(f"어딜 @@...ㅡㅡ 괘씸한 것 {interaction.user.mention} 너 {abs(time)}분 밴",
                                                    allowed_mentions=discord.AllowedMentions(users=False))
            duration = timedelta(minutes=abs(time))
            await interaction.guild.get_member(interaction.user.id).timeout(duration / 10, reason="어딜")
    except:
        await interaction.response.send_message("님 권한 없음")


#============================================console commands=======================================================
@my_console.command()
async def unban(user: discord.User, guild: discord.Guild):
    print(f"unban to {user.name} id: = {user.id}")
    await guild.get_member(user.id).timeout(None)


#unban 796381848233836574 1293878848085033001

@my_console.command()
async def ban(user: discord.User, guild: discord.Guild, time):
    print(f"ban to {user.name} id: = {user.id} t:{time}minutes")
    await guild.get_member(user.id).timeout(timedelta(minutes=time))

@my_console.command()
async def restart():
    my_console.start()
    client.run(Token)
    print("재시작해요")


my_console.start()
client.run(Token)
