import time


def timer_func(seconds, start_time):
    while True:
        #print('Pin high - normal operation')
        current_time = time.time()
        elapsed_time = current_time - start_time 
        if elapsed_time > seconds:
            print('Pin low - No water')
            break
    return 0
