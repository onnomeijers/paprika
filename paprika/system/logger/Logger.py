import inspect
from paprika.repositories.PropertyRepository import PropertyRepository


class Logger(object):
    def __init__(self, connector, parent):
        object.__init__(self)
        self.__parent = parent
        self.__appenders = []
        self.__connector = connector
        self.__properties = PropertyRepository(connector)
        self.__levels = {"trace": 0, "debug": 1, "info": 2, "warn": 3, "fatal": 4}
        self.load_appenders()

    def get_connector(self):
        return self.__connector

    def load_appenders(self):
        connector = self.get_connector()
        properties = self.get_properties()
        appenders = properties.get_property('application.log.appenders')
        appenders = appenders.split(';')
        for appender in appenders:
            if appender == 'console':
                from paprika.system.logger.ConsoleAppender import ConsoleAppender
                self.__appenders.append(ConsoleAppender)
            if appender == 'database':
                from paprika.system.logger.DatabaseAppender import DatabaseAppender
                self.__appenders.append(DatabaseAppender(connector))
            if appender == 'syslog':
                from paprika.system.logger.SyslogAppender import SyslogAppender
                self.__appenders.append(SyslogAppender)

    def get_appenders(self):
        return self.__appenders

    def get_properties(self):
        return self.__properties

    def get_levels(self):
        return self.__levels

    def get_parent(self):
        return self.__parent

    def insert(self, message):
        appenders = self.get_appenders()
        for appender in appenders:
            appender.write(message)

    def trace(self, job_name, message, backtrace=''):
        properties = self.get_properties()

        log_level = properties.get_property('application.loglevel').lower()
        levels = self.get_levels()
        if levels[log_level] <= levels['trace']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "trace", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def debug(self, job_name, message, backtrace=''):
        properties = self.get_properties()

        log_level = properties.get_property('application.loglevel').lower()
        levels = self.get_levels()
        if levels[log_level] <= levels['debug']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "debug", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def info(self, job_name, message, backtrace=''):
        properties = self.get_properties()

        log_level = properties.get_property('application.loglevel').lower()
        levels = self.get_levels()
        if levels[log_level] <= levels['info']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "info", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def warn(self, job_name, message, backtrace=''):
        properties = self.get_properties()

        log_level = properties.get_property('application.loglevel').lower()
        levels = self.get_levels()
        if levels[log_level] <= levels['warn']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "warn", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)

    def fatal(self, job_name, message, backtrace=''):
        properties = self.get_properties()

        log_level = properties.get_property('application.loglevel').lower()
        levels = self.get_levels()
        if levels[log_level] <= levels['fatal']:
            parent = self.get_parent()
            package_name = parent.__class__.__name__
            method_name = inspect.stack()[1][3]

            message = {"job_name": job_name, "logtype_code": "fatal", "message": message, "package_name": package_name, "method_name": method_name, "backtrace": backtrace}
            self.insert(message)