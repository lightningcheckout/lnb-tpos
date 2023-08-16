async def m001_initial(db):
    """
    Initial tposs table.
    """
    await db.execute(
        """
        CREATE TABLE tpos.tposs (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            currency TEXT NOT NULL
        );
    """
    )


async def m002_addtip_wallet(db):
    """
    Add tips to tposs table
    """
    await db.execute(
        """
        ALTER TABLE tpos.tposs ADD tip_wallet TEXT NULL;
    """
    )


async def m003_addtip_options(db):
    """
    Add tips to tposs table
    """
    await db.execute(
        """
        ALTER TABLE tpos.tposs ADD tip_options TEXT NULL;
    """
    )
    
async def m004_addwithdrawlimit(db):
    rows = [list(row) for row in await db.fetchall("SELECT * FROM tpos.tposs")]
    await db.execute("DROP TABLE tpos.tposs")
    await db.execute(
        """
        CREATE TABLE tpos.tposs (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            currency TEXT NOT NULL,
            tip_wallet TEXT NULL,
            tip_options TEXT NULL,
            withdrawlimit INTEGER DEFAULT 0,
            withdrawpin INTEGER DEFAULT 878787,
            withdrawamt INTEGER DEFAULT 0,
            withdrawtime TIMESTAMP NOT NULL DEFAULT """
        + db.timestamp_now
        + """
        );
    """
    )
    for row in rows:
        await db.execute(
            """
            INSERT INTO events.ticket (
                id,
                wallet,
                name,
                currency,
                tip_wallet,
                tip_options,
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (row[0], row[1], row[2], row[3], row[4], row[5]),
        )

async def m005_initial(db):
    """
    Initial withdaws table.
    """
    await db.execute(
        f"""
        CREATE TABLE tpos.withdaws (
            id TEXT PRIMARY KEY,
            tpos_id TEXT NOT NULL,
            amount int NOT NULL,
            claimed BOOL NOT NULL
        );
    """
    )