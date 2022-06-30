#
# Simple Discord embed message limits class
#
#
# A simple class to allow to get the total length of fields used
# within an embed message



class EmbedLimits():
    total = 6000
    title = 256
    desc = 4096
    fields = 25

    class Field():
        name = 256
        value = 1024
        field_total = 1280

        def get_field_used_both(obj1, obj2):
            used1 = len(obj1)
            used2 = len(obj2)

            if used1 + used2 > field_total:
                # This shouldn't happen, but because the embed isn't sent yet
                # I don't think there's a way to know ahead of time while the
                # command is running if the length is maxed
                #
                # Just return -1 if the size overflows to indacate something
                # went wrong
                return -1
            else:
                # Return total used length for both strings
                return user1 + user2


    class Footer():
        text = 1024

    class Author():
        name = 256
