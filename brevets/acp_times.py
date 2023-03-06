"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    # 20 Percent larger special case. Changing control distance to equal brevet
    # distance.
    if brevet_dist_km < control_dist_km <= brevet_dist_km * 1.2:
        control_dist_km = brevet_dist_km

    # Special Cases
    if control_dist_km == 0:
        return brevet_start_time

    """ALGORITHM:
    Calculates running sum of the time needed to complete each part
    of the brevet. 
    """

    # distance-speed key value pairs
    times_table = {200: 34, 400: 32, 600: 30, 1000: 28, 1300: 26}
    # put distances into list
    distance_list = list(times_table.keys())
    # the difference in distances between speed changes
    diff_in_dist = [200, 200, 200, 400, 300]
    total_hours = 0
    total_minutes = 0
    # location in the times_table (start at 1 b/c using i - 1 to compare prev)
    i = 1

    remaining_distance = control_dist_km - distance_list[i - 1]

    # Calculates sum of each part until distance is < 0
    while remaining_distance > 0 and i < len(diff_in_dist):
        hours = diff_in_dist[i - 1] // times_table[distance_list[i - 1]]
        minutes = ((diff_in_dist[i - 1] / times_table[
            distance_list[i - 1]]) - hours) * 60
        total_hours += hours
        total_minutes += minutes
        i += 1
        remaining_distance = remaining_distance - (diff_in_dist[i - 1])

    # Adds back the distance and calculates the remaining distance of the brevet
    remaining_distance = remaining_distance + (diff_in_dist[i - 1])
    hours = remaining_distance // times_table[distance_list[i - 1]]
    minutes = ((remaining_distance / times_table[
        distance_list[i - 1]]) - hours) * 60
    total_hours += hours
    total_minutes += minutes

    # Fixes overflow of minutes
    while total_minutes > 60:
        total_hours += 1
        total_minutes -= 60

    return brevet_start_time.shift(hours=total_hours,
                                   minutes=round(total_minutes))


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    # 20 Percent larger special case. Changing control distance to equal brevet
    # distance.
    if brevet_dist_km < control_dist_km <= brevet_dist_km * 1.2:
        control_dist_km = brevet_dist_km

    # Special Cases
    if control_dist_km == 0:
        return brevet_start_time.shift(hours=1.0)

    if control_dist_km == 200 and brevet_dist_km == 200:
        return brevet_start_time.shift(hours=13, minutes=30)

    if control_dist_km == 300 and brevet_dist_km == 300:
        return brevet_start_time.shift(hours=20, minutes=0)

    if control_dist_km == 400 and brevet_dist_km == 400:
        return brevet_start_time.shift(hours=27, minutes=0)

    if control_dist_km == 600 and brevet_dist_km == 600:
        return brevet_start_time.shift(hours=40, minutes=0)

    if control_dist_km == 1000 and brevet_dist_km == 1000:
        return brevet_start_time.shift(hours=75, minutes=0)

    if control_dist_km < 60:
        hours = (control_dist_km // 20)
        minutes = ((control_dist_km / 20) - hours) * 60
        return brevet_start_time.shift(hours=hours + 1, minutes=round(minutes))


    """ALGORITHM:
    Calculates running sum of the time needed to complete each part
    of the brevet. 
    """

    # distance-speed key value pairs
    times_table = {600: 15, 1000: 11.428, 1300: 13.333}
    # put distances into list
    distance_list = list(times_table.keys())
    # the difference in distances between speed changes
    diff_in_dist = [600, 400, 300]
    total_hours = 0
    total_minutes = 0
    # location in the times_table (start at 1 b/c using i - 1 to compare prev)
    i = 1

    remaining_distance = control_dist_km - distance_list[i - 1]

    # Calculates sum of each part until distance is < 0
    while remaining_distance > 0 and i < len(diff_in_dist):
        hours = diff_in_dist[i - 1] // times_table[distance_list[i - 1]]
        minutes = ((diff_in_dist[i - 1] / times_table[
            distance_list[i - 1]]) - hours) * 60
        total_hours += hours
        total_minutes += minutes
        i += 1
        remaining_distance = remaining_distance - (diff_in_dist[i - 1])

    # Adds back the distance and calculates the remaining distance of the brevet
    remaining_distance = remaining_distance + (diff_in_dist[i - 1])
    hours = remaining_distance // times_table[distance_list[i - 1]]
    minutes = ((remaining_distance / times_table[
        distance_list[i - 1]]) - hours) * 60
    total_hours += hours
    total_minutes += minutes

    # Fixes overflow of minutes
    while total_minutes > 60:
        total_hours += 1
        total_minutes -= 60

    return brevet_start_time.shift(hours=total_hours,
                                   minutes=round(total_minutes))
