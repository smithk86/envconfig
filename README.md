#  pyenvprops

## Description

This module offers the ability to define and set application
properties using both a property file and enviornment variables.
It was originally intended to ease application configuration
for apps running in Docker containers.

The property file can be formatted in JSON or YAML. A "properties"
object is defined in the file. Each entry should be an object
with at least a "type" field. The supported types are defined
in EnvProps.supported_datatypes. The key of the object will be
name of the property. This is also the name of the enviornment
variable for which the parser will check. Optionally, a "default"
field can be defined for each property which will specify a value
to use if one is not provided via the enviornment. If no default is
provided, EnvProps will throw an exception if no value is found
in the enviornment.

## Examples

Please see [files/properties.json](https://github.com/smithk86/pyenvprops/blob/master/files/properties.json) and [files/properties.yaml](https://github.com/smithk86/pyenvprops/blob/master/files/properties.yaml) for property file examples.

## Using with Flask/Quart

~~~
from envprops import EnvProps
from flask import Flask

app = Flask(__name__)
env = EnvProps('properties.json')
app.config.update(env.asdict())
~~~
