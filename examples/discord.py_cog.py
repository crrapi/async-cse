"""
MIT License

Copyright (c) 2018 Chris Rrapi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# pylint: disable=R0903
import time

import discord
from discord.ext import commands
import async_cse


# ----
# Big thanks to surprise#1161 for this
# ----


class Google:
    """Commands for searching things on Google."""

    def __init__(self, bot):
        self.bot = bot
        self.google = async_cse.Search("API KEY HERE")  # insert your key here

    @commands.group(
        pass_context=True,
        invoke_without_command=True,
        name="search",
        aliases=["g", "google"],
    )
    @commands.cooldown(
        1, 10, commands.BucketType.guild
    )  # after the first invoke, set time cooldown to 10
    async def search(self, ctx, *, query: str):
        """Search queries from Google"""
        try:
            start = time.time()
            resp = (await self.google.search(query))[0]
        except async_cse.NoResults:
            return await ctx.send("No results for this query...")
        except (async_cse.NoMoreRequests, async_cse.APIError):
            return await ctx.send("Internal error ocurred, please try again later.")
        else:
            embed = discord.Embed(
                title=resp.title,
                description=resp.description,
                colour=discord.Color.blurple(),
                url=resp.url,
            )
            embed.set_thumbnail(url=resp.image_url)
            end = time.time()
            execution_time = f"{end - start:.2f}s"
            embed.set_footer(text=execution_time)
            await ctx.send(embed=embed)

    @search.command(name="search_image", aliases=["i", "image"], pass_context=True)
    @commands.cooldown(
        1, 10, commands.BucketType.guild
    )  # after the first invoke, set time cooldown to 10
    async def search_image(self, ctx, query: str):
        """Search images from Google"""
        try:
            start = time.time()
            resp = (await self.google.search(query, image_search=True))[0]
        except async_cse.NoResults:
            return await ctx.send("No results for this query...")
        except (async_cse.NoMoreRequests, async_cse.APIError):
            return await ctx.send("An internal error occurred, please try again later.")
        else:
            embed = discord.Embed(
                title=resp.title,
                description=resp.description,
                colour=discord.Color.blurple(),
                url=resp.url,
            )
            embed.set_thumbnail(url=resp.image_url)
            end = time.time()
            execution_time = f"{end - start:.2f}s"
            embed.set_footer(text=execution_time)
            await ctx.send(embed=embed)

    @search.error
    async def search_error_handler(self, ctx, error):
        """Local error handler for search command"""
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            await ctx.send(f"Wait {seconds:.2f}s!")


def setup(bot):
    """Adds the cog"""
    bot.add_cog(Google(bot))
