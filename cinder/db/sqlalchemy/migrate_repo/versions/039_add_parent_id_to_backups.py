# Copyright 2014 TrilioData, Inc
# Copyright (c) 2015 EMC Corporation
# All Rights Reserved.
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

from oslo_log import log as logging
from sqlalchemy import Column, MetaData, String, Table

from cinder.i18n import _LE

LOG = logging.getLogger(__name__)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    backups = Table('backups', meta, autoload=True)
    parent_id = Column('parent_id', String(length=36))

    try:
        backups.create_column(parent_id)
        backups.update().values(parent_id=None).execute()
    except Exception:
        LOG.error(_LE("Adding parent_id column to backups table failed."))
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    backups = Table('backups', meta, autoload=True)
    parent_id = backups.columns.parent_id

    try:
        backups.drop_column(parent_id)
    except Exception:
        LOG.error(_LE("Dropping parent_id column from backups table failed."))
        raise
