# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function
import six
import unittest
import os
import argparse
import sys

from azclishell import __version__
import azclishell._dump_help
import azclishell.configuration
from azclishell.gather_commands import GatherCommands
from azclishell.app import Shell
from azclishell.az_completer import AzCompleter
from azclishell.az_lexer import AzLexer
from azclishell.util import default_style

import azclishell.command_tree as tree

from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completion
from prompt_toolkit.history import FileHistory

from azure.cli.core.application import APPLICATION
from azure.cli.core._session import ACCOUNT, CONFIG, SESSION
from azure.cli.core._environment import get_config_dir as cli_config_dir
from azure.cli.core.commands.client_factory import ENV_ADDITIONAL_USER_AGENT

AZCOMPLETER = AzCompleter(GatherCommands())
SHELL_CONFIGURATION = azclishell.configuration.CONFIGURATION


class CompletionTest(unittest.TestCase):
    """ tests the shell specific gestures """
    def init1(self):
        """ a variation of initializing """

        os.environ[ENV_ADDITIONAL_USER_AGENT] = 'AZURECLISHELL/' + __version__

        style = default_style()

        azure_folder = cli_config_dir()
        if not os.path.exists(azure_folder):
            os.makedirs(azure_folder)

        config = SHELL_CONFIGURATION
        shell_config_dir = azclishell.configuration.get_config_dir

        if config.BOOLEAN_STATES[config.config.get('DEFAULT', 'firsttime')]:
            print("When in doubt, ask for 'help'")
            config.firsttime()

        self.shell_app = Shell(
            completer=AZCOMPLETER,
            lexer=AzLexer,
            history=FileHistory(
                os.path.join(shell_config_dir(), config.get_history())),
            app=APPLICATION,
            styles=style
        )

    def test_prompt(self):
        """ tests the prompt methods """
        self.init1()
        # description, examples = self.shell_app.generate_help_text('no')
        self.assertEquals(self.shell_app.cli.current_buffer.text, u'')
        # self.assertEquals(examples, '')


if __name__ == '__main__':
    unittest.main()
