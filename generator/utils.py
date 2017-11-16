import time

def writeBatch(file, batch): file.write('\n'.join(batch) + '\n')

logFile = open('logs/' + time.strftime("%d%m%Y%H%M%S") + '.log', 'a')

def log(str = ''):
  line = time.strftime("%d/%m/%Y %H:%M:%S") + ": " + str
  print(line)
  logFile.write(line  + '\n')