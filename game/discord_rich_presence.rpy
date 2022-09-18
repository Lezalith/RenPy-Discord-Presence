# Application Id - This is gotten Discord's Developer Portal.
define rich_presence.application_id = "1020817080838262795"

# Dict with all the properties of the presence state displayed when the game is launched.
# keys correspond not to Presence Fields, but to pypresence arguments! Here is the list of them:
#
# state (str) – the user’s current status
# details (str) – what the player is currently doing
# start (int) – epoch time for game start
# end (int) – epoch time for game end
# large_image (str) – name of the uploaded image for the large profile artwork
# large_text (str) – tooltip for the large image
# small_image (str) – name of the uploaded image for the small profile artwork
# small_text (str) – tootltip for the small image
# party_size (list) – current size of the player’s party, lobby, or group, and the max in this format: [1,4]
# buttons (list) – list of dicts for buttons on your profile in the format [{"label": "My Website", "url": "https://qtqt.cf"}, ...], can list up to two buttons
define rich_presence.initial_state = { "state" : "Reading a Chapter",
                                       "end" : time.time() + 3000,
                                       "party_size" : [1, 5],
                                       "buttons" : [ {"label" : "Discord Presence Example Button", "url" : "https://github.com/Lezalith/RenPy_Discord_Presence"},
                                                     {"label" : "Lezalith's Promotion Button!", "url" : "https://www.lezcave.com"}]}

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

            # Dict of current Presence properties.
            self.properties = {}

            # Runs the first setup.
            self.first_setup()

        # Connects to the Presence App and sets the initial state.
        def first_setup(self):

            print("Attempting to connect to Discord Rich Presence...")

            # Connects to the Presence App.
            self.presence.connect()

            print("Successfully connected.")

            # Sets the initial state.
            self.set(**rich_presence.initial_state)

        # Updates the state to provided properties. The *state* field is required.
        # Current timestamp is kept if keep_time is True, and is reset to 0:0 if keep_time is False.
        def set(self, keep_time = True, **fields):

            # Records all the properties passed to the Presence.
            self.properties = fields

            # Resets the time if it's not to be kept.
            if not keep_time:
                self.time = time.time()

            # Update the presence.
            self.presence.update(start = self.time, **self.properties)

        # Changes the Time Elapsed, while keeping everything else untouched.
        # timestamp is None by default, which resets the time to 0:0.
        def change_time(self, timestamp = None):

            if timestamp is None:
                self.time = time.time()

            else:
                self.time = timestamp

            # Update the Presence with new time and current properties.
            self.presence.update(start = self.time, **self.properties)

# The object for interacting with Rich Presence defined.
default discord = RenPyDiscord()