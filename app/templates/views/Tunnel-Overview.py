# Tunnel

## Model

#


class TunnelBase(BaseModel):
    id: str = None
    name: Optional[str] = None
    description: Optional[str] = None
    child_blocks: List[Block] = []


class TunnelCreate(TunnelBase):
    name: str
    description: str


class Tunnel_Read_Update_Delete(TunnelBase):
    id: str


## View
# Card View
"""
<div id="pallete-content" class="grid-container">
  <button
    hx-get="/tunnels/new"
    hx-target="#pallete"
    hx-push-url="true"
    type="button"
  >
    New Tunnel
  </button>
  {% if tunnels %} {% for tunnel in tunnels %}
  <div class="card">
    <div
      class="content"
      hx-get="/tunnels/{{ tunnel.id }}"
      hx-target="#pallete"
      hx-push-url="true"
    >
      <span class="material-symbols-outlined"> account_tree </span>
      <span class="text-block">
        <h6 class="block-name">{{ tunnel.name }}</h6>
        <p class="block-description">{{ tunnel.description }}</p>
      </span>
    </div>
  </div>
  {% endfor %} {% else %}
  <h3>No Tunnels Found</h3>
  {% endif %}
</div>
<!-- Form View -->
<!-- For Creating new Tunnel and Updating existing Tunnel -->
<div id="pallete-content" class="grid-container form-view">
  <form
    action="/tunnels/create"
    hx-boost="true"
    hx-target="#pallete"
    method="post"
    class="card"
  >
    <h3>Tunnel!</h3>
    <div class="mb-3">
      <label for="name" class="form-label">Name</label>
      <input type="text" name="name" class="form-control" id="name" />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea
        class="form-control"
        id="description"
        rows="5"
        name="description"
      ></textarea>
    </div>

    <div class="mb-3">
      <button type="submit" class="btn">Save Tunnel</button>
    </div>
  </form>
</div>
"""

## Controller

prefix = "/tunnels"
db = TunnelOps()


@router.get("/new", response_class=HTMLResponse)
async def new(request: Request):
    """
    Bring up the form to create a new Tunnel.
    """
    context = {
        "request": request,
    }

    return templates.TemplateResponse("views/tunnel-form.html", context)


@router.post("/create", response_class=HTMLResponse)
async def create_tunnel(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    hx_request: Optional[str] = Header(None),
):
    """Create a new Tunnel."""

    db_create_tunnel = await db.create(TunnelCreate(name=name, description=description))

    context = {
        "request": request,
        "tunnel": db_create_tunnel,
    }

    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


@router.get("/", response_class=HTMLResponse)
async def get_all_tunnels(request: Request, hx_request: Optional[str] = Header(None)):
    """
    Read all Tunnels in the database.
    """
    db_get_all_tunnels = await db.all()

    context = {
        "request": request,
        "tunnel": db_get_all_tunnels,
    }
    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


@router.get("/{id}", response_class=HTMLResponse)
async def get_tunnel(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """
    Get a single Tunnel from the database.
    """
    db_get_tunnel = await db.read(Tunnel_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "tunnel": db_get_tunnel,
    }
    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


@router.get("/edit/{id}/", response_class=HTMLResponse)
async def edit_tunnel(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """
    Bring up the form to edit a single Tunnel in the database.
    """
    db_edit_tunnel = await db.read(Tunnel_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "tunnel": db_edit_tunnel,
    }
    if hx_request:
        return templates.TemplateResponse("components/tunnel-form.html", context)

    return templates.TemplateResponse("base.html", context)


@router.post("/update/{id}", response_class=HTMLResponse)
async def update_tunnel(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """
    Update a single Tunnel in the database.
    """
    db_update_tunnel = await db.update(Tunnel_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "tunnel": db_update_tunnel,
    }
    if hx_request:
        return templates.TemplateResponse("components/tunnel-form.html", context)

    return templates.TemplateResponse("base.html", context)


@router.delete("/delete/{tunnel_id}", response_class=HTMLResponse)
async def delete_tunnel(
    request: Request, id: str, hx_request: Optional[str] = Header(None)
):
    """
    Delete a single Tunnel from the database.
    """
    db_delete_tunnel = await db.delete(Tunnel_Read_Update_Delete(id=id))

    context = {
        "request": request,
        "tunnel": db_delete_tunnel,
    }
    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


# DB Services


@dataclass
class TunnelOps:
    db_url: str = db_config["url"]
    db_ns: str = db_config["ns"]
    db_dbt: str = db_config["dbt"]

    @classmethod
    async def create(cls, create: TunnelCreate):
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
            newTunnel = await db.create("my_new_tunnel", create)
            results = await db.select("newTunnel")
            return results

    @classmethod
    async def all(cls):
        """
        Route to get all Blocks from the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.select("tunnel")
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
    async def update(cls, id: str, update: Tunnel_Read_Update_DeleteUpdate):
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
            updateTunnel = await db.update("id", update)
            results = await db.select("updateTunnel")
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
            deleteTunnel = await db.delete("id")
            results = await db.select(f"{deleteTunnel.name} successfully deleted.")
            return results


## Tunnel Modules


class Tunnel(TunnelBase):
    """
    Represents a tunnel of blocks.
    """

    def add_block(self, block: Block) -> None:
        """
        Add a block to the tunnel by populating tunnel_id field of the block,
        then adding the block to the tunnel's child_blocks list or creating
        a relationship between the block and tunnel in the db.???
        """

    def connect_blocks(self, source_block_name: str, target_block_name: str) -> None:
        """
        Connect two blocks in the tunnel by creting a relationship between them in db.
        """

    def update_connection(self, source_block_name: str, target_block_name: str) -> None:
        """
        Update the connection between two blocks in the tunnel by updating the relationship between them in db.
        """

    def delete_connection(self, source_block_name: str, target_block_name: str) -> None:
        """
        Delete the connection between two blocks in the tunnel by deleting the relationship between them in db.
        """

    def validate_tunnel(self) -> None:
        """
        Validate the tunnel by checking that there are no circular references.
        """

    # figure out the best way to send data through the tunnel according
    # to the blocks connections perhaps using a tool like Celary or
    # by implementing a callback function that is called when a block
    # finishes processing data_input

    async def run(self, data: Any) -> None:
        """
        Run the tunnel with the given data.
        """
        await asyncio.gather(data)
