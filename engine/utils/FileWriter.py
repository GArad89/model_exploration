
def log(msg, log_path, flag = 'a'):

    if log_path:
        with open(log_path, 'a') as fw:
            fw.write(msg + "\n")
    else:
        print(msg)

