# Trails in the Sky 3rd Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- [LB-ARK](https://github.com/Aureole-Suite/LB-ARK/releases) Latest Version. Put `d3dxof.dll` in the game install folder
- [Factoria](https://github.com/Aureole-Suite/Factoria/releases) Latest Version. Put `factoria.exe` in the game install folder

### Regarding SoraVoice

SoraVoice is not compatible with the AP Patch currently and for the foreseeable future.

## Generating a Game

1. Use `Generate Template Options` from Archipelago Launcher to get the YAML option file.
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).

## Connecting to a Server

1. Launch `Trails in the Sky 3rd Client` from Archipelago Launcher.
2. Ensure the game is **not** running.
3. Connect the client to the server by enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.
4. If this is your first time connecting, the client will ask for your `Trails in the Sky 3rd` installation folder.
    - If you want to change this settings you can do so inside the `host.yaml` file.
5. The client will appear to be frozen for a few seconds to install the game mod.
6. When the client says `Waiting for connection to Trails in the Sky the 3rd game instance...` you can start the game.
7. Start a new game or load from a previous AP save.

For a new game, you will start inside the Hermit Garden. To start sending or receiving item, interact with the Stone Monument or enter the Jade Corridor. This will only happen once.

### Regarding Save File

On a new AP game launch, the game will store a unique save id into the game save data. You can only send or receive data if the unique save id matches with what the client expects.

## Current Known Issue

- Your camera might get stuck if you interact with any object immediately after closing the receiving or sending item message. You can fix it by save/load, changing area, or use the Cube to teleport to another point.
