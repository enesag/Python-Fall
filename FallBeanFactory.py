from os.path import dirname, basename, join
from importlib.util import spec_from_file_location, module_from_spec

import glob

from PropertyInjector import PropertyInjector
import json_reader
import constants


class FallBeanFactory:
    def __init__(self, beansDir, configFile, configReader=json_reader, propertyReader=json_reader):
        self.beans = dict()
        self.configReader = configReader
        self.beanNames = self.readFilesInBeansDir(beansDir)
        self.beansConfig = self.readBeansConfiguration(configFile)

        propertyPlaceholder = self.beansConfig.get(
            constants.CONFIG_CONTEXT_PROPERTY_PLACEHOLDER_KEY)
        if propertyPlaceholder:
            externalPropertiesPath = propertyPlaceholder[
                constants.CONFIG_CONTEXT_PROPERTY_PLACEHOLDER_LOCATION_KEY]
            self.propertyInjector = PropertyInjector(
                propertyReader, self, externalPropertiesPath)

    def readFilesInBeansDir(self, beansDirPath):
        beans = dict()
        for path in glob.glob(join(dirname(__file__), beansDirPath + constants.BEAN_PREFIX_WILDCARD)):
            beans[basename(path)[:-3]] = path
        return beans

    def readBeansConfiguration(self, configFilePath):
        return self.configReader.read(configFilePath)

    def instantiateBean(self, beanName):
        beanConfig = self.beansConfig[constants.CONFIG_BEANS_KEY][beanName]
        className = beanConfig[constants.CONFIG_CLASS_KEY]

        spec = spec_from_file_location(className, self.beanNames[className])
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        constructorArguments = []
        if constants.CONFIG_CONSTRUCTOR_ARGS_KEY in beanConfig:
            for argument in beanConfig[constants.CONFIG_CONSTRUCTOR_ARGS_KEY]:
                constructorArguments.append(self.getBean(argument))

        bean = getattr(module, className)(*constructorArguments)
        properties = beanConfig.get(constants.CONFIG_PROPERTIES_KEY, None)
        if properties:
            self.propertyInjector.injectProperties(bean, properties)

        return bean

    def getBean(self, beanName):
        if beanName in self.beans:
            return self.beans[beanName]
        else:
            self.beans[beanName] = self.instantiateBean(beanName)
            return self.beans[beanName]
