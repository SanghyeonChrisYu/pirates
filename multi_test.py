# 멀티프로세싱을 위한 Process 클래스

# 그저 하나의 프로세스를 하나의 함수에 적당한 인자값을 할당해주고(없을 수도 있음) 진행

import time
import os
from multiprocessing import Process

def func():
    print('연속적으로 진행하고자 하는 어떤 작업')
    time.sleep(1)
    
def doubler(number):
    result = number + 10
    func()
    proc = os.getpid()
    print('number : {0}, result : {1}, process id : {2}'.format(number, result, proc))
    
if __name__ == '__main__':
    numbers = range(0,1000)
    procs = []

    tempTime = time.time()
    
    for index, number in enumerate(numbers):
        proc = Process(target = doubler, args = (number,))
        procs.append(proc) # 프로세스의 join()을 추가할 의도
        proc.start() # doubler 함수가 호출
        
    for proc in procs:
        proc.join() # 끝날 때 까지 기다림
    
    print(f"{time.time() - tempTime} secs")
