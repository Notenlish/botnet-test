import threading

with open("script_to_send.txt", "r")as f:
    script = f.read()

with open("got_script.py", "w") as f:
    f.write(script)

from got_script import run
t = threading.Thread(target=run, name="name", args=())
# t.daemon = True
t.start()
t.join()