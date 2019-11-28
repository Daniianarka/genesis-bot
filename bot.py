import discord
import asyncio
import aiohttp
import discord.ext.commands as cmd
import os, sys, time
import traceback as tb
import json

with open(os.path.join(sys.path[0], "config.json"), "r") as config:
    data = json.load(config)


class Genesis(cmd.Bot):
    def __init__(self):
        self.cogs_ = ["jishaku"]
        self.dev = int(data["dev"])
        self.url = "https://github.com/JoseMHC/genesis-bot"
        self.session = aiohttp.ClientSession()
                
        super().__init__(command_prefix=self.prefix,
                         owner=self.dev,
                         description=f"ayy ùwú")
                         
        self.status_bg = self.loop.create_task(self.status_task())
    
                             
    async def prefix(self, bot, message):
        prefixes = ["gen "]
        if message.guild is None:
            return ""
        else:
            return cmd.when_mentioned_or(*prefixes)(bot, message)
    
    ###########PROPERTY
        
    @property
    async def command_amount(self):
        await self.wait_until_ready()
        a = {x for x in super().walk_commands()}
        return len(a)
            
    ###########BG TASKS
        
    async def status_task(self):
        await self.wait_until_ready()
        status = [discord.Status.online, discord.Status.idle, discord.Status.dnd]
        message = [f'@{super().user.name} help (or gen help)',
                   f'{len(super().guilds)} guild(s) ;w;',
                   f'Created in {super().user.created_at.strftime("%Y-%m-%d")}',
                   f'@{super().user.name} help (or gen help)',
                   f'Made in discord.py v{discord.__version__} by Bell ✭ ☆#5144']
        n = 0
        m = 0
        while not self.is_closed():
            if n == len(status):
                n = 0
            if m == len(message):
                m = 0
            game = discord.Game(message[m])
            await super().change_presence(status=status[n], activity=game)
            n += 1
            m += 1
            await asyncio.sleep(18)
            
    ###########EVENTS
        
    async def on_ready(self):
        ownerdata = super().get_user(self.dev)
        print('Logged in as {0}'.format(super().user))
        print("Developed by ", ownerdata)
        print(f"Using discord.py v{discord.__version__}")
        print("__________________________________________________________________________")
        games = discord.Game(f'@{super().user.name} help (or gen help)')
        await super().change_presence(activity=games)
        bid = (await super().application_info()).id
        self.invite = f"https://discordapp.com/oauth2/authorize?&client_id={bid}&scope=bot&permissions=268823744"
        
    async def on_guild_join(self, guild):
        e = discord.Embed(title="NEW GUILD", color=discord.Color.orange())
        e.add_field(name="Name/ID", value=f"{guild} | {guild.id}")
        e.add_field(name="Members", value=f"{guild.member_count} members", inline=False)
        e.add_field(name="Creation date", value=f"{guild.created_at.replace(microsecond=0)}", inline=False)
        e.add_field(name="Owner", value=f"{guild.owner} | {guild.owner.id}", inline=False)
        if guild.icon_url:
            e.set_image(url=guild.icon_url)
        await (super().get_user(self.dev)).send(embed=e)
            
    ###########METHODS
   
    def run(self):
    
        dir = os.path.join(sys.path[0], "cogs")
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        for f in files:
            cog = "cogs." + f.split(".")[0]
            self.cogs_.append(cog)
            
    
        for ext in self.cogs_:
            try:
                self.load_extension(ext)
                print(f"Cog <{ext}> loaded.")
            except Exception as e:
                print(f'Something went wrong when trying to load extension {ext}: {e}')
        super().get_cog("Jishaku").retain=True
        super().get_cog("Jishaku").hidden=True
        super().get_cog("Jishaku").nsfw=False
        super().run(data['token'], reconnect=True)
            
                
                
gen = Genesis()

@gen.command() 
async def ping(ctx):
    tytime = time.perf_counter()
    async with ctx.channel.typing():
        start = time.perf_counter()
        m = await ctx.send('Ping...')
        end = time.perf_counter()
        duration = (end - start) * 1000
        tytimend = time.perf_counter()
        tydur = (tytimend -tytime) * 1000
        await m.edit(content=f'Pong!\nMessage send time = {duration:.2f}ms\nBot latency = {gen.latency*1000:.2f}\nCommand call time = {tydur:.2f}\nAverage = {((duration+tydur+ gen.latency*1000)/3):.2f}')
        
if __name__ == "__main__":
    gen.run()