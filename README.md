# Discord Rich Presence Support for Ren'Py Projects
This script creates a **RenPyDiscord** object stored in the **discord** variable, which can be used to interact with Discord Rich Presence. All it requires is an Application set up on the [Discord Developer Portal](https://discord.com/developers) and it's **Application ID**.

Upon launching the project, Presence status is set to values stored in the **initial_state** variable. After that, it can changed at any time by calling one of the bound methods.

# set and update Methods
**discord.set** and **discord.update** are two ways of changing the Presence. They both take the **keep_time** argument to determine whether the Elapsed Time should be reset to 0:0 with this change, and all following arguments should correspond to Presence Elements - all are listed below.

The difference between the two methods is that while **set** sets the properties only to those given, **update** updates the given properties and leaves others already set alone.

# Basic Rich Presence Elements
There are many things that can be shown in Rich Presence. In this screenshot, individual elements of the Presence are highlighted and their **argument** equivalent for **discord.update** method listed at the bottom.

Aside from the Presence arguments, there's one argument that can be passed to **discord.update** - **keep_time**, which determines whether the Time Elapsed should be reset to zero. Default of **True** leaves the time unchanged, while setting it to **False** resets it.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190881237-3f1e0b72-d954-4af2-8a93-a35e59bdf51e.png)

**details** takes a **string**, and is the upper text line shown in the Presence.
```py
discord.update(details = "Testing Discord Rich Presence.")
```

**state** takes a **string**, and is the lower text line shown in the Presence.
```py
discord.update(state = "It's super easy in Ren'Py 8!")
```

**start** takes a **string** with an epoch timestamp, from which it counts the Time Elapsed. However, this time should only be changed with the specialized method **change_time**.

**change_time** takes the optional **timestamp** argument, which is the epoch timestamp from which the Time Elapsed is calculated. If it's **None**, as it is by default, the time gets reset to 0:0.
```py
discord.change_time()
```

**large_image** takes a **string** that needs to correspond with an image uploaded onto the Discord Application.
It is the large image shown on the left side.
```py
discord.update(large_image = "lezalith")
```

**small_image** takes a **string** that needs to correspond with an image uploaded onto the Discord Application.
It is the smaller image, shown at the bottom right of the **large_image**.

If no **large_image** is set, **small_image** is used in it's place instead of being the miniature at the botoom right as it should be.
```py
discord.update(large_image = "lezalith", small_image = "lezalith")
```

Overall, state shown on the screenshot can be accomplished with the following:
```py
discord.set(details = "Testing Discord Rich Presence.",
            state = "It's super easy in Ren'Py 8!",
            large_image = "lezalith",
            large_text = "Large Image Tooltip!",
            small_image = "lezalith",
            small_text = "Small Image Tooltip!")
```

There are two more variables there that I haven't mentioned - **large_text** and **small_text**. This is a text tooltip that appears when the respective images are hovered.

# Advanced Rich Presence Elements
We have one more screenshot, after which all the features of Rich Presence will be covered. **state** was covered above, however it is required for **party_size** to work.

![rich_presence_example](https://user-images.githubusercontent.com/56970124/190882416-25642658-8823-4d05-8dd9-ee9f9e6d62bf.png)

**end** takes a **string** with an epoch timestamp and calculates time remaining until that timestamp. It pushes aside **start** completely, and the Time Elapsed with it.
It is the smaller image, shown at the bottom right of the **large_image**.
```py
discord.update(end = time.time() + 3000)
```

**party_size** takes a **list** of two **ints**. This is used for multiplayer games, where the two numbers would represent the current party size and max party size respectively. We can still use it with visual novels if we're clever enough.

For the **party_size** to be visible, **state** has to be also provided.
```py
discord.update(state = "Reading a Chapter", party_size = [1, 5])
```

**buttons** takes a **list** of **up to two dicts**, and allows for buttons to be added into the Presence. The dict consists of two keys, **label** being the text written on the button, and **url** being the url opened upon clicking it. 

Note: Clicking buttons in your own Presence does nothing.

```py
discord.update(buttons = [ dict(label = "Discord Presence Example Button", url = "https://github.com/Lezalith/RenPy_Discord_Presence"),
                           dict(label = "Lezalith's Promotion Button!", url = "https://www.lezcave.com") ]
```

Putting all of that together, state shown on the screenshot was created with these properties:
```py
discord.set(state = "Reading a Chapter",
            end = time.time() + 3000,
            party_size = [1, 5],
            buttons = [ {"label" : "Discord Presence Example Button", "url" : "https://github.com/Lezalith/RenPy_Discord_Presence"},
                        {"label" : "Lezalith's Promotion Button!", "url" : "https://www.lezcave.com"}])
```
