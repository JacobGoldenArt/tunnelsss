# Block:

## Model (Pydantic):


class BlockBase(BaseModel):
    id: str = None
    name: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    tunnel_id: str = None
    source_block_id: str = None
    child_blocks: List[Block] = []


class BlockCreate(BlockBase):
    name: str
    type: str
    model: str = "gpt-3.5-turbo"
    tunnel_id: str


class Block_Read_Update_Delete(BlockBase):
    id: str


## View - HTML/JINJA2 Template:
# Card View
"""
    <div class="card" hx-get="/blocks/update/{{ block.id }}" hx-target="#pallete" hx-push-url="true">
        <div class="content" data-id="{{ block.id }}" data-tunnel-id="{{ block.tunnel_id }}">
            <span class="material-symbols-outlined">
                toast
            </span>
            <span class="text-block">
                <h6 class="block-name">{{ block.name }}</h6>
                <p class="block-type">{{ block.type }}</p>
                <p class="block-model">{{ block.model }}</p>
                <p class="block-description">{{ block.description }}</p>
            </span>
        </div>
    </div>
"""
# Form View
"""
<form>
    <div class="form-group">
        <label for="block-name">Name</label>
        <input type="text" class="form-control" id="block-name" placeholder="Enter name" value="{{ block.name }}">
    </div>
    <div class="form-group">
        <label for="block-type">Type</label>
        <select>
            <option value="text">
            <option value="image">
            <!-- etc... -->
        </select>
    <div class="form-group">
        <label for="block-model">Model</label>
        <select>
            <option value="gpt-3.5-turbo">
            <option value="gpt-4">
            <!-- etc... -->
        </select>
    </div>
    <div class="form-group">
        <label for="block-description">Description</label>
        <input type="text" class="form-control" id="block-description" placeholder="Enter description" value="{{ block.description }}">
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
         <p>or</p>
    <!-- figure out how to only show delete button when the user types delete into #delete-block input
    can I do this with HTMX and or JINJA? -->
    <input type="text" id="delete-block" placeholder="type delete to delete block">
    <button type="submit" class="btn btn-danger hidden">Delete</button>
</form>
"""

## Controller:

prefix = "/blocks"
db = BlockOps()


@app.get("/new", response_class=HTMLResponse)
async def new(request: Request):
    """
    Bring up the form to create a new Block.
    """
    context = {
        "request": request,
    }

    return templates.TemplateResponse("views/block-form.html", context)


@app.post("/create", response_class=HTMLResponse)
async def create_block(
    request: Request,
    name: str = Form(...),
    type: str = Form(...),
    model: str = Form(...),
    description: str = Form(...),
    parent_block_id: str = Form(...),
    hx_request: Optional[str] = Header(None),
):
    """Create a new Block in the database."""

    db_create_block = await db.create(
        BlockCreate(
            name=name,
            type=type,
            model=model,
            description=description,
            tunnel_id=parent_block_id,
        )
    )

    context = {
        "request": request,
        "block": db_create_block,
    }

    if hx_request:
        return templates.TemplateResponse("components/block.html", context)

    return templates.TemplateResponse("base.html", context)


@app.get("/", response_class=HTMLResponse)
async def get_all_blocks(request: Request, hx_request: Optional[str] = Header(None)):
    """
    Read all Blocks from the database.
    """
    db_get_all_blocks = await db.all()

    context = {
        "request": request,
        "block": db_get_all_blocks,
    }

    if hx_request:
        return templates.TemplateResponse("components/block.html", context)

    return templates.TemplateResponse("base.html", context)


