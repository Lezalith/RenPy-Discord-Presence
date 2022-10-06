# TODO: time in second_example stays the same.
# TODO: label_callback is NOT a list! BUT NEW VAR GOT ADDED NOT REMOVED SO ITS PROBABLY OKAY.

# Following are all methods being appended to different callbacks.
# Callbacks are lists of methods that are ran when something happens.
# As creators can define them themselves, they're accessed here and changed rather than overwritten.

# quit_callbacks trigger when quitting the game. Serves to properly close the connection to the Presence.

# rollback_check is what makes rollback and save/load work.
# after_load_callbacks trigger when a game is loaded.
# interact_callbacks trigger on every interaction.

# start_callbacks trigger when the game is done launching. Records the presence's initial properties into a global var.
# Even though backup_properties is triggered during init, the global var is overwritten afterwards by a default statement.

# start_callbacks trigger when the game is done launching. Records the presence's initial properties into a global var.

define config.quit_callbacks = [discord.close]
define config.after_load_callbacks = [discord.rollback_check]
define config.interact_callbacks = [discord.rollback_check]
define config.start_callbacks = [discord.reset]
define config.label_callback = discord.set_start
# define config.label_callbacks = [discord.set_start]

init -950 python in discord:

    # Used instead of regular print across this code.
    # Difference is that it only prints out text if `log` is set to True in settings.rpy
    def rich_print(s):
        global log
        if log is True:
            print(s)

    # Alpha and Omega of Rich Presence.
    import pypresence

    # Try to set up the Presence object and connect through it to the Discord Presence App.
    try:
        rich_print("Attempting to connect to Discord Rich Presence...")
        presence_object = pypresence.Presence(application_id)
        presence_object.connect()
        rich_print("Successfully connected.")

    # Discord Desktop App was not found installed.
    except pypresence.DiscordNotFound:
        rich_print("Discord Desktop App not found. Rich Presence will be disabled.")
        presence_object = None

    # Error occured while connecting to the Presence App.
    # Note: This is also raised when the Desktop App is installed but no account is logged in.
    except pypresence.DiscordError:
        rich_print("Error occured during connection. Rich Presence will be disabled.")
        presence_object = None

    # For interacting with Rollback.
    from store import NoRollback

    # Used to display time in the presence.
    import time

    # Timestamp of when the game started. Time Elapsed is calculated from it.
    # Presence can always restore it by changing the start property to "start_time"
    start_time = time.time()

    # For copying dictionaries with properties.
    from copy import deepcopy

    # Returns None, no matter the arguments.
    def return_none(*_args, **_kwargs): pass

    # Decorator that is called before every RenPyDiscord method.
    # If DiscordNotFound or DiscordError were encountered during init, return_none follows rather than the method called originally.
    def presence_disabled(func):
        global presence_object
        if presence_object is None:
            return return_none
        else:
            return func

    # REWRITE
    def backup_properties():

        global properties, properties_copy
        properties_copy = deepcopy(properties)
        print("Properties recorded: {}".format(properties_copy))

    # Sets the state to provided properties.
    @presence_disabled
    def set(**props):

        # Records all the properties passed to the Presence.
        global properties
        properties = deepcopy(props)

        global start_time

        # If start is specified in the passed properties:
        if "start" in properties:

            # First special argument, restores start_time
            if properties["start"] == "start_time":
                properties["start"] = start_time

            # Second special argument, resets time to 0:0.
            elif properties["start"] == "new_time":
                properties["start"] = time.time()

        # If "start" for calculating elapsed time is not provided in the state,
        # set it here to the recorded start_time.
        else:

            # if properties:
            properties["start"] = start_time

        # Record the updated properties into a global var.
        backup_properties()

        # Update the presence.
        global presence_object
        presence_object.update(**properties)

    # Updates the provided properties, while leaving others as they are.
    @presence_disabled
    def update(**props):

        global properties, start_time

        # If start is specified in the passed properties:
        if "start" in props:

            # First special argument, restores start_time
            if props["start"] == "start_time":
                properties["start"] = start_time
                del props["start"]    

            # Second special argument, resets time to 0:0.
            elif props["start"] == "new_time":
                properties["start"] = time.time()
                del props["start"]          

        # Update properties passed.
        for p in props:
            properties[p] = props[p]

        # Record the updated properties into a global var.
        backup_properties()

        # Update the presence.
        global presence_object
        presence_object.update(**properties)

    # Resets the presence to the original properties, gotten from discord.main_menu_state.
    @presence_disabled
    def reset():

        # Sets the initial state.
        global original_properties
        set(**original_properties)

    # Compares the properties to their rollback-able version and updates the presence accordingly if they do not match.
    # This is what makes the script rollback/rollforward compatible.
    @presence_disabled
    def rollback_check():

        global properties, properties_copy

        if properties != properties_copy:

            print("Properties do not match during this interaction. They will be set to Copy.")
            print("Copy: {}".format(properties_copy))
            print("This: {}".format(properties))

            set(**properties_copy)

    # Properly closes the connection with the Rich Presence.
    # Internally clears the info, no need to call the clear method prior.
    @presence_disabled
    def close():

        rich_print("Closing DRP connection.")

        global presence_object
        presence_object.close()

        rich_print("Successfully closed.")

    # Sets the Presence to start_state properties.
    @presence_disabled
    def set_start(label_name, interaction):

        global start_state, start_label

        # If there are multiple start labels:
        if isinstance(start_label, list):
            if label_name in start_label:
                set(**start_state)

        # If there is only one start label:
        elif label_name == start_label:
            set(**start_state)


    ## NOTE: clear seems to have its effect delayed if called too soon
    ##       after establishing the connection (first_setup) or another clear call.
    ## 
    ##       The delay seems to be about 10s on average.
    ##       The minimum wait time to avoid this seems to be about 15s.
    ##
    ##       Same happens with the close method defined below.

    # Clears all the info in the presence, hiding the game being played.
    @presence_disabled
    def clear():

        global properties

        print("clear called.")

        # First, get rid of images if they're present.
        # presence_object.update(large_image = None, small_image = None)

        # Clear currently recorded properties.
        properties = {}
        
        backup_properties()
        # global properties_copy
        # properties_copy = {}

        global presence_object
        presence_object.clear()


    # Class of object used for interacting with the Rich Presence.
    class RenPyDiscord(NoRollback):

        # Called when defined.
        def __init__(self):
            self.properties = {}

    # Current properties of the presence.
    global properties
    properties = {} 

    # First properties displayed.
    global original_properties, main_menu_state    
    original_properties = deepcopy(main_menu_state)

    # Insert Time Elapsed into original properties if not provided.
    if not "start" in original_properties:
        original_properties["start"] = start_time

# Dictionary mirroring the properties for Rollback reasons.
default discord.properties_copy = {}