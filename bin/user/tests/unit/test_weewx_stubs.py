# pylint: disable=missing-docstring
# pylint: disable=invalid-name
import locale
import sys
import time

class weewx: # pylint: disable=invalid-name
    class units:
        METRIC = 0x10
        METRICWX = 0x11
        US = 0x01

        unit_constants = {
            'US'       : US,
            'METRIC'   : METRIC,
            'METRICWX' : METRICWX
        }

        def to_std_system(self):
            pass

    class accum:
        def Accum(self):
            pass

        class OutOfSpan(ValueError):
            """Raised when attempting to add a record outside of the timespan held by an acumulator"""

    class NEW_LOOP_PACKET(object):
        """Event issued when a new LOOP packet is available. The event contains
        attribute 'packet', which is the new LOOP packet."""
    class engine:
        class StdService(object):
            def __init__(self, engine, config_dict):
                pass
            def bind(self, p1, p2):
                pass
    class drivers: # pylint: disable=invalid-name
        class AbstractDevice:
            pass
        class AbstractConfEditor:
            pass

class weeutil:
    class weeutil():
        class TimeSpan(tuple):
            """Represents a time span, exclusive on the left, inclusive on the right."""

            def __new__(cls, *args):
                if args[0] > args[1]:
                    raise ValueError("start time (%d) is greater than stop time (%d)" % (args[0], args[1]))
                return tuple.__new__(cls, args)

        @staticmethod
        def timestamp_to_string(ts, format_str="%Y-%m-%d %H:%M:%S %Z"):
            if ts is not None:
                return "%s (%d)" % (time.strftime(format_str, time.localtime(ts)), ts)
            else:
                return "******* N/A *******     (    N/A   )"

        @staticmethod
        def _get_object(module_class):
            """Given a string with a module class name, it imports and returns the class."""
            # Split the path into its parts
            parts = module_class.split('.')
            # Strip off the classname:
            module = '.'.join(parts[:-1])
            # Import the top level module
            mod = __import__(module)
            # Recursively work down from the top level module to the class name.
            # Be prepared to catch an exception if something cannot be found.
            try:
                for part in parts[1:]:
                    mod = getattr(mod, part)
            except AttributeError:
                # Can't find something. Give a more informative error message:
                raise AttributeError(
                    "Module '%s' has no attribute '%s' when searching for '%s'" % (mod.__name__, part, module_class))
            return mod

        @staticmethod
        def option_as_list(option):
            if option is None:
                return None
            return [option] if not isinstance(option, list) else option

        @staticmethod
        def to_sorted_string(rec):
            return ", ".join(["%s: %s" % (k, rec.get(k)) for k in sorted(rec, key=locale.strxfrm)])

        @staticmethod
        def to_bool(value):
            try:
                if value.lower() in ['true', 'yes']:
                    return True
                elif value.lower() in ['false', 'no']:
                    return False
            except AttributeError:
                pass
            try:
                return bool(int(value))
            except (ValueError, TypeError):
                pass
            raise ValueError("Unknown boolean specifier: '%s'." % value)

        @staticmethod
        def to_float(value):
            if isinstance(value, str) and value.lower() == 'none':
                value = None
            return float(value) if value is not None else None

        @staticmethod
        def to_int(value):
            return int(value)

UNITS_CONSTANTS = {'US': 1}

class NEW_LOOP_PACKET(object):
    """Event issued when a new LOOP packet is available. The event contains
    attribute 'packet', which is the new LOOP packet."""
class NEW_ARCHIVE_RECORD(object):
    """Event issued when a new archive record is available. The event contains
    attribute 'record', which is the new archive record."""

class Event(object):
    """Represents an event."""
    def __init__(self, event_type, **argv):
        self.event_type = event_type

        for key in argv:
            setattr(self, key, argv[key])

    def __str__(self):
        """Return a string with a reasonable representation of the event."""
        et = "Event type: %s | " % self.event_type
        s = "; ".join("%s: %s" %(k, self.__dict__[k]) for k in self.__dict__ if k != "event_type")
        return et + s

sys.modules['weewx'] = weewx
sys.modules['weewx.drivers'] = weewx.drivers
sys.modules['weewx.engine'] = weewx.engine
sys.modules['weeutil'] = weeutil
sys.modules['weeutil.weeutil'] = weeutil.weeutil