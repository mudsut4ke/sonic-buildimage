#!/usr/bin/env python

from __future__ import print_function

try:
    from sonic_platform_base.sonic_thermal_control.thermal_action_base \
        import ThermalPolicyActionBase
    from sonic_platform_base.sonic_thermal_control.thermal_json_object \
        import thermal_json_object
except ImportError as e:
    raise ImportError("%s - required module not found" % e)


@thermal_json_object('thermal_control.control')
class ControlThermalAlgoAction(ThermalPolicyActionBase):
    """
    Action to control the thermal control algorithm
    """
    # JSON field definition
    JSON_FIELD_STATUS = 'status'

    def __init__(self):
        self.status = True

    def load_from_json(self, json_obj):
        """
        Construct ControlThermalAlgoAction via JSON. JSON example:
            {
                "type": "thermal_control.control"
                "status": "true"
            }
        :param json_obj: A JSON object representing a ControlThermalAlgoAction action.
        :return:
        """
        if ControlThermalAlgoAction.JSON_FIELD_STATUS in json_obj:
            status_str = json_obj[ControlThermalAlgoAction.JSON_FIELD_STATUS].lower(
            )
            if status_str == 'true':
                self.status = True
            elif status_str == 'false':
                self.status = False
            else:
                raise ValueError('Invalid {} field value, please specify true of false'.
                                 format(ControlThermalAlgoAction.JSON_FIELD_STATUS))
        else:
            raise ValueError('ControlThermalAlgoAction '
                             'missing mandatory field {} in JSON policy file'.
                             format(ControlThermalAlgoAction.JSON_FIELD_STATUS))

    def execute(self, thermal_info_dict):
        """
        Disable thermal control algorithm
        :param thermal_info_dict: A dictionary stores all thermal information.
        :return:
        """
        from .thermal_infos import ChassisInfo
        if ChassisInfo.INFO_NAME in thermal_info_dict:
            chassis_info_obj = thermal_info_dict[ChassisInfo.INFO_NAME]
            chassis = chassis_info_obj.get_chassis()
            thermal_manager = chassis.get_thermal_manager()
            if self.status:
                thermal_manager.start_thermal_control_algorithm()
            else:
                thermal_manager.stop_thermal_control_algorithm()


@thermal_json_object('switch.power_cycle')
class SwitchPolicyAction(ThermalPolicyActionBase):
    """
    Base class for thermal action. Once all thermal conditions in a thermal policy are matched,
    all predefined thermal action will be executed.
    """

    def execute(self, thermal_info_dict):
         """
         Take action when thermal condition matches. For example, adjust speed of fan or shut
         down the switch.
         :param thermal_info_dict: A dictionary stores all thermal information.
         :return:
         """
         from helper import APIHelper
         from .thermal import HIGH_CRIT_THRESHOLD

         print(HIGH_CRIT_THRESHOLD)
         print(thermal_info_dict)

         # cmd = 'bash /usr/local/bin/thermal_overload_control.sh {}'.format(thermal_info_dict)

         # APIHelper().run_command(cmd)
