from enum import StrEnum

from asynctinydb import TinyDB, Query, Document


class Migrations:
    def __init__(self, db: TinyDB):
        self.db = db
        self.migration_table = db.table('migrations')
        self.migration_query = Query()
        self.first_migration()

    async def first_migration(self):
        migration_done = await self.migration_table.search(self.migration_query.version == 1)
        if not migration_done:
            await self.db.drop_tables()
            gen_channels = self.db.table("gen_channels")
            await gen_channels.insert_multiple(
                [
                    Document(doc_id="1221208542376361985", value={"children": {}, "name": "Create Open Voice"}),
                    Document(doc_id="1221208626644127816", value={"children": {}, "name": "Create Game Comms"}),
                    Document(doc_id="1221208915270697022", value={"children": {}, "name": "Create Ask To Join"})
                ]
            )
            await self.migration_table.insert({"version": 1})
