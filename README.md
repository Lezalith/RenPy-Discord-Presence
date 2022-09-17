# Discord Rich Presence support for Ren'Py Projects
This script creates a **RenPyDiscord** object stored in the **discord** variable, which can be used to interact with Discord Rich Presence. All it requires is an Application set up on the [Discord Developer Portal](https://discord.com/developers) and it's **Application ID**.

Upon launching the project, Presence status is set to values stored in the **initial_state** variable. After that, it can changed at any time by calling the **discord.update** method.

# TODO: Overview of all the possible fields