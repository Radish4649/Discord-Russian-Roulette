# this program returns the relevant code for that channel
def get_code(cxt):
    return str(cxt.guild) + " " + str(cxt.channel)


def is_plural(num):
    if num == 1:
        return ""
    else:
        return "s"
