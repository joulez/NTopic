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

from supybot.test import *

succeed = 'The operation succeeded.'

class NTopicTestCase(ChannelPluginTestCase):
    plugins = ('NTopic', 'User')
    #def test01List(self):
    #    r = 'add, change, cycle, order, remove, and set'
    #    self.assertResponse('list NTopic', r)

    def test02Add(self):
        self.assertResponse('ntopic add test "this is a test"', succeed)

    def test03Remove(self):
        self.assertResponse('ntopic remove test',succeed)

    def test04Change(self):
        self.assertResponse('ntopic change test s/this/THIS/', succeed)

    def test05Set(self):
        self.assertResponse('ntopic set test', succeed)
    
    def test06Order(self):
        self.assertResponse('ntopic order test 1', succeed)

    def test07Cycle(self):
        fail = 'Error: --fail is not a valid option for command \"ntopic cycle\"'
        self.assertResponse('ntopic cycle', succeed)
        self.assertResponse('ntopic cycle --reverse', succeed)
        self.assertResponse('ntopic cycle --fail', fail)

    def test08Bind(self):
        self.assertError('ntopic bind #test')
        self.assertResponse('ntopic bind #test test', succeed)

    def test08Fail(self):
        self.assertError('ntopic test')

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
