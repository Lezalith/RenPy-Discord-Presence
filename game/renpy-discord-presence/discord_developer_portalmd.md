# What is it and what is it used for?
**Discord Developer Portal** is a corner on the official Discord website that allows creating applications. These applications are used to interact with Discord's code. 

The most common applications are **bots**. Yes, those bots that are added onto Discord servers to provide all kinds of functionality, from playing music in voice channels to giving users virtual xp for writing in channels. The second most common ones are apps for interacting with Rich Presence - that's what we're here for.

# Creating an application
To create a new application, click the **New Application** blue button in top right. You should create a new app for each of your projects that uses RenPy Discord Presence.

![1](https://user-images.githubusercontent.com/56970124/192089196-8e266520-9f74-4006-89f5-468f3a7fed11.png)

You will be asked to input a name, do so and click **Create**. This name is displayed inside the Presence when the game is being played, so it of course should be the name of your game. Don't worry, you can always change it later.

![2](https://user-images.githubusercontent.com/56970124/192095513-7bd5cdc9-0867-4073-9348-972d3a8b26d6.png)

And that's all. The application is now created and you've been brought to its main page.

![3](https://user-images.githubusercontent.com/56970124/192091720-92843357-3030-4c4c-ae11-4a5dc67e0c6d.png)

Top of the main page contains a couple of things:
- **Name** is what you've chosen when creating the application, shown inside presence when the game is being played.
- **App Icon** is shown on the list of applications at the beginning of the Discord Developer Portal. It's pretty.
- **Description** is absolutely useless to us, as it's used by bots...
- ...and so are the **Tags**.

Finally:
- **Application ID.** This is the most important thing of all, you need to copy it over to **settings.rpy** as a value for the **application_id** variable. Simply put: Your game uses this to communicate with this application, and this application communicates with presences in users' profiles. And don't worry about this being in your code, it cannot be misused by others!

After you copy the **App ID** to the **settings.rpy** file, you're ready to start using this script.

# Preparing images
On the left side, there is a menu with the **Rich Presence** tab. Clicking it takes you to its sub-tab, **Art Assets**.  

![4](https://user-images.githubusercontent.com/56970124/192093502-55342b26-34f6-4539-a2ea-aff60dd3643d.png)

This is where you need to upload all the images that you want to show in the presence. Since your game communicates with the application and not the presence, it cannot tell presence what image to show. Instead, your game tells the application which image to show, and the app displays it inside the presence.

To upload an image, click the blue **Add Image(s)** button, which will prompt you to select one or more files. As the note next to the button says, they have to be in the **.png**, **.jpg** or **.jpeg** format, and are recommended to be **1024x1024** in size. They don't have to be that big, but they have to be at least **512x512**.

After the files are done uploading, they will appear under **Rich Presence Assets** with editable names. This is the name that you'll be using in your code to refer to them, so be short and descriptive. The name **cannot be changed later**, but if you do mess up, you can always delete the image and re-upload it.

![5](https://user-images.githubusercontent.com/56970124/192094366-806b97d8-70af-4324-92e2-b75f6002d66f.png)

Once you've named the image(s), you can click the green **Save Changes** button to confirm it, and voilà, the image is now prepared to be referred in your code.

![6](https://user-images.githubusercontent.com/56970124/192093946-ed45c714-b3a4-4a81-8c21-24d6068c9bb7.png)

# Visualizer
One more cool feature that I want to mention in this doc is the **Visualizer** sub-tab in the left-side menu. Here, you can see what the user's presence looks like when playing your game. If you're just starting out with **RenPy Discord Presence**, this can help you, well, visualize how the presence will look with your code!

![7](https://user-images.githubusercontent.com/56970124/192094127-2fabea63-b3b5-472d-9479-b6cf57f75e38.png)

Below all the fields is the preview in question. Transferring it into game code, here is what it would looks like:
```py
discord.set(state = "Scene 1: Perfect Day",
            large_image = "sophie",
            small_image = "book")
```

And being the one who tested all this, let me finish by showing you what those properties look like on my own profile.

![result](https://user-images.githubusercontent.com/56970124/192094276-462b12f8-9fd3-475a-8d6f-bfb4bd365ee4.png)

# Credits
This documentation page was made with the help of WitchyDev and their project **Sophie the Witch**. You can check the game out on [its itch.io page](https://witchydev.itch.io/sophie-the-witch) and I've included a few screenshots below, just because I think the game looks great. Thank you, Witchy!

![screen3](https://user-images.githubusercontent.com/56970124/192091285-c253b692-b898-47c6-b649-8fbb7a42b187.png)
![screen2](https://user-images.githubusercontent.com/56970124/192091344-1468e799-8af5-4b7c-9d29-e6e0f93e9dbb.png)
![screen1](https://user-images.githubusercontent.com/56970124/192091345-af6a236a-8f10-4d69-8bed-d8c88f363f70.png)