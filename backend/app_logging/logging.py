from database.logger.LoggerDatabase import LoggerDatabase
class Log:
    @staticmethod
    def logInsert(value):
        LoggerDatabase.logMessageToDB(value)
    @staticmethod
    def emptyLogDb():
        LoggerDatabase.emptyLogDB()

    def getLog():
        return LoggerDatabase.getWholeLog()