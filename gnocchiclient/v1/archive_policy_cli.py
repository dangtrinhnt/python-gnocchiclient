#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cliff import command
from cliff import lister
from cliff import show

from gnocchiclient import utils


class CliArchivePolicyList(lister.Lister):
    """List archive policies."""

    COLS = ('name',
            'back_window', 'definition', 'aggregation_methods')

    def take_action(self, parsed_args):
        policies = utils.get_client(self).archive_policy.list()
        if parsed_args.formatter == 'table':
            for ap in policies:
                utils.format_archive_policy(ap)
        return utils.list2cols(self.COLS, policies)


class CliArchivePolicyShow(show.ShowOne):
    """Show an archive policy."""

    def get_parser(self, prog_name):
        parser = super(CliArchivePolicyShow, self).get_parser(prog_name)
        parser.add_argument("name",
                            help="Name of the archive policy")
        return parser

    def take_action(self, parsed_args):
        ap = utils.get_client(self).archive_policy.get(
            name=parsed_args.name)
        if parsed_args.formatter == 'table':
            utils.format_archive_policy(ap)
        return self.dict2columns(ap)


def archive_policy_definition(string):
    parts = string.split(",")
    defs = {}
    for part in parts:
        attr, __, value = part.partition(":")
        if (attr not in ['granularity', 'points', 'timespan'] or
           value is None):
            raise ValueError
        defs[attr] = value
    if len(defs) < 2:
        raise ValueError
    return defs


class CliArchivePolicyWriteBase(show.ShowOne):
    def get_parser(self, prog_name):
        parser = super(CliArchivePolicyWriteBase, self).get_parser(prog_name)
        parser.add_argument("name", help="name of the archive policy")
        parser.add_argument("-d", "--definition", action='append',
                            required=True, type=archive_policy_definition,
                            metavar="<DEFINITION>",
                            help=("two attributes (separated by ',') of an "
                                  "archive policy definition with its name "
                                  "and value separated with a ':'"))
        return parser


class CliArchivePolicyCreate(CliArchivePolicyWriteBase):
    """Create an archive policy."""

    def get_parser(self, prog_name):
        parser = super(CliArchivePolicyCreate, self).get_parser(prog_name)
        parser.add_argument("-b", "--back-window", dest="back_window",
                            type=int,
                            help="back window of the archive policy")
        parser.add_argument("-m", "--aggregation-method",
                            action="append",
                            dest="aggregation_methods",
                            help="aggregation method of the archive policy")
        return parser

    def take_action(self, parsed_args):
        archive_policy = utils.dict_from_parsed_args(
            parsed_args, ['name', 'back_window', 'aggregation_methods',
                          'definition'])
        ap = utils.get_client(self).archive_policy.create(
            archive_policy=archive_policy)
        if parsed_args.formatter == 'table':
            utils.format_archive_policy(ap)
        return self.dict2columns(ap)


class CliArchivePolicyUpdate(CliArchivePolicyWriteBase):
    """Update an archive policy."""

    def take_action(self, parsed_args):
        archive_policy = utils.dict_from_parsed_args(
            parsed_args, ['definition'])
        ap = utils.get_client(self).archive_policy.update(
            name=parsed_args.name, archive_policy=archive_policy)
        if parsed_args.formatter == 'table':
            utils.format_archive_policy(ap)
        return self.dict2columns(ap)


class CliArchivePolicyDelete(command.Command):
    """Delete an archive policy."""

    def get_parser(self, prog_name):
        parser = super(CliArchivePolicyDelete, self).get_parser(prog_name)
        parser.add_argument("name",
                            help="Name of the archive policy")
        return parser

    def take_action(self, parsed_args):
        utils.get_client(self).archive_policy.delete(name=parsed_args.name)
