# Application Id - This is gotten Discord's Developer Portal.
define rich_presence.application_id = "1020817080838262795"

# Dict with all the properties of the presence state displayed when the game is launched.
define rich_presence.initial_state = { "details" : "Testing Discord Rich Presence.",
                                       "state" : "It's super easy in Ren'Py 8!"}

init -10 python:

    # Used to display time in the presence.
    import time

    # Alpha and Omega of Rich Presence.
    from pypresence import Presence

    # Class of object for interacting with the Rich Presence.
    class RenPyDiscord():

        # Called when defined.
        def __init__(self):

            # Rich Presence object, it controls everything.
            self.presence = Presence(rich_presence.application_id)

            # Records the timestamp currently used in the presence.
            # This is so that the same time can be kept upon updating the presence.
            self.time = time.time()

            # Runs the first setup.
            self.first_setup()

        # Connects to the Presence App and sets the initial state.
        def first_setup(self):

            # Connects to the Presence App.
            self.presence.connect()

            # Sets the initial state.
            self.update(**rich_presence.initial_state)

        # Updates the state to provided properties. The *state* field is required.
        # Current timestamp is kept if keep_time is True, and is reset to 0.0 if keep_time is False.
        def update(self, keep_time = True, **fields):

            # Resets the time if it's not to be kept.
            if not keep_time:
                self.time = time.time()

            # Update the presence.
            self.presence.update(start = self.time, **fields)

# The object for interacting with Rich Presence defined.
default discord = RenPyDiscord()