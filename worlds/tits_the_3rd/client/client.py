import asyncio
import hashlib
import io
import os
from pathlib import Path
import pkgutil
import shutil
import subprocess
import time
import queue
from typing import Optional, Set
import zipfile

import bsdiff4
import colorama

from NetUtils import ClientStatus, NetworkItem
from settings import get_settings
from worlds.tits_the_3rd.locations import get_location_id
from worlds.tits_the_3rd.items import get_item_id
from worlds.tits_the_3rd.names.location_name import LocationName
from worlds.tits_the_3rd.names.item_name import ItemName
from worlds.tits_the_3rd.util import load_file

from .memory_io import TitsThe3rdMemoryIO
from CommonClient import (
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)


class TitsThe3rdContext(CommonContext):
    """Trails in the Sky the 3rd Context"""

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)
        self.game = "Trails in the Sky the 3rd"
        self.items_handling = 0b111  # Fully Remote
        self.game_interface = None
        self.world_player_identifier: bytes = b"\x00\x00\x00\x00"
        self.location_ids = None
        self.location_name_to_ap_id = None
        self.location_ap_id_to_name = None
        self.item_name_to_ap_id = None
        self.item_ap_id_to_name = None
        self.last_received_item_index = -1
        self.non_local_locations: Set[int] = set()
        self.non_local_locations_initiated = False

        self.items_to_be_sent_notification = queue.Queue()

        self.critical_section_lock = asyncio.Lock()

    def init_game_interface(self):
        logger.info("Initiating Game Interface")
        if not self.install_game_mod():
            raise Exception("Error Installing Game Mod")
        logger.info("Finish installing game mod")
        # self.install_dt_patch() #TODO: implement this when we actually have something for this
        self.game_interface = TitsThe3rdMemoryIO(self.exit_event)

    def install_game_mod(self):
        game_dir = Path(get_settings().tits_the_3rd_options.game_installation_path)
        files_in_game_dir = os.listdir(game_dir)
        if not "ed6_win3_DX9.exe" in files_in_game_dir:
            raise Exception("Incorrect game directory")

        lb_ark_folder = game_dir / "data"
        scena_temp_folder = lb_ark_folder / "ED6_DT21_BASE"
        game_mod_folder = lb_ark_folder / "ED6_DT21"
        os.makedirs(lb_ark_folder, exist_ok=True)
        if "player.txt" in os.listdir(lb_ark_folder):  # TODO: Check for player id + seed
            return True

        if os.path.exists(game_mod_folder):  # Remove previously installed mod for a clean install
            shutil.rmtree(game_mod_folder)

        if not "factoria.exe" in files_in_game_dir:
            raise Exception("factoria.exe not found. Please install factoria from https://github.com/Aureole-Suite/Factoria/releases/tag/v1.0")

        # Create the temporary base game folder
        if not os.path.exists(scena_temp_folder):
            factoria_command = f'"{game_dir/ "factoria.exe"}" --output "{scena_temp_folder}" "{game_dir / "ED6_DT21.dir"}"'
            subprocess.run(factoria_command, shell=True)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for file in sorted(os.listdir(scena_temp_folder)):
                if file.endswith("._sn"):
                    zip_file.write(scena_temp_folder / file, arcname=file)

        zip_buffer.seek(0)
        patch = load_file("data/tits3rd_basepatch.bsdiff4")
        output_data = bsdiff4.patch(zip_buffer.read(), patch)
        output_buffer = io.BytesIO(output_data)
        with zipfile.ZipFile(output_buffer, "r") as output_file:
            os.makedirs(game_mod_folder, exist_ok=True)
            output_file.extractall(game_mod_folder)
        return True

    def reset_client_state(self):
        """
        Resets the client state to the initial state.
        """
        self.game_interface = None
        self.world_player_identifier = b"\x00\x00\x00\x00"
        self.location_ids = None
        self.location_name_to_ap_id = None
        self.location_ap_id_to_name = None
        self.item_name_to_ap_id = None
        self.item_ap_id_to_name = None
        self.last_received_item_index = -1
        self.items_to_be_sent_notification = queue.Queue()
        self.locations_checked = set()
        self.non_local_locations = set()
        self.non_local_locations_initiated = False

    async def server_auth(self, password_requested: bool = False):
        """Wrapper for login."""
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            # if we dont have the seed name from the RoomInfo packet, wait until we do.
            while not self.seed_name:
                time.sleep(1)
            # Hash the seed name + player name and take the first 4 bytes as the world player identifier.
            self.world_player_identifier = f"{self.seed_name}-{self.auth}"
            self.world_player_identifier = (hashlib.sha256(self.world_player_identifier.encode()).digest())[:4]
            self.location_ids = set(args["missing_locations"] + args["checked_locations"])
            self.locations_checked = set(args["checked_locations"])

            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": self.location_ids}]))

        elif cmd == "LocationInfo":
            if not self.non_local_locations_initiated:
                for item in [NetworkItem(*item) for item in args["locations"]]:
                    if self.player_names[item.player] != self.slot_info[self.slot].name:
                        self.non_local_locations.add(item.location)
                self.non_local_locations_initiated = True

        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

        elif cmd == "DataPackage":
            if not self.location_ids:
                # Connected package not recieved yet, wait for datapackage request after connected package
                return
            self.location_name_to_ap_id = args["data"]["games"]["Trails in the Sky the 3rd"]["location_name_to_id"]
            self.location_name_to_ap_id = {name: loc_id for name, loc_id in self.location_name_to_ap_id.items() if loc_id in self.location_ids}
            self.location_ap_id_to_name = {v: k for k, v in self.location_name_to_ap_id.items()}
            self.item_name_to_ap_id = args["data"]["games"]["Trails in the Sky the 3rd"]["item_name_to_id"]
            self.item_ap_id_to_name = {v: k for k, v in self.item_name_to_ap_id.items()}

    def client_recieved_initial_server_data(self):
        """
        This returns true if the client has finished the initial conversation with the server.
        This means:
            - Authenticated with the server (self.auth is set)
            - RoomInfo package recieved (self.seed_name is set)
            - World player identifier is calculated based on the seed and player name (self.world_player_identifier is set)
        """
        return self.auth and self.seed_name and self.world_player_identifier and self.non_local_locations_initiated

    async def give_item(self):
        self.last_received_item_index = self.game_interface.read_last_item_receive_index()
        try:
            current_item = self.items_received[self.last_received_item_index + 1]
        except IndexError:
            current_item = None

        result = False

        if current_item:
            item_id = current_item.item
            # Special case where we don't actually want to give anything but just acknowledge it
            if item_id is None or item_id >= 500000:
                result = True
            # Unlock location
            elif get_item_id(ItemName.area_min_id) <= item_id <= get_item_id(ItemName.area_max_id):
                result = self.game_interface.unlock_area(item_id - get_item_id(ItemName.area_min_id))
            # Unlock character
            elif get_item_id(ItemName.character_min_id) <= item_id <= get_item_id(ItemName.character_max_id):
                result = self.game_interface.unlock_character(item_id - get_item_id(ItemName.character_min_id))
            # Give Mira
            elif get_item_id(ItemName.mira_min_id) <= item_id <= get_item_id(ItemName.mira_max_id):
                result = self.game_interface.give_mira(item_id - get_item_id(ItemName.mira_min_id))
            # Give lower element sepith
            elif get_item_id(ItemName.lower_elements_sepith_min_id) <= item_id <= get_item_id(ItemName.lower_elements_sepith_max_id):
                result = self.game_interface.give_low_sepith(item_id - get_item_id(ItemName.lower_elements_sepith_min_id))
            # Give higher element sepith
            elif get_item_id(ItemName.higher_elements_sepith_min_id) <= item_id <= get_item_id(ItemName.higher_elements_sepith_max_id):
                result = self.game_interface.give_high_sepith(item_id - get_item_id(ItemName.higher_elements_sepith_min_id))
            # Give Recipe
            elif get_item_id(ItemName.recipe_min_id) <= item_id <= get_item_id(ItemName.recipe_max_id):
                result = self.game_interface.give_recipe(item_id - get_item_id(ItemName.recipe_min_id))
            # Just a normal item
            else:
                result = self.game_interface.give_item(item_id, 1)
            if result:
                while self.game_interface.is_in_event():
                    await asyncio.sleep(0.1)
                self.game_interface.write_last_item_receive_index(self.last_received_item_index + 1)
            await asyncio.sleep(0.1)

    async def send_item(self):
        if not self.items_to_be_sent_notification.empty():
            item_to_be_sent = self.items_to_be_sent_notification.get()
            item_id = 50000 + int(item_to_be_sent)  # Make that non native item be 50000 + location_id
            result = self.game_interface.send_item()
            while self.game_interface.is_in_event():
                await asyncio.sleep(0.1)

    async def wait_for_ap_connection(self):
        """
        This method waits until the client finishes the initial connection with the server.
        See client_recieved_initial_server_data for wait requirements
        """
        if self.client_recieved_initial_server_data():
            return
        logger.info("Waiting for connect from server...")
        while not self.client_recieved_initial_server_data() and not self.exit_event.is_set():
            await asyncio.sleep(1)
        if not self.exit_event.is_set():
            # wait an extra second to process data
            await asyncio.sleep(1)
            logger.info("Received initial data from server!")

    async def check_for_locations(self):
        for location_id in self.location_ids:
            if location_id in self.locations_checked:
                continue
            if self.game_interface.read_flag(location_id):
                if not self.game_interface.should_send_and_recieve_items(self.world_player_identifier):
                    return
                if location_id == get_location_id(LocationName.chapter1_boss_defeated):
                    # Chapter 1 boss defeated
                    self.finished_game = True
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                self.locations_checked.add(location_id)
                await self.send_msgs([{"cmd": "LocationChecks", "locations": self.locations_checked}])
                if location_id in self.non_local_locations:
                    self.items_to_be_sent_notification.put(location_id)

