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

from oslo_log import log as logging
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy import MetaData, String, Table, UniqueConstraint

from cinder.i18n import _LE

LOG = logging.getLogger(__name__)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    # New table
    initiator_data = Table(
        'driver_initiator_data', meta,
        Column('created_at', DateTime(timezone=False)),
        Column('updated_at', DateTime(timezone=False)),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('initiator', String(length=255), index=True, nullable=False),
        Column('namespace', String(length=255), nullable=False),
        Column('key', String(length=255), nullable=False),
        Column('value', String(length=255)),
        UniqueConstraint('initiator', 'namespace', 'key'),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

    try:
        initiator_data.create()
    except Exception:
        LOG.error(_LE("Table |%s| not created!"), repr(initiator_data))
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    table_name = 'driver_initiator_data'
    initiator_data = Table(table_name, meta, autoload=True)
    try:
        initiator_data.drop()
    except Exception:
        LOG.error(_LE("%(table_name)s table not dropped"),
                  {'table_name': table_name})
        raise
