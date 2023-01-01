import threading
import time


# Run all the given actions (functions) in parallel for a certain number of
# seconds. Each action should accept one parameter: an event that is set when
# the threads should exit.
#
# Example:
# def thread1(stop_evt):
#     while not stop_evt.is_set():
#         print("Thread 1")
#         time.sleep(2)
#
#
# def thread2(stop_evt):
#     while not stop_evt.is_set():
#         print("Thread 2")
#         time.sleep(1)
#
# The first thread will print 5 times, and the second will print 10 times.
# run_in_parallel(10, (thread1, thread2))
def run_in_parallel(seconds, actions, arguments):
    stop_event = threading.Event()

    threads = []
    for index in range(0, len(actions)):
        thread = threading.Thread(target=actions[index], args=(*arguments[index], stop_event,))
        thread.start()
        threads.append(thread)

    time.sleep(seconds)
    stop_event.set()

    for thread in threads:
        thread.join()
