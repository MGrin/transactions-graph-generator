import time

logFile = open('logs/' + time.strftime("%d%m%Y%H%M%S") + '.log', 'a+')

def writeBatch(file, batch): file.write('\n'.join(batch) + '\n')

def log(str = ''):
  line = time.strftime("%d/%m/%Y %H:%M:%S") + ": " + str
  print(line)
  logFile.write(line  + '\n')
