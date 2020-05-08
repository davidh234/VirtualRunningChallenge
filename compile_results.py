lines = []  # raw lines from log file


# A class for each runner. This is the class that gets updated for each line in the log file
class Runner:
    name = ""
    distance = 0.00
    overall_time_minutes = 0
    overall_time_secs = 0
    lap_time = 0.00
    run_count = 0

    def __init__(self, name, distance, overall_time_minutes, overall_time_secs, lap_time, run_count):
        self.name = name
        self.distance = distance
        self.overall_time_minutes = overall_time_minutes
        self.overall_time_secs = overall_time_secs
        self.lap_time = lap_time
        self.run_count = run_count


# This is a class to hold information about each line in the log file, in a more accessible way.
class Log:
    runner = ""
    activity = ""
    distance = 0.0
    time_minutes = 0
    time_seconds = 0
    date = ""
    verified = False

    def __init__(self, runner, activity, dist, time_mins, time_secs, date, verified):
        self.runner = runner
        self.activity = activity
        self.distance = dist
        self.time_minutes = time_mins
        self.time_seconds = time_secs
        self.date = date
        self.verified = verified


# This method reads the log file, and adds each line to the 'lines' list. After finishing, 'lines' now holds all lines
# in the log file.
def read_file():
    file = open("runs.log", "r")
    for line in file:
        lines.append(line)


# This is the main method for calculating each persons stats. It begins by initialising each runner with stats of zero,
# and then proceeds to tally up the statistics for each runner.
def calculate_runners_stats():
    d = Runner('D', 0.0, 0.0, 0.0, 0.0, 0)
    b = Runner('B', 0.0, 0.0, 0.0, 0.0, 0)
    g = Runner('G', 0.0, 0.0, 0.0, 0.0, 0)
    p = Runner('P', 0.0, 0.0, 0.0, 0.0, 0)

    runners_list = [d, b, g, p]
    process_file(runners_list)


# Parses each line of the log file read earlier, and then adjusts the appropriate runners stats based on that line.
def process_file(runners_list):
    for line in lines:
        log = parse_line(line)

        for runner in runners_list:
            if log.runner == runner.name:
                if log.activity == 'ran':
                    runner.distance += log.distance
                    runner.run_count += 1
                    updated_time = calculate_overall_time(runner.overall_time_minutes, runner.overall_time_secs,
                                                          log.time_minutes, log.time_seconds)
                    runner.overall_time_minutes = updated_time[0:2]
                    runner.overall_time_secs = updated_time[3:5]
                    split = split_time(runner.overall_time_minutes, runner.overall_time_secs, float(runner.distance))
                    runner.lap_time = split

    output_runners_results(runners_list)


# Just a print method for displaying the results once the processing has finished.
def output_runners_results(runners_list):
    sort_by_distance(runners_list)
    for runner in runners_list:
        print('name: ', runner.name, ' , distance travelled: ', round(runner.distance, 2), ' , overall time: ',
              runner.overall_time_minutes, ':', runner.overall_time_secs, ' , lap time: ', runner.lap_time,
              ', run count: ', runner.run_count)


# given the finished list of runners, sorts them by distance.
def sort_by_distance(runner_list):
    runner_list.sort(key=lambda x: x.distance, reverse=True)
    return runner_list


# This calculates a runners overall time based on adding the new time in the log line to
# the old time they had up until this point
def calculate_overall_time(old_time_mins, old_time_secs, new_time_mins, new_time_secs):
    old_mins = int(old_time_mins)
    old_secs = int(old_time_secs)
    new_mins = int(new_time_mins)
    new_secs = int(new_time_secs)

    old_converted = (old_mins * 60) + old_secs
    new_converted = (new_mins * 60) + new_secs

    total_converted = old_converted + new_converted

    total_mins = int(total_converted / 60)
    total_secs = total_converted % 60

    return str(total_mins) + ':' + str(total_secs)


# This calculates the runners 'per/KM' time or split time. It does this by looking at the overall time and distance.
def split_time(overall_time_mins, overall_time_secs, overall_dist):
    converted_time = (int(overall_time_mins) * 60) + int(overall_time_secs)
    split_in_secs = float(converted_time) / float(overall_dist)
    secs_mod = int(round(split_in_secs % 60))

    split_mins = int(split_in_secs / 60)
    return str(split_mins) + ':' + str(secs_mod)


# This method parses each log line. Given an english string, its job is to extract the important information, and
# put it into a Log object, for easier processing.
def parse_line(line):
    tokens = str.split(line)
    name = tokens[0][1]
    activity = tokens[1]
    dist = tokens[2][0:4]
    time_mins = tokens[4][0:2]
    time_secs = tokens[5][0:2]
    date = tokens[7]
    verified_token = tokens[8]

    if verified_token == '(verified)':
        verified = True
    else:
        verified = False
    log = Log(name, activity, float(dist), time_mins, time_secs, date, verified)
    return log


# These are the driver methods. Without these the code will not actually execute.
read_file()
calculate_runners_stats()
