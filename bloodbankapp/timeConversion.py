
def convertTo24Hr(timeString):
    hour = int(timeString.split(':')[0])
    minute = timeString.split(':')[1]
    minute = int(''.join(filter(str.isdigit, minute)))

    if "PM" in timeString:
        hour += 12
    return [hour, minute]


def convertTo12Hr(hour, minute):
    suffix = "AM"
    if hour >= 12:
        if hour != 12:
            hour -= 12
        suffix = "PM"
    return str(hour)+":"+str(minute)+suffix
