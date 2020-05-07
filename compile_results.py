lines = []  # raw lines from log file


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


class Log:
    runner = ""
    distance = 0.0
    time_minutes = 0
    time_seconds = 0
    date = ""
    verified = False

    def __init__(self, runner, dist, time_mins, time_secs, date, verified):
        self.runner = runner
        self.distance = dist
        self.time_minutes = time_mins
        self.time_seconds = time_secs
        self.date = date
        self.verified = verified


def read_file():
    file = open("runs.log", "r")
    i = 0
    for line in file:
        lines.append(line)
        i += 1


def init_runners():
    d = Runner('D', 0.0, 0.0, 0.0, 0.0, 0)
    b = Runner('B', 0.0, 0.0, 0.0, 0.0, 0)
    g = Runner('G', 0.0, 0.0, 0.0, 0.0, 0)
    p = Runner('P', 0.0, 0.0, 0.0, 0.0, 0)

    runners_list = [d, b, g, p]
    process_file(runners_list)


def process_file(runners_list):
    for line in lines:
        log = parse_line(line)

        # ********** CHECK THAT ITS A RUN ****************
        for runner in runners_list:
            if log.runner == runner.name:
                runner.distance += log.distance
                runner.run_count += 1
                updated_time = calculate_overall_time(runner.overall_time_minutes, runner.overall_time_secs, log.time_minutes, log.time_seconds)
                runner.overall_time_minutes = updated_time[0:2]
                runner.overall_time_secs = updated_time[3:5]
                split = split_time(runner.overall_time_minutes, runner.overall_time_secs, float(runner.distance))
                runner.lap_time = split
                print(split)


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


def split_time(overall_time_mins, overall_time_secs, overall_dist):
    converted_time = (int(overall_time_mins) * 60) + int(overall_time_secs)
    split_in_secs = float(converted_time) / float(overall_dist)
    secs_mod = float(converted_time) % overall_dist

    split_mins = split_in_secs / 60
    return str(split_mins) + ':' + str(secs_mod)


def parse_line(line):
    tokens = str.split(line)
    name = tokens[0][1]
    dist = tokens[2][0:3]
    time_mins = tokens[4][0:2]
    time_secs = tokens[5][0:2]
    date = tokens[7]
    verified_token = tokens[8]

    if verified_token == '(verified)':
        verified = True
    else:
        verified = False
    log = Log(name, float(dist), time_mins, time_secs, date, verified)
    return log


read_file()
init_runners()
# process_file()
