# Discord Rich Presence Support for Ren'Py Projects
This script creates a **RenPyDiscord** object stored in the **discord** variable, which can be used to interact with Discord Rich Presence. All it requires is an Application set up on the [Discord Developer Portal](https://discord.com/developers) and it's **Application ID**.

Upon launching the project, Presence status is set to values stored in the **initial_state** variable. After that, it can changed at any time by calling the **discord.update** method.

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

**start** takes a **string** with the epoch timestamp, from which it counts the Time Elapsed. However, this time should only be changed with the specialized method **change_time**.

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
```py
discord.update(small_image = "lezalith")
```

Overall, state from the screenshot can be accomplished with the following:
```py
discord.update(details = "Testing Discord Rich Presence.",
               state = "It's super easy in Ren'Py 8!",
               large_image = "lezalith",
               small_image = "lezalith")
```

