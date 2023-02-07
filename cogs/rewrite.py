import discord
from discord.ext import commands
from discord.utils import find
from lib.embeds import *
from lib.prefixes import get_prefix
from lib.utils import fetch_message, get_channel, TEXT_INVALID_MESSAGE_LINK

TEXT_FORMAT_TEMPLATE = 'Copy and paste the following template:\n```json\n{0}\n```'  # arg: message text
TEXT_ONLY_HUMANS = 'I can only post messages that were written by humans!'
TEXT_TOO_LONG = 'Discord only allows me to post messages up to 2000 characters long!'

class Rewrite(commands.Cog):
    help = {
        KEY_EMOJI: '📝',
        KEY_TITLE: 'Rewrite',
        KEY_DESCRIPTION: 'Facilitates collaborative editing of Discord posts.',
        KEY_COMMAND: '!rewrite',
        KEY_SUBCOMMANDS: [
            {
                KEY_EMOJI: '📨',
                KEY_TITLE: 'post [message link] [channel]',
                KEY_DESCRIPTION: 'Posts the content of the linked message to the specified channel.',
                KEY_EXAMPLE: '!rw post https://discord.com/URL #announcements'
            },
            {
                KEY_EMOJI: '📝',
                KEY_TITLE: 'edit [message link]',
                KEY_DESCRIPTION: 'Provides a template for editing the specified message.',
                KEY_EXAMPLE: '!rw edit https://discord.com/URL'
            },
            {
                KEY_EMOJI: '♻',
                KEY_TITLE: 'replace [old message link] [new message link]',
                KEY_DESCRIPTION: 'Replaces the content of the old message with the content of the new message.',
                KEY_EXAMPLE: '!rw replace https://discord.com/OLD https://discord.com/NEW'
            }
        ]
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rw'])
    async def rewrite(self, ctx, command: str = None, *args):
        clowncil = find(lambda r: r.name == 'Clowncil', ctx.message.guild.roles)
        if not ctx.author.guild_permissions.administrator and not clowncil in ctx.author.roles:
            await ctx.send(embed=create_basic_embed("Sorry, you aren't authorized to use that command!", EMOJI_ERROR))
        elif command == 'post' and len(args) == 2:
            await Rewrite.post(ctx, args[0], args[1])
        elif command == 'edit' and len(args) == 1:
            await Rewrite.edit(ctx, args[0])
        elif command == 'replace' and len(args) == 2:
            await Rewrite.replace(ctx, args[0], args[1])
        else:
            prefix = get_prefix(self.bot, ctx.message)
            await ctx.send(embed=create_help_embed(self.help, prefix))

    @staticmethod
    async def post(ctx, message_link, channel_str):
        message = await fetch_message(ctx, message_link)
        channel = get_channel(ctx, channel_str)
        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        am = discord.AllowedMentions(
            roles=False,
        )

        if not channel:
            await ctx.send(embed=create_basic_embed('Please specify a valid channel!', EMOJI_ERROR))
        elif not channel.permissions_for(bot_member).send_messages:
            await ctx.send(embed=create_basic_embed("I'm not allowed to post in that channel!", EMOJI_ERROR))
        elif await Rewrite.check_postable_message(ctx, message):
            await channel.send(message.content, allowed_mentions=am)
            await ctx.send(
                embed=create_basic_embed(f'Message successfully posted to {channel.mention}.', EMOJI_SUCCESS))

    @staticmethod
    async def edit(ctx, message_link):
        message = await fetch_message(ctx, message_link)
        if await Rewrite.check_editable_message(ctx, message):
            await ctx.send(embed=create_basic_embed(TEXT_FORMAT_TEMPLATE.format(message.content), EMOJI_INFO))

    @staticmethod
    async def replace(ctx, old_message_link, new_message_link):
        old_message = await fetch_message(ctx, old_message_link)
        new_message = await fetch_message(ctx, new_message_link)

        if (await Rewrite.check_editable_message(ctx, old_message)
                and await Rewrite.check_postable_message(ctx, new_message)):
            await old_message.edit(content=new_message.content, embed=None)
            await ctx.send(embed=create_basic_embed(
                f'Message successfully edited. [Check it out!]({old_message_link})', EMOJI_SUCCESS))

    @staticmethod
    async def check_postable_message(ctx, message):
        if not message:
            await ctx.send(embed=create_basic_embed(TEXT_INVALID_MESSAGE_LINK, EMOJI_ERROR))
        elif message.author.bot:
            await ctx.send(embed=create_basic_embed(TEXT_ONLY_HUMANS, EMOJI_ERROR))
        elif len(message.content) >= 2000:
            await ctx.send(embed=create_basic_embed(TEXT_TOO_LONG, EMOJI_ERROR))
        else:
            return True

    @staticmethod
    async def check_editable_message(ctx, message):
        if not message:
            await ctx.send(embed=create_basic_embed(TEXT_INVALID_MESSAGE_LINK, EMOJI_ERROR))
        elif message.author.id != ctx.bot.user.id:
            await ctx.send(embed=create_basic_embed('I can only edit messages that I posted!', EMOJI_ERROR))
        # elif message.embeds:
        #     await ctx.send(
        #         embed=create_basic_embed("I can only edit messages that don't have any embeds!", EMOJI_ERROR))
        else:
            return True


def setup(bot):
    bot.add_cog(Rewrite(bot))