async def tits_the_3rd_watcher(ctx: TitsThe3rdContext):
    """
    Client loop, watching the Trails in the Sky the 3rd game process.
    Handles game hook attachments, checking locations, giving items, calling scena methods, etc.

    Args:
        ctx (TitsThe3rdContext): The Trails in the Sky the 3rd context instance.
    """
    await ctx.wait_for_ap_connection()
    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.1)

        if not ctx.server:
            # client disconnected from server
            ctx.reset_client_state()
            await ctx.wait_for_ap_connection()
            continue

        if not ctx.game_interface:
            ctx.init_game_interface()

        if not ctx.game_interface.is_connected():
            await ctx.game_interface.connect()
            continue

        if ctx.game_interface.should_write_world_player_identifier():
            logger.info(f"Game Start Dectected. Setting up AP Verification Hook")
            ctx.game_interface.write_world_player_identifier(ctx.world_player_identifier)
            logger.info(f"AP Verification Hook Set. You can now save and resume the game for this AP Seed")
            continue

        try:
            if ctx.exit_event.is_set():
                break
            if ctx.game_interface.should_send_and_recieve_items(ctx.world_player_identifier) and ctx.client_recieved_initial_server_data():
                await ctx.check_for_locations()

            if (
                ctx.game_interface.is_valid_to_receive_item()
                and ctx.game_interface.should_send_and_recieve_items(wpid=ctx.world_player_identifier)
                and ctx.client_recieved_initial_server_data()
            ):
                await ctx.send_item()

            if (
                ctx.game_interface.is_valid_to_receive_item()
                and ctx.game_interface.should_send_and_recieve_items(wpid=ctx.world_player_identifier)
                and ctx.client_recieved_initial_server_data()
            ):
                await ctx.give_item()

        except Exception as err:
            logger.warning("*******************************")
            logger.warning("Encountered error. Please post a message to the thread on the AP discord: https://discord.com/channels/731205301247803413/1217595862872490065")
            logger.warning("*******************************")
            logger.exception(str(err))
            # attempt to reconnect at the top of the loop
            continue


def launch():
    """
    Launch a client instance (wrapper / args parser)
    """

    async def main(args):
        """
        Launch a client instance (threaded)
        """
        ctx = TitsThe3rdContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="TitsThe3rdServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        watcher = asyncio.create_task(tits_the_3rd_watcher(ctx), name="TitsThe3rdProgressionWatcher")
        await ctx.exit_event.wait()
        await watcher
        await ctx.shutdown()

    parser = get_base_parser(description="Trails in the Sky the 3rd Client")
    args, _ = parser.parse_known_args()

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
