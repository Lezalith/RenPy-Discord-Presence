# Discord Rich Presence Support for Ren'Py Projects
This script contains a `discord` namespace containing functions used to interact with Discord Rich Presence. It is very intuitive and simple to use, but can only be run on Ren'Py 8, as the module this script depends on doesn't have a Py2 version.

An Application set up on the [Discord Developer Portal](https://discord.com/developers) is required for every game supporting Rich Presence. After the App is created, you will receive the necessary **Application ID** to insert into **settings.rpy**, and it is also where all the images you plan on displaying in the presence need to be uploaded first. What it is and how to work with it is covered [under the **Wiki** tab](https://github.com/Lezalith/RenPy_Discord_Presence/wiki/Interacting-with-Discord-Developer-Portal) on this GitHub page, local copy of which is included in the code files.

Finally, this project is under the **MIT License**. This means you can use, modify and/or distribute this script, as long as I am credited ("Lezalith" is enough, but a link to my website with Ren'Py content, LezCave.com, is greatly appreciated!) and as long as the **LICENSE.txt** file stays included.

# Table of Contents:

- [Download of one of two versions of a **Discord Rich Presence**.](https://github.com/Lezalith/RenPy_Discord_Presence#download)
- [Variables that you need to check out before using this script.](https://github.com/Lezalith/RenPy_Discord_Presence#related-variables)
- [Functions and Screen Actions that allow you to interact with the Discord Presence.](https://github.com/Lezalith/RenPy_Discord_Presence#interacting-with-the-presence)
- [First part of the Rich Presence elements all described.](https://github.com/Lezalith/RenPy_Discord_Presence#basic-rich-presence-elements)
- [Second part of the Rich Presence elements all described.](https://github.com/Lezalith/RenPy_Discord_Presence#advanced-rich-presence-elements)
- [Notes about compatibility and limitations.](https://github.com/Lezalith/RenPy_Discord_Presence#important-notes)
- [Examples of using this script inside both `screen` and `label`.](https://github.com/Lezalith/RenPy_Discord_Presence#examples)

# Download
To get the script, download one of the releases on the right side of the GitHub page, under the [**Releases** section](https://github.com/Lezalith/RenPy_Discord_Presence/releases). Here are the files that you need to put into your **game** folder:

- **python-packages** folder contains the **pypresence** module that handles everything Discord-related. [![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

- **RenPy_Discord_Presence** folder contains this script's files:
    - **rich_presence.rpy**  holds the entire script code.
    - **settings.rpy** contains the two [**Related Variables**](https://github.com/Lezalith/RenPy_Discord_Presence#related-variables) described below.
    - **discord_developer_portal.md** is a local copy of the [**Wiki** tab](https://github.com/Lezalith/RenPy_Discord_Presence/wiki/Interacting-with-Discord-Developer-Portal), as already mentioned.
    - **LICENSE.TXT**, a file containing the MIT License that I ask you keep when downloading the files.

There are two versions for every release:

## Project Version
**Project Version** contains the whole code of this repository. It is a project that can be launched from the Ren'Py Launcher and that shows how simple it is to update the presence status from both **screens** and **labels**, utilizing the `set` and `update` [functions](https://github.com/Lezalith/RenPy_Discord_Presence#functions) and their [screen actions](https://github.com/Lezalith/RenPy_Discord_Presence#screen-actions) counterparts, both described below. Simply launch the project and keep an eye on your Discord profile.

All of the project's code is located in its **script.rpy** file.

## Clean Version
**Clean Version** does not contain project files and only contains the files listed [above](https://github.com/Lezalith/RenPy_Discord_Presence#download), meaning you can just copy everything over to your own project and you're good to go!

# Related Variables
There are some important variables in the **settings.rpy** file that you need to visit. Here is what they do:

`application_id` takes a **string** with an Application ID of your Application set up on Discord Developer Portal. This **has to** be set in order for this script to work, having an invalid ID set **will throw an error** when launching the game.
```py
define rich_presence.application_id = "10208ABCDEFGHIJ2795"
```

`main_menu_state` takes a dictionary. Keys are **strings** of properties corresponding to [presence elements](https://github.com/Lezalith/RenPy_Discord_Presence#basic-rich-presence-elements), and values are their values.

This is the state shown in the presence anytime the game launches and/or enters the main menu. Below is what it looks like by default.
```py
define rich_presence.main_menu_state = { "details" : "In the Main Menu.",
                                       "large_image" : "lezalith"}
```

There's also the `start_state`. Just like `main_menu_state`, this is a set of properties, ones that are set when the game starts.
Script acknowledges this by reaching the start label, name of which you need to set in the `start_label` variable. It can also be a **list** of label names instead, in case you have multiple labels this game can **Start** at.

Unlike `main_menu_state`, `start_state` doesn't *have to* be set, and `start_label` can be set to **None** to ignore its functionality.
```py
define rich_presence.start_state = { "details" : "Reading the Story.",
                                       "large_image" : "lezalith"}

define rich_presence.start_label = "start"
```

Finally, there are **log** variables controlling what is printed out. Prints are recorded in the game's console and in the **log.txt** file. There are three of them:

```py
# Shows whether the Presence was initialized and closed correctly.
define discord.log_important = True 

# Records properties whenever they change with set or update methods.
define discord.log_properties = True 

# Notes whenever the properties get rolled back or loaded from a save file, and what they were restored into.
define discord.log_restore = True 
```

I recommend leaving these on, it's information your players can pass on to you in case they're having troubles with your game. 

# Interacting With The Presence
## Functions
Functions used to interact with the presence are defined inside the `discord` namespace. They're meant to be used inside `label`s and `init python` blocks.
Here are the core two:

`discord.set` takes **property names** corresponding to presence elements for arguments. All elements [are listed below](https://github.com/Lezalith/RenPy_Discord_Presence#basic-rich-presence-elements).
If some properties are already set in the presence, they are discarded and only the passed properties are kept.

An exception to this is the `start` property, which sticks to time since this session's launch unless specified.
```py
discord.set(details = "Setting new Discord Rich Presence.")
```

`discord.update` takes **property names** for arguments the same way `discord.set` does.
Difference between the two is that `discord.update` keeps the current properties as they are and only changes the ones provided.
```py
discord.set(details = "Setting new Discord Rich Presence.")
discord.update(state = "State got changed while details stayed the same!")
```

## Screen Actions
`discord.set` and `discord.update` have Screen Actions counterparts, intuitive alternatives to `Function(discord.set)` and `Function(discord.update)`.

Same rules apply for both Actions:

- They are sensitive as long as Presence was successfully initialized.
- They are selected if properties given to the Action inside the screen match currently shown properties. Exception to this is `start` - if it's not specified inside the screen but is present in currently shown properties, it is ignored in the comparison.

Here's an example of a simple screen with both Actions present. [Almost identical example is below](https://github.com/Lezalith/RenPy_Discord_Presence#screen-example).
```py
screen both_screen_actions():

    vbox:
        align (0.5, 0.5)

        textbutton "This one sets the state only.":
            action discord.Set(state = "Example State set.")

        textbutton "This sets details and leaves the state alone.":
            action discord.Update(details = "Details added while state was kept!")
```

# Basic Rich Presence Elements
There are many things that can be shown inside Rich Presence. Below is a screenshot of a couple elements of Rich Presence highlighted, with their **property name** equivalent below. All the **property names** are listed below the screenshot with a short example using `discord.update`.

In the preview project, dictionary with all the properties for this example is stored in the `rich_presence.first_example` variable.

![first_presence_example](https://user-images.githubusercontent.com/56970124/194740336-aeeeafa1-9f9a-49a0-a598-f539761044e6.png)
```py
discord.update(details = "Testing Discord Rich Presence.")
```

`state` takes a **string**, and is the lower line of text shown in the Presence.
```py
discord.update(state = "It's super easy in Ren'Py 8!")
```

`start` is a time from which Time Elapsed is calculated. It can take four different values:

- `"start_time"` makes Time Elapsed refer to the `start_time` variable, where time since this game session's launch is recorded.
- `"new_time"` inserts a new unix timestamp, reseting Time Elapsed to 0:0. It does **not** overwrite the recorded `start_time` by itself, but you can change that one directly if you need to.
- `None` which results in Time Elapsed being **hidden**.
- **Unix timestamp** from which Time Elapsed is calculated.
```py
discord.update(start = "start_time")
```

`large_image` takes a **string** that needs to correspond with an image uploaded onto the Discord Application.
It is the larger image shown on the left side. If it doesn't find an image with that name, it displays a placeholder question mark image.
```py
discord.update(large_image = "lezalith")
```

`small_image` takes a **string** that needs to correspond with an image uploaded onto the Discord Application. 
It is the smaller image, shown at the bottom right of the `large_image`. Unlike `large_image`, if it doesn't find an image with that name it shows nothing.

If no `large_image` is set or found, `small_image` is used in its place and no smaller image at the bottom right is shown.
```py
discord.update(large_image = "lezalith", small_image = "lezalith")
```

Overall, state shown on the screenshot can be accomplished with the following properties passed:
```py
discord.set(details = "Testing Discord Rich Presence.",
            state = "It's super easy in Ren'Py 8!",
            large_image = "lezalith",
            large_text = "Large Image Tooltip!",
            small_image = "lezalith",
            small_text = "Small Image Tooltip!")
```

As you can see, there are two more **property names** included there that I haven't mentioned - `large_text` and `small_text`. These are text tooltips that appear when the respective images are hovered by a cursor.

# Advanced Rich Presence Elements
The final screenshot covers all the remaining rich presence properties. `state` was already covered above, however it is required for the `party_size` property to work.

In the preview project, dictionary with all the properties for this example is stored in the `rich_presence.second_example` variable.

![second_presence_example](https://user-images.githubusercontent.com/56970124/194740611-7b59bba5-783c-49c8-a91f-65f9b5eab612.png)

`end` takes an **unix timestamp** and calculates Time Left until that timestamp. 

Setting this pushes `start` completely aside and Time Elapsed with it and **displays Time Left instead.**
```py
discord.update(end = time.time() + 3000)
```

`party_size` takes a **list** of two **ints**. This is used for multiplayer games, where the two numbers represent the current party size and max party size respectively. We can still use it with visual novels if we're creative enough.

For the `party_size` to be visible, `state` has to be also provided.
```py
discord.update(state = "Reading a Chapter", party_size = [1, 5])
```

`buttons` takes a **list** of **up to two dicts**, and allows for buttons to be added into the Presence. The dict consists of two keys, `label` being the text written inside the button, and `url` being the link opened upon clicking it. 

Note: Clicking buttons in the Presence in your own profile does nothing.

```py
discord.update(buttons = [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                           dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ]
```

Putting all of that together, state shown on the second example screenshot was created with these properties:
```py
discord.set(state = "Reading a Chapter",
            end = time.time() + 3000,
            party_size = [1, 5],
            buttons = [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                        dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ])
```

# Important Notes
## Discord Not Installed
Discord presence only works for users who have the Discord desktop application installed. For players that do not have Discord installed, this entire code will simply do nothing. `discord` variable is still defined with all the properties and methods, but none of the methods do anything.

This means that players who have Discord can enjoy the benefits while those who do not aren't hindered in any way.

## Saving, Loading and Rollback
All presence properties are compatible with both saving games and rollbacking dialogue:

- Loading a saved game will restore the properties that were present when the game was saved. `start` possibly preserves the value of `start_time` and refers to the **new** Time Elapsed.
- Rollbacking past a change in the presence will return the presence to the original state, as would be expected.

## Limitations

### config.label_callback Variable Taken
This script uses the `config.label_callback` variable to set `start_state`, meaning you can't use it yourself. If you're fine with `start_state` functionality not present, you can delete its `define` statement in **rich_presence.rpy**.

This will be fixed in Ren'Py 8.1 - a new variable called `config.label_callbacks` will be present, and that one can take multiple functions just like other callbacks. The line is already prepared in the file, and I'll release an updated version of this script myself once Ren'Py 8.1 comes out.

### Update Delays
A Discord Desktop Application running on the same machine as the game that's updating the presence, has updates on the player's profile shown instantly. This is not always the case for other Discord Desktop Apps - even ones where the account of the **player** is logged in, curiously enough.

How often this delay occurs seems to correlate with the frequency of the presence updates and especially affects the `clear` method, but you shouldn't worry about it too much, as it seems to be about 12s on average when it does occur.

### Too Many Connections
Connecting to the Discord Rich Presence multiple times in quick succession will result in the connection not being established. In practice, this happens when you...

- ...launch and quit...
- ...reload...
- ...start and return to the main menu in...

...the game too many (approximately 4) times too fast (span of approximately 40s).

This makes the game unresponsive for the approximate span since the oldest successful connection. Restarting the game doesn't fix this, and the game won't launch again until the timer runs out. 

My guess is that it's a precaution against malicious exploits on Discord's part and cannot be affected by Python code, but as is the case with [Update Delays](https://github.com/Lezalith/RenPy_Discord_Presence#update-delays) it's not a big issue - players should fulfill these requirements incredibly rarely, if ever.

# Examples
## Screen Example
Here is an example of two `textbutton`s in a screen, one with `discord.set` and other with `discord.update`.
```py
screen screen_example():

    vbox:
        align (0.5, 0.5)

        textbutton "This one sets the state only.":
            action discord.Set(state = "Example State.")

        textbutton "This sets details and leaves the state alone.":
            action discord.Set(details = "Example Details.")
```

## Label Example
And here is the example **label** used inside the preview project that showcases all of the functions. Everything is explained by the dialogue lines.
```py
label functionality_example():

    "This label shows how discord presence can be changed inside labels!"

    "Since it is set as the {b}start_label{/b} in {b}settings.rpy{/b}, entering it sets the presence to {b}start_state{/b}."

    "After this line, {b}discord.set{/b} will be called to set presence to only contain a {b}state{/b} text line."

    $ discord.set(state = "Update after the first line.")

    "And it is so."

    "After this line, {b}discord.update{/b} is called to change the {b}details{/b} property, while keeping others as they are."

    $ discord.update(details = "This wasn't here before!")

    "Presence now contains one more piece of info."

    "After this line, {b}start{/b} property is changed to {b}\"new_time\"{/b}, which will reset Time Elapsed to 0:0."

    $ discord.update(start = "new_time")

    "The time since the first launch can always be restored by changing {b}start{/b} property to {b}\"start_time\"{/b}"

    "Done after this line."

    $ discord.update(start = "start_time")

    "Finally, changing the {b}start{/b} property to {b}None{/b} hides Time Elapsed altogether."

    "Again, done after this line."

    $ discord.update(start = None)

    "As you can see, Time Elapsed is no longer visible."

    "Last method is {b}discord.clear{/b}, which can be called to clear the presence."

    $ discord.clear()

    "Presence all cleared and hidden!"

    "You will now return to the main menu. {b}main_menu_state{/b} will be restored and Time Elapsed will go back to the time of first launch."

    return
```

# Support
If you need help setting up this script or the App on Discord's Dev Portal, you can contact me on **Discord** itself. Either write me a DM, **Lezalith (LezCave.com)#2853**, or preferably **[join my server](https://discord.gg/Nnf6mMnfSe)**! It's a server dedicated to my website, **[LezCave.com](https://www.lezcave.com)**, where I post Ren'Py scripts and tutorials. 

A good alternative is pinging me on the official **[Ren'Py Discord server](https://discord.gg/48k3g3pwkC)**, where I'm one of the Moderators, so I'm very active there. You can send me an email at **Lezalith@gmail.com** if you want to be extra formal, but I don't check my emails very often. Consider also letting me know on Discord that you've sent me one, so I notice it and can reply to it.

Finally, if you want to be extra supportive, you can donate a dollar or two to my [Paypal.me](https://paypal.me/Lezalith). I'll use the money to improve my website and dedicate more time to posting new scripts and tutorials!
