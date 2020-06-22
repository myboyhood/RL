import gym
import plane_env
import time
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios
import threading

msg = """
Control plane !

you can control acc_y,

acc_x is automatically calculated :
---------------------------
q : +1 , w : +2 , e : +3
a : -1 , s : -2 , d : -3
x : 0

CTRL-C to quit current episode
"""

e = """
Communications Failed
"""

class getkeyThread (threading.Thread):
    def __init__(self, threadID, name, variable, ExitFlag):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.key = variable
        self.ExitFlag = ExitFlag
    def run(self):
        while self.ExitFlag:
            self.key = input('input key:\t')
        print('Exit thread1')

def getKey():
    if os.name == 'nt':
        return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def constrain(input, low, high):
    if input < low:
        input = low
    elif input > high:
        input = high
    else:
        input = input

    return input

if __name__=="__main__":
    env = gym.make("PlaneEnv-v3")
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
    key = 'x'
    ExitFlag = 1
    thread1 = getkeyThread(1, "getkey", key, ExitFlag)
    thread1.start()
    episodes = 1
    status = 0
    a = 0
    print(msg)
    for i in range(episodes):
        s = env.reset()


        while(1):
            env.render()

            # print('what key get:  %s\n' % thread1.key)
            if thread1.key == 'q':
                a = 0.5
                print("acc_y: +0.5\n")

            elif thread1.key == 'w':
                a = 1
                print("acc_y: +1\n")

            elif thread1.key == 'e':
                a = 1.5
                print("acc_y: +1.5\n")

            elif thread1.key == 'a':
                a = -0.5
                print("acc_y: -0.5\n")

            elif thread1.key == 's':
                a = -1
                print("acc_y: -1\n")

            elif thread1.key == 'd':
                a = -1.5
                print("acc_y: -1.5\n")

            elif thread1.key == 'x':
                a = 0
                print("acc_y: 0\n")

            else:
                if (thread1.key == '\x03'):
                    print("ctrl + c")
                    break

            # time.sleep(1)

            # 执行动作
            next_s, reward, done, _ = env.step(a)

            if done:
                print('reach goal or out')
                break
            # if out:
            #     print('out of field')
            #     break

    thread1.ExitFlag = 0

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)