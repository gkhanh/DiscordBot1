import discord
from discord.ext import commands
from random import choice, random
import asyncpraw
import os
from asyncprawcore import NotFound, Forbidden, Redirect


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(client_id = os.getenv("REDDIT_CLIENT_ID"),
                                       client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
                                       user_agent = "script:memeBot:v1.0 (by u/Gkhanh)")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready!")

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("Test command is working!")

    @commands.command(name="meme")
    async def meme(self, ctx: commands.Context, *, topic: str = "memes"):
        """Fetch a random meme from a specific subreddit based on the topic."""
        try:
            subreddit = await self.reddit.subreddit(topic)
            posts_list = []

            # Select the hot 50 posts with author, url link
            async for post in subreddit.hot(limit=50):
                if not post.over_18 and post.author is not None and any(
                        post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                    author_name = post.author.name
                    posts_list.append((post.url, author_name))
                if post.author is None:
                    posts_list.append((post.url, "N/A"))

            if posts_list:
                random_post = choice(posts_list)

                meme_embed = discord.Embed(
                    title=f"Random Meme from r/{topic}",
                    description=f"Fetches random memes from r/{topic}",
                    colour=discord.Colour.random()
                )
                meme_embed.set_author(name=f"Meme requested by {ctx.author.name}", icon_url=ctx.author.avatar)
                meme_embed.set_image(url=random_post[0])
                meme_embed.set_footer(text=f"Post created by {random_post[1]}.", icon_url=None)

                await ctx.send(embed=meme_embed)

            else:
                await ctx.send(f"Unable to fetch any post from r/{topic}, try another topic or later.")

        except NotFound:
            await ctx.send(f"Subreddit r/{topic} not found. Please try a different topic.")
        except Forbidden:
            await ctx.send(f"Subreddit r/{topic} is private or restricted. Please try a different topic.")
        except Redirect:
            await ctx.send(f"r/{topic} does not exist. Please try a different topic.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}. Please try again later.")

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())

async def setup(bot):
    await bot.add_cog(Reddit(bot))

