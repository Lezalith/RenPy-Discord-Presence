# Discord Rich Presence Support for Ren'Py Projects
This script creates a `RenPyDiscord` object stored in the `discord` variable, which can be used to interact with Discord Rich Presence. It can only be run on Ren'Py 8 - Unlike Ren'Py 7, that one runs on Python 3, and the module this script depends on only has a Py3 version.

An Application set up on the [Discord Developer Portal](https://discord.com/developers) is required for every game supporting Rich Presence. After the App is created, you will receive the necessary **Application ID** to insert into **settings.rpy**, and it is also where all the images you plan on displaying in the presence need to be uploaded first.

Instructions on how all of that is done are found [under the **Wiki** tab](https://github.com/Lezalith/RenPy_Discord_Presence/wiki/Interacting-with-Discord-Developer-Portal) on this GitHub page, local copy of which is included in the code files.

Finally, you can use, modify and/or distribute this script, as long as I am credited ("Lezalith" is enough, but a link to my website with Ren'py content, LezCave.com is greatly appreciated!) and as long as the **LICENSES.txt** file stays included.

# Download
To get the script, download one of the releases on the right side of the GitHub page, under the [**Releases** section](https://github.com/Lezalith/RenPy_Discord_Presence/releases). Here are the files that you need to put into your **game** folder:

- **python-packages** folder contains the **pypresence** module that handles everything Discord-related: [![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

- **RenPy_Discord_Presence** folder contains this script's files:
    - **rich_presence.rpy**  holds the entire script code
    - **settings.rpy** contains the two [**Related Variables**](https://github.com/Lezalith/RenPy_Discord_Presence#related-variables) described below.
    - **discord_developer_portal.md** is a local copy of the [**Wiki** tab](https://github.com/Lezalith/RenPy_Discord_Presence/wiki/Interacting-with-Discord-Developer-Portal), as already mentioned.

There are two versions for every release:

## Project Version
**Project Version** contains the whole code of this repository. It is a project that can be launched from the Ren'Py Launcher and that shows how simple it is to update the presence status from both **screens** and **labels**, utilizing the `set` and `update` [methods described below](https://github.com/Lezalith/RenPy_Discord_Presence#list-of-methods). Simply launch the project and keep an eye out on your Discord profile.

## Standalone Version
**Standalone Version** does not contain the project files and only contains the files listed [above](https://github.com/Lezalith/RenPy_Discord_Presence#download).

# Related Variables
There are two variables defined in the **settings.rpy** file that you need to set before using the code. Here is what they do and what their default value is:

`application_id` takes a **string** with an Application ID of your Application set up on Discord Developer Portal.
```py
define rich_presence.application_id = "10208ABCDEFGHIJ2795"
```

`initial_state` takes a dictionary. Keys are **strings** of properties corresponding to [presence elements](https://github.com/Lezalith/RenPy_Discord_Presence#basic-rich-presence-elements), and values are their values.

This is the state shown in the presence anytime the game launches and/or enters the main menu.
```py
define rich_presence.initial_state = { "details" : "Testing Discord Rich Presence.",
                                       "state" : "It's super easy in Ren'Py 8!",
                                       "large_image" : "lezalith", 
                                       "small_image" : "lezalith"}
```

# List of Methods
Methods used to interact with the presence are bound to a defined `RenPyDiscord` instance stored in the `discord` variable.
Here are the core three:

`discord.set` takes the `keep_time` argument which is `True` by default, to determine whether the Elapsed Time shown should be reset to 0:0 with this change.
As for the arguments that follow, they should correspond to presence elements - [all are listed below](https://github.com/Lezalith/RenPy_Discord_Presence#basic-rich-presence-elements).
If some properties are already set in the presence, they are discarded, and only the passed properties are kept.
```py
discord.set(keep_time = False, details = "Setting new Discord Rich Presence.")
```

`discord.update` takes `keep_time` with default `True` and properties corresponding to presence elements just like `discord.set` does.
Difference between the two is that `discord.update` keeps the current properties and only sets the ones provided.
```py
discord.set(details = "Setting new Discord Rich Presence.")
discord.update(state = "State got changed while details stayed the same!")
```

Finally, `discord.change_time` is a method specialized in changing the Time Elapsed. It takes the optional `timestamp` argument, which is an epoch timestamp from which Time Elapsed is calculated. If it's `None`, as it is by default, the time gets reset to 0:0.
```py
discord.set(details = "Let's set Time Elapsed to 600 seconds, aka 10 minutes!")
discord.change_time(timestamp = time.time() + 600)
```

# Basic Rich Presence Elements
There are many things that can be shown inside Rich Presence. Below is a screenshot of a couple elements of Rich Presence highlighted, with their **property** name equivalent below. They are all listed below the screenshot with a short example using `discord.update`.

In the preview project, dictionary with all the properties for this example is stored in the `rich_presence.first_example` variable, and `rich_presence.initial_state` is redirected to it, both inside **script.rpy**.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190881237-3f1e0b72-d954-4af2-8a93-a35e59bdf51e.png)

`details` takes a **string**, and is the upper line of text shown in the Presence.
```py
discord.update(details = "Testing Discord Rich Presence.")
```

`state` takes a **string**, and is the lower line of text shown in the Presence.
```py
discord.update(state = "It's super easy in Ren'Py 8!")
```

`start` takes an epoch timestamp from which it counts the Time Elapsed. However, `start` should only be changed with the specialized `change_time` method described above in [**List of Methods**](https://github.com/Lezalith/RenPy_Discord_Presence#list-of-methods). 

Snippet below shows it with the `timestamp` not provided, causing it to set Time Elapsed to 0:0.
```py
discord.change_time()
```

`large_image` takes a **string** that needs to correspond with an image uploaded onto the Discord Application. If it doesn't find an image with that name, it simply displays nothing, as if it wasn't provided.
It is the large image shown on the left side.
```py
discord.update(large_image = "lezalith")
```

`small_image` takes a **string** that needs to correspond with an image uploaded onto the Discord Application. As is the case with `large_image`, it also displays nothing if it doesn't find an image with that name.
It is the smaller image, shown at the bottom right of the `large_image`.

If no `large_image` is set or the image was not found, `small_image` is used in its place and no smaller image at the bottom right is shown.
```py
discord.update(large_image = "lezalith", small_image = "lezalith")
```

`time` is a special non-pypresence property that can be `True` or `False`.
If `True` (the default), Elapsed Time is shown in the presence. If `False`, it is hidden.
```py
discord.update(time = False)
```

Overall, state shown on the screenshot can be accomplished with the following properties passed:
```py
discord.set(details = "Testing Discord Rich Presence.",
            state = "It's super easy in Ren'Py 8!",
            large_image = "lezalith",
            large_text = "Large Image Tooltip!",
            small_image = "lezalith",
            small_text = "Small Image Tooltip!",
            time = True)
```

As you can see, there are two more variables included there that I haven't mentioned - `large_text` and `small_text`. These are text tooltips that appear when the respective images are hovered by a cursor.

# Advanced Rich Presence Elements
Another screenshot covers all the remaining rich presence properties. `state` was covered above, however it is required for the `party_size` property to work.

In the preview project, dictionary with all the properties for this example is stored in the `rich_presence.second_example` variable inside **script.rpy**.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190882416-25642658-8823-4d05-8dd9-ee9f9e6d62bf.png)

`end` takes an epoch timestamp and calculates Time Left until that timestamp. 

Setting this pushes `start` completely aside and the Time Elapsed with it, **displaying Time Left instead.**
```py
discord.update(end = time.time() + 3000)
```

`party_size` takes a **list** of two **ints**. This is used for multiplayer games, where the two numbers represent the current party size and max party size respectively. We can still use it with visual novels if we're creative enough.

For the `party_size` to be visible, `state` has to be also provided.
```py
discord.update(state = "Reading a Chapter", party_size = [1, 5])
```

`buttons` takes a **list** of **up to two dicts**, and allows for buttons to be added into the Presence. The dict consists of two keys, `label` being the text written on the button, and `url` being the url opened upon clicking it. 

Note: Clicking buttons in your own Presence - i.e. in your own profile - does nothing.

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
Discord presence only works for users who have the Discord desktop application installed. For players that do not have Discord installed, this entire code will simply do nothing. `discord` variable is still defined as the `RenPyDiscord` object, but none of its methods do anything.

This means that players with Discord can enjoy the benefits, and those who do not have it aren't hindered in any way.

## Saving and Loading
All presence properties, along with time property that determines whether Time Elapsed is shown, are saved in save files and restored when the save is loaded.

Upon loading a save, Time Elapsed is reset to 0:0.
 
## Rollback
The presence *should* be fully compatible with rollback and rollforward features of Ren'Py. 

## Too Many Connections
Connecting to the Discord Rich Presence multiple times in quick succession will result in the connection not being established.
This makes the program unresponsive and unable to be launched again for about the next 30s. I'd imagine it's a precation against malicious exploits on Discord's side, and cannot be affected by Python code.

In practice, this happens when you...
- ...launch and quit...
- ...reload...
- ...start and return to the main menu in...

...the game too many times too fast.

# Examples
Here is an example of two `textbutton`s in a screen, one with `discord.set` and other with `discord.update`.
```py
screen screen_example():

    vbox:
        align (0.5, 0.5)

        textbutton "This one sets the state only.":
            action Function(discord.set, state = "Example State.")

        textbutton "This sets details and leaves the state alone.":
            action Function(discord.update, details = "Example Details.")
```

And here is the example **label** used inside the preview project that showcases all of the functions. Everything is explained by the dialogue lines.
```py
label label_example():

    "This label shows how discord presence can be changed inside labels!"

    "After this line, {b}discord.set{/b} will be called to set presence to only contain a {b}state{/b} text line."

    $ discord.set(state = "Update after the first line.")

    "And it is so. Elapsed Time stayed the same."

    "After this line, {b}discord.set{/b} is called again, with {b}keep_time = False{/b} argument passed, so that the time gets set to 0:0."

    $ discord.set(state = "Second update, with the time reset.", keep_time = False)

    "State updated and Elapsed Time reset."

    "After this line, {b}discord.update{/b} is called to change the {b}details{/b} property, while keeping others ({b}state{/b} and {b}time{/b}) as they are."

    $ discord.update(details = "This wasn't here before!")

    "Presence now contains one more piece of info."

    "After this line, {b}discord.change_time{/b} is called to change the Time Elapsed shown. The time is reset and 3000 seconds are added to it."

    $ discord.change_time(timestamp = time.time() - 3000)

    "3000 seconds is 50 minutes, so that's what Time Elapsed got set to."

    "By default, the Time Elapsed is shown. It can be hidden by setting the {b}time{/b} property to False."

    "It is done with {b}discord.update{/b} after this line."

    $ discord.update(time = False)

    "As you can see, Time Elapsed is no longer visible."

    "Finally, after this line, {b}discord.clear{/b} is called to clear the presence."

    $ discord.clear()

    "Presence all cleared and hidden!"

    "After this line, you will return to the main menu, and {b}initial_state{/b} will be restored."

    return
```
