from nextcord import SlashOption, ChannelType
import nextcord, datetime, sqlite3, pytz, random, asyncio, time
from nextcord.ui import Button, View
from nextcord import ButtonStyle
from nextcord.abc import GuildChannel

intents = nextcord.Intents.default()
intents.members = True
client = nextcord.Client(intents=intents)
  
#========================



#========================

@client.event
async def on_ready():
    i = datetime.datetime.now()
    print(f"{client.user.name}봇은 준비가 완료 되었습니다.")
    print(f"[!] 참가 중인 서버 : {len(client.guilds)}개의 서버에 참여 중")
    print(f"[!] 이용자 수 : {len(client.users)}와 함께하는 중")
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"대규모 업데이트중.."))
    print(i)

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"대규모 업데이트중.."))

@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"대규모 업데이트중.."))

#=================================================================================================================================

@client.slash_command(name="경고",description="경고를 지급하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 멤버: nextcord.Member, 경고수: int, 사유: str) -> None:
    try:
        if inter.user.guild_permissions.administrator:
                conn = sqlite3.connect("danger.db", isolation_level=None)
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS danger(user_id INTEGER PRIMARY KEY, guild_id INTEGER, count INTEGER)")
                if c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}").fetchone() is None:
                    c.execute("INSERT INTO danger (user_id,guild_id, count) VALUES (?, ?, ?)", (멤버.id, inter.guild.id, 경고수))
                    embed = nextcord.Embed(title=f"경고 지급 완료!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"정보", value=f"사유 : {사유}\n현재 경고 수 : **{경고수}번**", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
                else:
                    c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}")
                    y = c.fetchone()
                    c.execute("UPDATE danger SET count=? WHERE user_id=? AND guild_id=?",(y[2] + 경고수, 멤버.id, inter.guild.id,))
                    embed = nextcord.Embed(title=f"경고 지급 완료!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"정보", value=f"사유 : {사유}\n현재 경고 수 : **{경고수 + y[2]}번**", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("관리자 권한이 필요합니다!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`경고`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


@client.slash_command(name="경고차감",description="경고를 차감하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 멤버: nextcord.Member, 경고수: int) -> None:
    try:
        if inter.user.guild_permissions.administrator:
            conn = sqlite3.connect("danger.db", isolation_level=None)
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS danger(user_id INTEGER PRIMARY KEY, guild_id INTEGER, count INTEGER)")
            if c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}").fetchone() is None:
                await inter.response.send_message(f"해당 멤버는 경고를 보유하지 않았습니다!")
            else:
                c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}")
                y = c.fetchone()
                c.execute("UPDATE danger SET count=? WHERE user_id=? AND guild_id=?",(y[2]-경고수, 멤버.id, inter.guild.id,))
                z = c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}").fetchone()
                if z[-1] <= 0:
                    c.execute("DELETE FROM danger WHERE guild_id=? AND user_id=?", (inter.guild.id, 멤버.id,))
                    embed = nextcord.Embed(title=f"경고 차감 완료!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"정보", value=f"현재 경고 수 : **0번**", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
                else:
                    embed = nextcord.Embed(title=f"경고 차감 완료!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"정보", value=f"현재 경고 수 : **{y[2]-경고수}번**", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("관리자 권한이 필요합니다!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`경고차감`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


@client.slash_command(name="경고확인",description="경고를 확인 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 멤버: nextcord.Member) -> None:
    try:
            if inter.user.guild_permissions.administrator:
                conn = sqlite3.connect("danger.db", isolation_level=None)
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS danger(user_id INTEGER PRIMARY KEY, guild_id INTEGER, count INTEGER)")
                if c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}").fetchone() is None:
                    await inter.response.send_message(f"현재 경고가 없는 사용자 입니다!")
                else:
                    c.execute(f"SELECT * FROM danger WHERE user_id={멤버.id} AND guild_id={inter.guild.id}")
                    y = c.fetchone()
                    embed = nextcord.Embed(title=f"경고 현황!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"정보", value=f"현재 경고 수 : **{y[2]}번**", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
            else:
                await inter.response.send_message("관리자 권한이 필요합니다!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`경고확인`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)

#=================================================================================================================================



#=================================================================================================================================

@client.slash_command(name="청소",description="메세지를 청소할 수 있습니다!")
async def hello(inter: nextcord.Interaction, 메세지_갯수: int) -> None:
    try:
        amount = 메세지_갯수+1
        if inter.user.guild_permissions.administrator:
            if amount > 100:
                embed = nextcord.Embed(title=f"청소가 취소되었어요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"청소취소 사유", value=f"\n100이상에 값을 입력함", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)
            else:
                embed = nextcord.Embed(title=f"청소가 완료되었어요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"삭제된 메세지", value=f"\n{amount - 1}개에 메세지가 삭제됨", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)
                await inter.channel.purge(limit=amount)
        else:
            await inter.response.send_message("관리자 권한이 필요합니다!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`청소`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


#=================================================================================================================================



#=================================================================================================================================

@client.slash_command(name="큐알코드",description="큐알코드를 제작 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 링크: str) -> None:
    try:
        embed = nextcord.Embed(title="QR코드", description="QR코드를 만들고 있습니다...",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        loadingmsg = await inter.response.send_message(embed=embed)
        qrserver = f"https://api.qrserver.com/v1/create-qr-code/?data={링크}"
        embed = nextcord.Embed(title="QR코드", description="요청하신 QR코드입니다!", color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.set_image(url=f"{qrserver}")
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.edit_original_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`큐알코드`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


#=================================================================================================================================

@client.slash_command(name="bmi",description="bmi를 확인 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 키: int, 몸무게: int) -> None:
    try:
        h1 = 키/100
        h2 = h1*h1
        b = round(몸무게/h2, 1)
        if b <=  18.5:
            embed = nextcord.Embed(title=f"bmi지수를 알려드릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.add_field(name=f"BMI", value=f"\nBMI : {b}\n단계 : 저체중", inline=True)
            embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
            await inter.response.send_message(embed=embed)

        elif 18.5 < b <= 24.9:
                embed = nextcord.Embed(title=f"bmi지수를 알려드릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"BMI", value=f"\nBMI : {b}\n단계 : 정상", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)

        elif 24.9 < b <= 29.9:
                embed = nextcord.Embed(title=f"bmi지수를 알려드릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"BMI", value=f"\nBMI : {b}\n단계 : 초기비만", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)

        elif 29.9 < b <=  34.9:
                embed = nextcord.Embed(title=f"bmi지수를 알려드릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"BMI", value=f"\nBMI : {b}\n단계 : 2단계 비만", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)

        elif 34.9 < b:
                embed = nextcord.Embed(title=f"bmi지수를 알려드릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"BMI", value=f"\nBMI : {b}\n단계 : 고도비만!", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`BMI`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


#=================================================================================================================================

cp = ['inf엔터', 'inf전자', "inf건설"]

@client.slash_command(name="도박가입",description="봇 서비스에 가입하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 회사: str = SlashOption(description="더 많은 회사 추가 예정!", choices=cp)) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS cp(name TEXT PRIMARY KEY, money INTEGER, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            if 회사 == cp[0]:
                y = c.execute(f"SELECT * FROM cp WHERE name='inf엔터'").fetchone()
                c.execute("UPDATE cp SET ct=? WHERE name=?",(y[-1]+1, 'inf엔터',))
                c.execute("UPDATE cp SET money=? WHERE name=?",(y[1]+5000, 'inf엔터',))
            elif 회사 == cp[1]:
                y = c.execute(f"SELECT * FROM cp WHERE name='inf전자'").fetchone()
                c.execute("UPDATE cp SET ct=? WHERE name=?",(y[-1]+1, 'inf전자',))
                c.execute("UPDATE cp SET money=? WHERE name=?",(y[1]+5000, 'inf전자',))
            elif 회사 == cp[2]:
                y = c.execute(f"SELECT * FROM cp WHERE name='inf건설'").fetchone()
                c.execute("UPDATE cp SET ct=? WHERE name=?",(y[-1]+1, 'inf건설',))
                c.execute("UPDATE cp SET money=? WHERE name=?",(y[1]+5000, 'inf건설',))
            c.execute("INSERT INTO casino (user_id, money, cp, sp, ct) VALUES (?, ?, ?, ?, ?)", (user, 5000, 회사, "인턴", 0,))
            embed = nextcord.Embed(title=f"가입 성공!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.add_field(name=f"정보", value=f"기본 돈 **5000**원이 지급됨\n회사 : **{회사}**\n직위 : **인턴**", inline=True)
            embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
            await inter.response.send_message(embed=embed)
        else:
                embed = nextcord.Embed(title=f"가입 실패!",description="이미 가입 하셨어요..!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`가입`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)

@client.slash_command(name="회사정보",description="회사 정보를 확인 하실 수 있습니다")
async def hello(inter: nextcord.Interaction, 회사: str = SlashOption(description="더 많은 회사 추가 예정!", choices=cp)) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS cp(name TEXT PRIMARY KEY, money INTEGER, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
            if 회사 == 'inf엔터':
                y = c.execute(f"SELECT * FROM cp WHERE name='inf엔터'").fetchone()
                embed = nextcord.Embed(title=f"회사!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"정보", value=f"시급 : **10000원**\n자금 : {y[1]}\n직원 수 : {y[2]}", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.send(embed=embed)
            elif 회사 == 'inf전자':
                y = c.execute(f"SELECT * FROM cp WHERE name='inf전자'").fetchone()
                embed = nextcord.Embed(title=f"회사!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"정보", value=f"시급 : **10000원**\n자금 : {y[1]}\n직원 수 : {y[2]}", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.send(embed=embed)
            elif 회사 == "inf건설":
                y = c.execute(f"SELECT * FROM cp WHERE name='inf건설'").fetchone()
                embed = nextcord.Embed(title=f"회사!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"정보", value=f"시급 : **10000원**\n자금 : {y[1]}\n직원 수 : {y[2]}", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.send(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`가입`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)

#=================================================================================================================================

@client.slash_command(name="도박",description="도박을 할 수 있습니다!")
async def hello(inter: nextcord.Interaction, 돈: int) -> None:
    try:
        user = inter.user.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
            y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
            if 돈 > y[1]:
                await inter.response.send_message("잔액을 제대로 입력해주세요!")
            else:
                i = random.randint(1,5)
                if i == 1 or i == 2:
                    c.execute("UPDATE casino SET money=? WHERE user_id=?",(y[1]+돈, user,))
                    y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                    await inter.response.send_message(f"당첨 되셨습니다! **잔액 : {y[1]}**")
                else:
                    c.execute("UPDATE casino SET money=? WHERE user_id=?",(y[1]-돈, user,))
                    y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                    if y[1] == 0:
                        await inter.response.send_message("실패... 전재산을 탕진 하셨군요.. 다시 시작하세요!\n**1000원을 지급해드릴게요!**")
                        c.execute("UPDATE casino SET money=? WHERE user_id=?",(1000, user,))
                    else:
                        y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                        await inter.response.send_message(f"실패... 하셨어요.. **잔액 : {y[1]}**")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`도박`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


#=================================================================================================================================

@client.slash_command(name="정보",description="유저에 잔액을 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
                y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                embed = nextcord.Embed(title=f"정보!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"{inter.user.name}님의 잔액", value=f"잔액 : **{y[1]}**")
                embed.add_field(name=f"{inter.user.name}님의 회사", value=f"회사 : **{y[2]}**\n직위 : **{y[3]}**\n회사에서 일한 시간 : **{y[4]}시간**")
                embed.set_thumbnail(url=inter.user.avatar.url)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                await inter.response.send_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`잔액`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


#=================================================================================================================================

@client.slash_command(name="송금",description="송금을 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction, 돈: int, 멤버: nextcord.Member) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
            y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
            if y[1] <= 돈:
                await inter.response.send_message("전재산 후원은 불가능 합니다!")
            else:
                if c.execute(f"SELECT * FROM casino WHERE user_id={멤버.id}").fetchone() is None:          
                    await inter.response.send_message("가입되지 않은 사용자 입니다!")
                else:
                    v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                    z = c.execute(f"SELECT * FROM casino WHERE user_id={멤버.id}").fetchone()
                    c.execute("UPDATE casino SET money=? WHERE user_id=?",(z[1]+돈, 멤버.id,))
                    c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]-돈, user,))
                    embed = nextcord.Embed(title=f"송금!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"{inter.user}님의 잔액", value=f"잔액 : **{v[1]-돈}**")
                    embed.add_field(name=f"{멤버}님의 잔액", value=f"잔액 : **{z[1]+돈}**")
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`송금`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


#=================================================================================================================================

@client.slash_command(name="돈줘",description="봇 개발자만 이용 할 수 있습니다!")
async def hello(inter: nextcord.Interaction, 돈: int) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        if user == 815013473133920297:
            v = c.execute(f"SELECT * FROM casino WHERE user_id=815013473133920297").fetchone()
            c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]+돈, user,))
            await inter.response.send_message("돈을 지급하였습니다!")
        else:
            await inter.response.send_message("봇 관리자만 이용이 가능합니다!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`돈줘`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)


@client.slash_command(name="핑",description="핑을 확인 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction) -> None:
    try:
        la = client.latency
        embed = nextcord.Embed(title=f"퐁🏓! 현재 핑을 알려드릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"핑", value=f"\n{str(round(la * 1000))}ms", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.response.send_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`핑`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)

@client.slash_command(name="순위표",description="돈 순위를 확인 하실 수 있습니다!")
async def hello(inter: nextcord.Interaction) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        y = c.execute("SELECT * FROM casino").fetchall()
        gameList = sorted(list(y), key = lambda x:x[1] , reverse=True)
        print(gameList)
        embed = nextcord.Embed(title=f"순위표!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"순위!", value=f"<@{gameList[0][0]}> : {gameList[0][1]}\n<@{gameList[1][0]}> : {gameList[1][1]}\n<@{gameList[2][0]}> : {gameList[2][1]}\n<@{gameList[3][0]}> : {gameList[3][1]}\n<@{gameList[4][0]}> : {gameList[4][1]}", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.response.send_message(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`순위표`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)

@client.slash_command(name="로그설정",description="특정채널에 로그를 기록하는 메세지를 보낼 수 있습니다")
async def hello(inter: nextcord.Interaction, 채널이름: GuildChannel = SlashOption(description = "등록할 채널을 선택해주세요!",channel_types = [ChannelType.text])) -> None:
    try:
        if inter.user.guild_permissions.administrator:
            user = inter.user.id
            guild = inter.guild.id
            conn = sqlite3.connect("log.db", isolation_level=None)
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS log(guild_id INTEGER PRIMARY KEY, channel_id INTEGER)")
            if 채널이름 == "삭제":
                if c.execute(f"SELECT * FROM log WHERE guild_id={guild}").fetchone() is None:
                    await inter.send("이미 위 서버 데이터가 없어요!")
                else:
                    c.execute("DELETE FROM 'log' WHERE guild_id=?", (guild,))
                    embed = nextcord.Embed(title=f"로그 설정이 삭제되었습니다!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                    await inter.response.send_message(embed=embed)
            else:
                    channel = 채널이름
                    채널id = channel.id
                    if c.execute(f"SELECT * FROM log WHERE guild_id={guild}").fetchone() is None:
                        c.execute("INSERT INTO log (guild_id, channel_id) VALUES (?, ?)", (guild, 채널id,))
                        embed = nextcord.Embed(title=f"로그 설정 성공!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                        embed.add_field(name=f"정보", value=f"이제부터 <#{채널id}>의 로그를 기록합니다!\n기록을 취소 하고 싶다면 채널이름 란에 삭제 라고 해주세요!", inline=True)
                        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                        await inter.response.send_message(embed=embed)
                    else:
                        c.execute("UPDATE log SET channel_id=? WHERE guild_id=?",(채널id, guild,))
                        embed = nextcord.Embed(title=f"로그 설정이 변경되었습니다!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                        embed.add_field(name=f"정보", value=f"이제 <#{채널id}>로 로그를 기록할게요!\n기록을 취소 하고 싶다면 채널이름 란에 삭제 라고 해주세요!")
                        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
                        await inter.response.send_message(embed=embed)
        else:
            await inter.send("관리자 권한이 필효합니다!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await inter.send(embed=embed)
        ch = client.get_channel(971420989374234624)
        embed = nextcord.Embed(title=f"에러!",description=f"`로그설정`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
        await ch.send(embed=embed)

@client.event
async def on_message_delete(message):
    if message.author.bot:
        return None
    else:
        guild = message.guild.id
        conn = sqlite3.connect("log.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS log(guild_id INTEGER PRIMARY KEY, channel_id INTEGER)")
        if c.execute(f"SELECT * FROM log WHERE guild_id={guild}").fetchone() is None:
            return None
        else:
            y = c.execute(f"SELECT * FROM log WHERE guild_id={guild}").fetchone()[1]
            ch = client.get_channel(y)
            embed = nextcord.Embed(title=f"삭제됨", description=f"유저 : {message.author.mention} 채널 : {message.channel.mention}", color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.add_field(name="삭제된 내용", value=f"```내용 : {message.content}```", inline=False)
            embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
            await ch.send(embed=embed)

@client.event
async def on_message_edit(before, after):
    if before.author.bot:
        return None
    else:
        guild = before.guild.id
        conn = sqlite3.connect("log.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS log(guild_id INTEGER PRIMARY KEY, channel_id INTEGER)")
        if c.execute(f"SELECT * FROM log WHERE guild_id={guild}").fetchone() is None:
            return None
        else:
            y = c.execute(f"SELECT * FROM log WHERE guild_id={guild}").fetchone()[1]
            ch = client.get_channel(y)
            embed = nextcord.Embed(title=f"수정됨", description=f"유저 : {before.author.mention} 채널 : {before.channel.mention}",  color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.add_field(name="수정 전 내용", value=f"```{before.content}```", inline=True)
            embed.add_field(name="수정 후 내용", value=f"```{after.content}```", inline=True)
            embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/pH7U82m.png")
            await ch.send(embed=embed)
        
@client.slash_command(name="유저베팅",description="유저끼리 돈을 배팅 할 수 있습니다!")
async def hello(inter: nextcord.Interaction, 돈:  int) -> None:
    try:
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%82%AC%EB%8B%A4%EB%A6%AC%ED%83%80%EA%B8%B0"
        
        user = inter.user.id
        guild = inter.guild.id
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
            yes = Button(label="✅수락", style=ButtonStyle.green)
            no = Button(label="❌베팅 취소", style=ButtonStyle.red)
            myview = View()
            myview.add_item(yes)
            myview.add_item(no)
            embed = nextcord.Embed(title=f"유저 베팅!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.add_field(name=f"정보", value=f"베팅 금액 : {돈}\n참여를 원하시면 수락 버튼을 눌러주세요!", inline=True)
            embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
            await inter.send(embed=embed, view=myview)
            async def yes_callback(interaction):
                if interaction.user.id == inter.user.id:
                    pass
                else:
                    if c.execute(f"SELECT * FROM casino WHERE user_id={interaction.user.id}").fetchone() is None:
                        await inter.edit_original_message("**/가입**으로 가입 부탁드립니다!")
                    else:
                        if c.execute(f"SELECT * FROM casino WHERE user_id={interaction.user.id}").fetchone()[1] > 돈:
                            embed = nextcord.Embed(title="베팅 승락!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                            embed.add_field(name="5초후 베팅이 시작됩니다!", value=f"{inter.user.name} vs {interaction.user.name}", inline=True)
                            embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                            await inter.edit_original_message(embed=embed, view=None)
                            await asyncio.sleep(5)
                            i = random.randint(1,10)
                            if i == 1 or i == 2 or i == 3 or i == 4 or i == 5:
                                v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                                z = c.execute(f"SELECT * FROM casino WHERE user_id={interaction.user.id}").fetchone()
                                c.execute("UPDATE casino SET money=? WHERE user_id=?",(z[1]-돈, interaction.user.id,))
                                c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]+돈, user,))
                                embed = nextcord.Embed(title="베팅 결과!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                                embed.add_field(name="베팅 결과", value=f"{inter.user.mention}님이 승리!", inline=True)
                                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                                await inter.edit_original_message(embed=embed, view=None)
                            else:
                                v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                                z = c.execute(f"SELECT * FROM casino WHERE user_id={interaction.user.id}").fetchone()
                                c.execute("UPDATE casino SET money=? WHERE user_id=?",(z[1]+돈, interaction.user.id,))
                                c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]-돈, user,))
                                embed = nextcord.Embed(title="베팅 결과!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                                embed.add_field(name="베팅 결과", value=f"{interaction.user.mention}님이 승리!", inline=True)
                                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                                await inter.edit_original_message(embed=embed, view=None)
                        else:
                            await inter.edit_original_message("전재산 배팅 불가능!")

        yes.callback = yes_callback

        async def no_callback(interaction):
            if interaction.user.id == inter.user.id:
                embed = nextcord.Embed(title="베팅이 취소됨",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                await inter.edit_original_message(embed=embed, view=None)
            else:
                return
        no.callback = no_callback

    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
        await inter.send(embed=embed)
        ch = client.get_channel(974698263011815444)
        embed = nextcord.Embed(title=f"에러!",description=f"`유저베팅`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
        await ch.send(embed=embed)

@client.slash_command(name="주사위",description="봇과 주사위 대결을 할 수 있어요!")
async def hello(inter: nextcord.Interaction, 돈: int) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        mem = inter.user.name
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        i = random.randrange(1,7)
        l = random.randrange(1,7)
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
            if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()[1] > 돈:
                embed = nextcord.Embed(title=f"{mem}님 주사위를 굴릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"{mem}님의 주사위", value=f"🎲굴리는중...", inline=True)
                embed.add_field(name=f"inf의 주사위", value=f"대기중", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                msg = await inter.send(embed=embed)

                await asyncio.sleep(2)

                embed = nextcord.Embed(title=f"{mem}님 주사위를 굴릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"{mem}님의 주사위", value=f"🎲{i}!!", inline=True)
                embed.add_field(name=f"inf의 주사위", value=f"🎲굴리는중...", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                msg2 = await inter.edit_original_message(embed=embed)

                await asyncio.sleep(2)

                embed = nextcord.Embed(title=f"{mem}님 주사위를 굴릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                embed.add_field(name=f"{mem}님의 주사위", value=f"🎲{i}!!", inline=True)
                embed.add_field(name=f"inf의 주사위", value=f"🎲{l}!!", inline=True)
                embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                msg3 = await inter.edit_original_message(embed=embed)

                if i < l:
                    v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                    c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]-돈, user,))
                    embed = nextcord.Embed(title=f"{mem}님 주사위를 굴릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"{mem}님의 주사위", value=f"🎲{i}!!", inline=True)
                    embed.add_field(name=f"inf의 주사위", value=f"🎲{l}!!", inline=True)
                    embed.add_field(name=f"승자", value=f"🎲{i} < 🎲{l} 이므로 승은 inf!", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                    await inter.edit_original_message(embed=embed)

                elif l < i:
                    v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                    c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]+돈, user,))
                    embed = nextcord.Embed(title=f"{mem}님 주사위를 굴릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"{mem}님의 주사위", value=f"🎲{i}!!", inline=True)
                    embed.add_field(name=f"inf의 주사위", value=f"🎲{l}!!", inline=True)
                    embed.add_field(name=f"승자", value=f"🎲{l} < 🎲{i} 이므로 승은 {mem}!", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                    await inter.edit_original_message(embed=embed)

                else:
                    embed = nextcord.Embed(title=f"{mem}님 주사위를 굴릴게요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    embed.add_field(name=f"{mem}님의 주사위", value=f"🎲{i}!!", inline=True)
                    embed.add_field(name=f"inf의 주사위", value=f"🎲{l}!!", inline=True)
                    embed.add_field(name=f"승자", value=f"🎲{l} = 🎲{i} 이므로 무승부...!", inline=True)
                    embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
                    await inter.edit_original_message(embed=embed)
            else:
                await inter.send("전재산 배팅 불가능!")
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
        await inter.send(embed=embed)
        ch = client.get_channel(974698263011815444)
        embed = nextcord.Embed(title=f"에러!",description=f"`주사위`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
        await ch.send(embed=embed)

@client.slash_command(name="일",description="일을 할 수 있어요!")
async def hello(inter: nextcord.Interaction, 일: str = SlashOption(description="선택 해주세요!", choices=["시작", "그만"])) -> None:
    try:
        user = inter.user.id
        guild = inter.guild.id
        mem = inter.user.name
        conn = sqlite3.connect("money.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS casino(user_id INTEGER PRIMARY KEY, money INTEGER, cp TEXT, sp TEXT, ct INTEGER)")
        if c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone() is None:
            await inter.response.send_message("**/가입**으로 가입 부탁드립니다!")
        else:
            if 일 == "시작":
                y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                if y[2] == "inf엔터":
                    await inter.send('일을 시작합니다!')
                    global time_1
                    time_1 = time.time()
                elif y[2] == "inf전자":
                    await inter.send('일을 시작합니다!')
                    global time_2
                    time_2 = time.time()
                else:
                    await inter.send('일을 시작합니다!')
                    global time_3
                    time_3 = time.time()
            else:
                y = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                if y[2] == "inf엔터":
                    try:
                        y = c.execute(f"SELECT * FROM cp WHERE name='inf엔터'").fetchone()
                        v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                        z = round((time.time() - time_1)/3600, 1)
                        await inter.send(f'일한 시간 : {round((time.time() - time_1)/3600, 1)}시간')
                        c.execute("UPDATE casino SET ct=? WHERE user_id=?",(v[4]+z, user,))
                        if z >= 1:
                            x = round(z)*3000
                            c.execute("UPDATE cp SET money=? WHERE name=?",(y[1]+x, "inf엔터"))
                            p  = round(z)*10000
                            c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]+p, user))
                            o = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                            if o[4] > 190:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("부사장", user))
                            elif o[4] > 170:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("전무", user))
                            elif o[4] > 150:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("상무", user))
                            elif o[4] > 130:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("이사", user))
                            elif o[4] > 110:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("부장", user))
                            elif o[4] > 90:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("차장", user))
                            elif o[4] > 70:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("과장", user))
                            elif o[4] > 50:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("대리", user))
                            elif o[4] > 30:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("주임", user))
                            elif o[4] > 10:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("사원", user))
                    except:
                        await inter.send(f'일을 시작하지 않았어요! `/일시작`')
                elif y[2] == "inf전자":
                    try:
                        y = c.execute(f"SELECT * FROM cp WHERE name='inf전자'").fetchone()
                        v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                        z = round((time.time() - time_1)/3600, 1)
                        await inter.send(f'일한 시간 : {round((time.time() - time_1)/3600, 1)}시간')
                        c.execute("UPDATE casino SET ct=? WHERE user_id=?",(v[4]+z, user,))
                        if z >= 1:
                            x = round(z)*3000
                            c.execute("UPDATE cp SET money=? WHERE name=?",(y[1]+x, "inf전자"))
                            p  = round(z)*10000
                            c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]+p, user))
                            o = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                            if o[4] > 190:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("부사장", user))
                            elif o[4] > 170:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("전무", user))
                            elif o[4] > 150:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("상무", user))
                            elif o[4] > 130:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("이사", user))
                            elif o[4] > 110:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("부장", user))
                            elif o[4] > 90:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("차장", user))
                            elif o[4] > 70:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("과장", user))
                            elif o[4] > 50:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("대리", user))
                            elif o[4] > 30:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("주임", user))
                            elif o[4] > 10:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("사원", user))
                    except:
                        await inter.send(f'일을 시작하지 않았어요! `/일시작`')
                else:
                    try:
                        y = c.execute(f"SELECT * FROM cp WHERE name='inf건설'").fetchone()
                        v = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                        z = round((time.time() - time_1)/3600, 1)
                        await inter.send(f'일한 시간 : {round((time.time() - time_1)/3600, 1)}시간')
                        c.execute("UPDATE casino SET ct=? WHERE user_id=?",(v[4]+z, user,))
                        if z >= 1:
                            x = round(z)*3000
                            c.execute("UPDATE cp SET money=? WHERE name=?",(y[1]+x, "inf건설"))
                            p  = round(z)*10000
                            c.execute("UPDATE casino SET money=? WHERE user_id=?",(v[1]+p, user))
                            o = c.execute(f"SELECT * FROM casino WHERE user_id={user}").fetchone()
                            if o[4] > 190:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("부사장", user))
                            elif o[4] > 170:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("전무", user))
                            elif o[4] > 150:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("상무", user))
                            elif o[4] > 130:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("이사", user))
                            elif o[4] > 110:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("부장", user))
                            elif o[4] > 90:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("차장", user))
                            elif o[4] > 70:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("과장", user))
                            elif o[4] > 50:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("대리", user))
                            elif o[4] > 30:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("주임", user))
                            elif o[4] > 10:
                                c.execute("UPDATE casino SET sp=? WHERE user_id=?",("사원", user))
                    except:
                        await inter.send(f'일을 시작하지 않았어요! `/일시작`')
    except Exception as e:
        embed = nextcord.Embed(title=f"에러!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```해당 에러를 개발자에게 제출중입니다!", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
        await inter.send(embed=embed)
        ch = client.get_channel(974698263011815444)
        embed = nextcord.Embed(title=f"에러!",description=f"`일하기`명령 에러",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.add_field(name=f"Error", value=f"```{e}```", inline=True)
        embed.set_footer(text="client Made by. ! 𝓫𝔂𝓮𝓸𝓵𝓴𝓲#8761", icon_url="https://i.imgur.com/zqx0nAn.jpeg")
        await ch.send(embed=embed)

client.run("토큰")