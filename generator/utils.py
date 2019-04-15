import time

logFile = open('logs/' + time.strftime("%H.%M.%S_%d-%m-%Y") + '.log', 'a+')

def writeBatch(file, batch): file.write('\n'.join(batch) + '\n')

def log(str = ''):
  line = time.strftime("%d/%m/%Y %H:%M:%S") + ": " + str
  print(line)
  logFile.write(line  + '\n')