@app.get("/{id}", response_class=HTMLResponse)
async def get_block(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """Get a single Block from the database."""
    db_get_block = await db.get(Block_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "block": db_get_block,
    }
    if hx_request:
        return templates.TemplateResponse("components/block.html", context)

    return templates.TemplateResponse("block.html", context)


@router.get("/edit/{id}/", response_class=HTMLResponse)
async def edit_tunnel(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """
    Bring up the form to edit a single Block in the database.
    """
    db_edit_block = await db.read(Block_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "tunnel": db_edit_block,
    }
    if hx_request:
        return templates.TemplateResponse("components/block-form.html", context)

    return templates.TemplateResponse("base.html", context)


@app.post("/update/{id}", response_class=HTMLResponse)
async def update_block(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """Update a single Block in the database."""

    db_edit_block = await db.update(Block_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "block_edit": db_edit_block,
    }

    if hx_request:
        return templates.TemplateResponse("components/block-form.html", context)

    return templates.TemplateResponse("base.html", context)


@app.delete("/delete/{id}", response_class=HTMLResponse)
async def delete_block(request: Request, id: str):
    """Delete a single Block from the database."""

    db_delete_block = await db.delete(Block_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "block": db_delete_block,
    }

    if hx_request:
        return templates.TemplateResponse("components/block.html", context)

    return templates.TemplateResponse("base.html", context)


## DB Services:


@dataclass
class BlockOps:
    db_url: str = db_config["url"]
    db_ns: str = db_config["ns"]
    db_dbt: str = db_config["dbt"]

    @classmethod
    async def create(cls, create: BlockCreate):
        """
        Route to create a new Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)

            # await db.query(
            #     """
            #     LET $myID = rand::uuid();
            #     CREATE blocks SET name = $myblock.name,
            #     type = $myblock.type,
            #     model = $myblock.model,
            #     description = $myblock.description,
            #     id = $myID,
            #     tunnel_id = $myblock.tunnel_id;

            #     UPDATE $myblock.tunnel_id SET child_blocks = [RETURN (SELECT * from blocks)]
            #     """,
            #     {"myblock": create},
            # )
            newBlock = await db.create("my_new_block", create)
            results = await db.select("newBlock")
            return results

    @classmethod
    async def all(cls):
        """
        Route to get all Blocks from the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.select("block")
            return results

    @classmethod
    async def get(cls, id: str):
        """
        Route to get a specific Block from the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.select("id")
            return results

    @classmethod
    async def update(cls, id: str, update: Block_Read_Update_Delete):
        """
        Route to update a specific Block in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            # await db.query(
            #     """
            #     UPDATE blocks SET name = $myblock.name,
            #     type = $myblock.type,
            #     model = $myblock.model,
            #     description = $myblock.description
            #     WHERE id = $myblock.id
            #     """,
            #     {"myblock": update},
            # )
            updateBlock = await db.update("id", update)
            results = await db.select("updateBlock")
            return results

    @classmethod
    async def delete(cls, id: str):
        """
        Route to delete a specific Block from the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            # await db.query(
            #     """
            #     LET $myblock = (SELECT * FROM blocks WHERE id = $myblock.id);
            #     DELETE $myblock;
            #     UPDATE $myblock.tunnel_id SET child_blocks = [RETURN (SELECT * from blocks)]
            #     """,
            #     {"myblock": block_id},
            # )
            deleteBlock = await db.delete("id")
            results = await db.select(f"{deleteBlock.name} successfully deleted.")
            return results


## Block Module


@dataclass
class Block(BlockBase):
    """
    Base Class for All Blocks
    """
    # Do I need to list all the fields here or can I just use the BlockBase class?
    id: str = None
    name: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    tunnel_id: str = None
    source_block_id: str = None
    child_blocks: List[Block] = []

    data: Optional[Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process method for this block class.
        """
        await asyncio.sleep(5)
        return {self.name: data}

    @classmethod
    async def input(self, data: Dict[str, Any]) -> None:
        """
        Inputs data into the block.
        """
        self.data = data
        processed_data = await self.process(self.data)
        self.processed.set(processed_data)

    @classmethod
    async def output(self) -> Dict[str, Any]:
        """
        Outputs processed data from the block to child_blocks.
        """
        for block in self.child_blocks:
            await block.input(self.processed.get())
        return self.processed.get()


@dataclass
class TestProcess:
    """
    This is a test process to test block functionality.
    """

    async def test_process(self, data: str) -> str:
        """
        Process the data and return the processed data.
        """
        return f"Processed {data}"


class TestBlock(Block):
    """
    This is a block in its simplest form to test block functionality.
    """

    type: Optional[str] = field(default=None)

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the data and return the processed data.
        """
        data_input: str = data.get(self.name, "")
        process_data = TestProcess()
        generated_text = await process_data.test_process(data_input)
        logger.info(f"{self.name} generated the following text: {generated_text}")
        return {self.name: generated_text}
