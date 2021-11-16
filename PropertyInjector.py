import re

from utils import generateSetterName
import constants


class PropertyInjector():
    def __init__(self, propertyReader, fallContext, externalPropertiesPath):
        self.fallContext = fallContext
        self.propertyReader = propertyReader
        if (externalPropertiesPath):
            self.externalProperties = self.readExternalProperties(
                externalPropertiesPath)

    def readExternalProperties(self, externalPropertiesPath):
        return self.propertyReader.read(externalPropertiesPath)

    def injectProperties(self, bean, properties):
        for property in properties:
            setter = getattr(bean, generateSetterName(
                property[constants.CONFIG_PROPERTY_NAME_KEY]))

            if constants.CONFIG_PROPERTY_REF_KEY in property:
                setter(self.fallContext.getBean(
                    property[constants.CONFIG_PROPERTY_REF_KEY]))
            else:
                def externalPropertyReplacer(match):
                    return self.externalProperties.get(match.group(1), match.group(0))
                value = re.sub(constants.EXTERNAL_PROPERTY_KEY_REGEX,
                               externalPropertyReplacer, property[constants.CONFIG_PROPERTY_VALUE_KEY])
                setter(value)
