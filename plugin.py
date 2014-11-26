###
# Copyright (c) 2014, Julian Paul Glass
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
from supybot.commands import getChannel
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import (PluginInternationalization,
                            internationalizeDocstring)
    _ = PluginInternationalization('NTopic')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

#Plugin specific imports
import os
import sqlite3
import sys
from .local.queries import *
from .local.database import *


def checkDirection(irc, msg, args, state):
    if args[0] != '--reverse':
        err = '%s is not a valid option for command \"ntopic cycle\"'
        state.error(_(format(err, args[0])))
    state.args.append(args.pop(0))

def canChangeTopic(irc, msg, args, state):
    assert not state.channel 
    callConverter('channel', irc, msg, args, state) 
    callConverter('inChannel', irc, msg, args, state) 
    c = irc.state.channels[state.channel] 
    if 't' in c.modes and not c.isHalfopPlus(irc.nick): 
        state.error(format(_('I can\'t change the topic, I\'m not (half)opped ' 
                           'and %s is +t.'), state.channel), Raise=True) 

addConverter('canChangeTopic', canChangeTopic)
addConverter('checkDirection', checkDirection)

class NTopic(callbacks.Plugin):
    """Add the help for "@plugin help NTopic" here
    This should describe *how* to use this plugin."""
    def __init__(self, irc):
        super(NTopic, self).__init__(irc)
        self._cache = []
        self.conn = None
        self.DBFilename = '/tmp/NTopic.db'
        self.connectDB(self.DBFilename)

    def connectDB(self, filename):
        conn = sqlite3.connect(filename, isolation_level='DEFERRED')
        if sys.version_info[0] < 3:
            conn.text_factory = str
        cursor = conn.cursor()
        try:
            cursor.execute(QCheckDB)
            self.last_access = cursor.fetchone()[0]
        except:
            for t in QSchema:
                cursor.execute(t)
            conn.commit()
        finally:
            conn.rollback()
        self.initDB(cursor)
        conn.commit()
        self.conn = conn

    @staticmethod
    def initDB(cursor):
        cursor.execute(QUpdateDB)

    def getGroupID(self, name):
        if not self.conn:
            return False
        cursor = self.conn.cursor()
        try:
            cursor.execute(format(QGetGroupID, name))
            value = cursor.fetchone()[0]
        except:
            cursor.execute(format(QSetGroupName, name))
            value = cursor.fetchone()[0]
        finally:
            self.conn.commit()
        return value

    @internationalizeDocstring
    def add(self, irc, msg, args, channel, name, text):
        """[<channel>] <name> <topic>
        Adds a topic group <name> for <channel>. <topic> is set to the topic
        text. <channel> is only necessary if the message isn't sent within
        the channel itself.
        """
        r = DBAddTopic(self.conn, msg.prefix, channel, name, text)
        if r[0] is False:
            raise irc.error(format('%s: Topic with id \"%s\" already exists.'\
                    ' To set it to the current topic use the \"set\"'\
                    ' command.',r[2],r[1]))
        else:
            irc.replySuccess()
    add = wrap(add, ['canChangeTopic', 'somethingWithoutSpaces', 'text'])
    
    @internationalizeDocstring
    def remove(self, irc, msg, args, channel, name):
        """[<channel>] <name>
        Removes a topic group <name> for <channel>.  <channel> is only 
        necessary if the message isn't sent within the channel itself.

        """
        irc.replySuccess()
    remove = wrap(remove, ['canChangeTopic', 'somethingWithoutSpaces'])
    
    @internationalizeDocstring
    def change(self, irc, msg, args, channel, name, re):
        """[<channel>] <name> <regexp>
        Changes topic group text on <channel> according to the regular
        expression <regexp>. <regexp> is in the format
        s/regexp/replacement/flags.  <channel> is only necessary if the 
        message isn't sent within the channel itself.
        """
        irc.replySuccess()
    change = wrap(change, ['canChangeTopic', 'somethingWithoutSpaces', 
        'regexpReplacer'])

    @internationalizeDocstring
    def set(self, irc, msg, args, channel, name):
        """[<channel>] <name>
        Sets current topic group <name> to channel topic.  <channel> is only 
        necessary if the message isn't sent within the channel itself.
        """
        irc.replySuccess()
    set = wrap(set, ['canChangeTopic', 'somethingWithoutSpaces'])

    @internationalizeDocstring
    def order(self, irc, msg, args, channel, name, order):
        """[<channel>] <name> <order>
        Set the order of topic group <name> to <order> number. <channel> is 
        only necessary if the message isn't sent within the channel itself.
        """
        irc.replySuccess()
    order = wrap(order, ['canChangeTopic', 'somethingWithoutSpaces', 'float'])
    
    @internationalizeDocstring
    def cycle(self, irc, msg, args, channel, direction='forward'):
        """[<channel>] [--reverse]
        Cycle through topic groups with optional --reverse.  <channel> is 
        only necessary if the message isn't sent within the channel itself.
        """
        irc.replySuccess()
    cycle = wrap(cycle, ['canChangeTopic', optional('checkDirection')])

    @internationalizeDocstring
    def bind(self, irc, msg, args, channel, name):
        """<channel> <name>
        bind (share) topic group <name> to another <channel>. 
        """
        irc.replySuccess()
    bind = wrap(bind, ['validChannel', 'somethingWithoutSpaces'])

    @internationalizeDocstring
    def stats(self, irc, msg, args):
        """Show database stats for NTopic."""
        irc.replySuccess()
    stats = wrap(stats)

Class = NTopic

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
