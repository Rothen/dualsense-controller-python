import time
from typing import Any, Final, Callable

import pyee

from dualsense_controller.core.core.Lockable import Lockable
from dualsense_controller.core.enum import ConnectionType
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.state.BaseStates import BaseStates
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.read_state.ReadState import ReadState
from dualsense_controller.core.state.typedef import StateValue
from dualsense_controller.core.state.read_state.more_read_states import (
    LeftJoystickReadState,
    LeftJoystickXReadState,
    LeftJoystickYReadState,
    RightJoystickReadState,
    RightJoystickXReadState,
    RightJoystickYReadState,
    GyroscopeReadState,
    GyroscopeXState,
    GyroscopeYState,
    GyroscopeZState,
    AccelerometerReadState,
    AccelerometerXState,
    AccelerometerYState,
    AccelerometerZState,
    OrientationState,
    DPadReadState,
    DPadUpReadState,
    DPadLeftReadState,
    DPadDownReadState,
    DPadRightReadState,
    ButtonSquareReadState,
    ButtonCrossReadState,
    ButtonCircleReadState,
    ButtonTriangleReadState,
    ButtonL1ReadState,
    ButtonR1ReadState,
    ButtonL2ReadState,
    ButtonR2ReadState,
    ButtonL3ReadState,
    ButtonR3ReadState,
    ButtonCreateReadState,
    ButtonOptionsReadState,
    ButtonPSReadState,
    ButtonTouchpadReadState,
    ButtonMuteReadState,
    TouchFinger1ActiveReadState,
    TouchFinger1IDReadState,
    TouchFinger1XReadState,
    TouchFinger1YReadState,
    TouchFinger1ReadState,
    TouchFinger2ActiveReadState,
    TouchFinger2IDReadState,
    TouchFinger2XReadState,
    TouchFinger2YReadState,
    TouchFinger2ReadState,
    LeftTriggerValueReadState,
    LeftTriggerFeedbackActiveReadState,
    LeftTriggerFeedbackValueReadState,
    LeftTriggerFeedbackReadState,
    RightTriggerValueReadState,
    RightTriggerFeedbackActiveReadState,
    RightTriggerFeedbackValueReadState,
    RightTriggerFeedbackReadState,
    BatteryLevelPercentageReadState,
    BatteryFullReadState,
    BatteryChargingReadState,
    BatteryReadState
)


class ReadStates(BaseStates):
    _EVENT_UPDATE: Final[str] = '_EVENT_UPDATE'

    def __init__(
            self,
            state_value_mapper: StateValueMapper,
            enforce_update: bool = False,
            can_update_itself: bool = True,
    ):
        super().__init__(state_value_mapper)
        # CONST
        self._states_to_trigger_after_all_states_set: Final[list[ReadState[Any]]] = []
        self._in_report_lockable: Final[Lockable[InReport]] = Lockable()
        # VAR
        self._timestamp: int = time.perf_counter_ns()
        self._update_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()

        # INIT STICKS
        self.left_stick: Final[LeftJoystickReadState] = LeftJoystickReadState(
            self._state_value_mapper,
            self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.left_stick_x: Final[LeftJoystickXReadState] = LeftJoystickXReadState(
            self.left_stick,
            self._state_value_mapper,
            self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.left_stick_y: Final[LeftJoystickYReadState] = LeftJoystickYReadState(
            self.left_stick,
            self._state_value_mapper,
            self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.right_stick: Final[RightJoystickReadState] = RightJoystickReadState(
            self._state_value_mapper,
            self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.right_stick_x: Final[RightJoystickXReadState] = RightJoystickXReadState(
            self.right_stick,
            self._state_value_mapper,
            self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.right_stick_y: Final[RightJoystickYReadState] = RightJoystickYReadState(
            self.right_stick,
            self._state_value_mapper,
            self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        # GYRO
        self.gyroscope: Final[GyroscopeReadState] = GyroscopeReadState(
            in_report_lockable=self._in_report_lockable,
            threshold_raw=state_value_mapper.gyroscope_threshold_mapped_to_raw,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.gyroscope_x: Final[GyroscopeXState] = GyroscopeXState(
            self.gyroscope,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)
    
        self.gyroscope_y: Final[GyroscopeYState] = GyroscopeYState(
            self.gyroscope,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)
        
        self.gyroscope_z: Final[GyroscopeZState] = GyroscopeZState(
            self.gyroscope,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        # ACCEL
        self.accelerometer: Final[AccelerometerReadState] = AccelerometerReadState(
            in_report_lockable=self._in_report_lockable,
            threshold_raw=state_value_mapper.accelerometer_threshold_mapped_to_raw,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)

        self.accelerometer_x: Final[AccelerometerXState] = AccelerometerXState(
            self.accelerometer,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)
        
        self.accelerometer_y: Final[AccelerometerYState] = AccelerometerYState(
            self.accelerometer,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself)
        
        self.accelerometer_z: Final[AccelerometerZState] = AccelerometerZState(
            self.accelerometer,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        # ORIENT
        self.orientation: Final[OrientationState] = OrientationState(
            threshold_raw=state_value_mapper.orientation_threshold_mapped_to_raw,
            depends_on=self.accelerometer,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        # INIT DIG BTN
        self.dpad: Final[ReadState[int]] = DPadReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_up: Final[DPadUpReadState] = DPadUpReadState(
            depends_on=self.dpad,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.btn_left: Final[DPadLeftReadState] = DPadLeftReadState(
            depends_on=self.dpad,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.btn_down: Final[DPadDownReadState] = DPadDownReadState(
            depends_on=self.dpad,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.btn_right: Final[DPadRightReadState] = DPadRightReadState(
            depends_on=self.dpad,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        self.btn_square: Final[ButtonSquareReadState] = ButtonSquareReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_cross: Final[ButtonCrossReadState] = ButtonCrossReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_circle: Final[ButtonCircleReadState] = ButtonCircleReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_triangle: Final[ButtonTriangleReadState] = ButtonTriangleReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_l1: Final[ButtonL1ReadState] = ButtonL1ReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_r1: Final[ButtonR1ReadState] = ButtonR1ReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_l2: Final[ButtonL2ReadState] = ButtonL2ReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_r2: Final[ButtonR2ReadState] = ButtonR2ReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_create: Final[ButtonCreateReadState] = ButtonCreateReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_options: Final[ButtonOptionsReadState] = ButtonOptionsReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_l3: Final[ButtonL3ReadState] = ButtonL3ReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_r3: Final[ButtonR3ReadState] = ButtonR3ReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_ps: Final[ButtonPSReadState] = ButtonPSReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_touchpad: Final[ButtonTouchpadReadState] = ButtonTouchpadReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.btn_mute: Final[ButtonMuteReadState] = ButtonMuteReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        # INIT TOUCH
        self.touch_finger_1_active: Final[TouchFinger1ActiveReadState] = TouchFinger1ActiveReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        self.touch_finger_1_id: Final[TouchFinger1IDReadState] = TouchFinger1IDReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        
        self.touch_finger_1_x: Final[TouchFinger1XReadState] = TouchFinger1XReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        
        self.touch_finger_1_y: Final[TouchFinger1YReadState] = TouchFinger1YReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        
        self.touch_finger_1: Final[TouchFinger1ReadState] = TouchFinger1ReadState(
            depends_on=(
                self.touch_finger_1_active,
                self.touch_finger_1_id,
                self.touch_finger_1_x,
                self.touch_finger_1_y
            ),
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.touch_finger_2_active: Final[TouchFinger2ActiveReadState] = TouchFinger2ActiveReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        self.touch_finger_2_id: Final[TouchFinger2IDReadState] = TouchFinger2IDReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        self.touch_finger_2_x: Final[TouchFinger2XReadState] = TouchFinger2XReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        self.touch_finger_2_y: Final[TouchFinger2YReadState] = TouchFinger2YReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )

        self.touch_finger_2: Final[TouchFinger2ReadState] = TouchFinger2ReadState(
            depends_on=(
                self.touch_finger_2_active,
                self.touch_finger_2_id,
                self.touch_finger_2_x,
                self.touch_finger_2_y
            ),
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        # INIT TRIGGERS
        self.left_trigger_value: Final[LeftTriggerValueReadState] = LeftTriggerValueReadState(
            state_value_mapper=self._state_value_mapper,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        
        self.left_trigger_feedback_active: Final[LeftTriggerFeedbackActiveReadState] = LeftTriggerFeedbackActiveReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        
        self.left_trigger_feedback_value: Final[LeftTriggerFeedbackValueReadState] = LeftTriggerFeedbackValueReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        
        self.left_trigger_feedback: Final[LeftTriggerFeedbackReadState] = LeftTriggerFeedbackReadState(
            depends_on=(self.left_trigger_feedback_active, self.left_trigger_feedback_value),
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        
        self.right_trigger_value: Final[RightTriggerValueReadState] = RightTriggerValueReadState(
            state_value_mapper=self._state_value_mapper,
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.right_trigger_feedback_active: Final[RightTriggerFeedbackActiveReadState] = RightTriggerFeedbackActiveReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.right_trigger_feedback_value: Final[RightTriggerFeedbackValueReadState] = RightTriggerFeedbackValueReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
        )
        self.right_trigger_feedback: Final[RightTriggerFeedbackReadState] = RightTriggerFeedbackReadState(
            depends_on=(self.right_trigger_feedback_active, self.right_trigger_feedback_value),
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        # INIT BATT
        self.battery_level_percentage: Final[BatteryLevelPercentageReadState] = BatteryLevelPercentageReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.battery_full: Final[BatteryFullReadState] = BatteryFullReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.battery_charging: Final[BatteryChargingReadState] = BatteryChargingReadState(
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        self.battery: Final[BatteryReadState] = BatteryReadState(
            depends_on=(self.battery_level_percentage, self.battery_full, self.battery_charging),
            in_report_lockable=self._in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )
        
        self._register_state(self.left_stick)
        self._register_state(self.left_stick_x)
        self._register_state(self.left_stick_y)
        self._register_state(self.right_stick)
        self._register_state(self.right_stick_x)
        self._register_state(self.right_stick_y)
        self._register_state(self.gyroscope)
        self._register_state(self.gyroscope_x)
        self._register_state(self.gyroscope_y)
        self._register_state(self.gyroscope_z)
        self._register_state(self.accelerometer)
        self._register_state(self.accelerometer_x)
        self._register_state(self.accelerometer_y)
        self._register_state(self.accelerometer_z)
        self._register_state(self.orientation)
        self._register_state(self.dpad)
        self._register_state(self.btn_up)
        self._register_state(self.btn_left)
        self._register_state(self.btn_down)
        self._register_state(self.btn_right)
        self._register_state(self.btn_square)
        self._register_state(self.btn_cross)
        self._register_state(self.btn_circle)
        self._register_state(self.btn_triangle)
        self._register_state(self.btn_l1)
        self._register_state(self.btn_r1)
        self._register_state(self.btn_l2)
        self._register_state(self.btn_r2)
        self._register_state(self.btn_create)
        self._register_state(self.btn_options)
        self._register_state(self.btn_l3)
        self._register_state(self.btn_r3)
        self._register_state(self.btn_ps)
        self._register_state(self.btn_touchpad)
        self._register_state(self.btn_mute)
        self._register_state(self.touch_finger_1_active)
        self._register_state(self.touch_finger_1_id)
        self._register_state(self.touch_finger_1_x)
        self._register_state(self.touch_finger_1_y)
        self._register_state(self.touch_finger_1)
        self._register_state(self.touch_finger_2_active)
        self._register_state(self.touch_finger_2_id)
        self._register_state(self.touch_finger_2_x)
        self._register_state(self.touch_finger_2_y)
        self._register_state(self.touch_finger_2)
        self._register_state(self.left_trigger_value)
        self._register_state(self.left_trigger_feedback_active)
        self._register_state(self.left_trigger_feedback_value)
        self._register_state(self.left_trigger_feedback)
        self._register_state(self.right_trigger_value)
        self._register_state(self.right_trigger_feedback_active)
        self._register_state(self.right_trigger_feedback_value)
        self._register_state(self.right_trigger_feedback)
        self._register_state(self.battery_level_percentage)
        self._register_state(self.battery_full)
        self._register_state(self.battery_charging)
        self._register_state(self.battery)

    # #################### PRIVATE #######################

    def _handle_state(
            self,
            state: ReadState[StateValue],
    ) -> None:
        state.set_cycle_timestamp(self._timestamp)
        if state.is_updatable_from_outside:
            state.calc_value(trigger_change_on_changed=False)
            self._states_to_trigger_after_all_states_set.append(state)

    def _post_update(self):
        self._update_emitter.emit(self._EVENT_UPDATE)
        for state in self._states_to_trigger_after_all_states_set:
            state.trigger_change_if_changed()
        self._states_to_trigger_after_all_states_set.clear()

    # #################### PUBLIC #######################

    def on_updated(self, callback: Callable[[], None]) -> None:
        self._update_emitter.on(self._EVENT_UPDATE, callback)

    def once_updated(self, callback: Callable[[], None]) -> None:
        self._update_emitter.once(self._EVENT_UPDATE, callback) # type: ignore

    def update(self, in_report: InReport, connection_type: ConnectionType) -> None:

        now_timestamp: int = time.perf_counter_ns()

        self._timestamp = now_timestamp
        self._in_report_lockable.value = in_report

        # #### ANALOG STICKS #####

        self._handle_state(self.left_stick)
        # use values from stick because deadzone_raw calc is done there
        self._handle_state(self.left_stick_x)
        self._handle_state(self.left_stick_y)

        self._handle_state(self.right_stick)
        # use values from stick because deadzone_raw calc is done there
        self._handle_state(self.right_stick_x)
        self._handle_state(self.right_stick_y)

        # # ##### TRIGGERS #####
        self._handle_state(self.left_trigger_value)
        self._handle_state(self.right_trigger_value)
        #
        # # ##### BUTTONS #####
        self._handle_state(self.dpad)
        self._handle_state(self.btn_up)
        self._handle_state(self.btn_down)
        self._handle_state(self.btn_left)
        self._handle_state(self.btn_right)

        self._handle_state(self.btn_cross)
        self._handle_state(self.btn_r1)
        self._handle_state(self.btn_square)
        self._handle_state(self.btn_circle)
        self._handle_state(self.btn_triangle)
        self._handle_state(self.btn_l1)
        self._handle_state(self.btn_l2)
        self._handle_state(self.btn_r2)
        self._handle_state(self.btn_create)
        self._handle_state(self.btn_options)
        self._handle_state(self.btn_l3)
        self._handle_state(self.btn_r3)
        self._handle_state(self.btn_ps)
        self._handle_state(self.btn_mute)
        self._handle_state(self.btn_touchpad)

        # following not supported for BT01
        if connection_type == ConnectionType.BT_01:
            self._post_update()
            return

        # ##### GYRO #####

        self._handle_state(self.gyroscope)
        self._handle_state(self.gyroscope_x)
        self._handle_state(self.gyroscope_y)
        self._handle_state(self.gyroscope_z)
        #
        # ##### ACCEL #####
        self._handle_state(self.accelerometer)
        self._handle_state(self.accelerometer_x)
        self._handle_state(self.accelerometer_y)
        self._handle_state(self.accelerometer_z)
        #
        # ##### ORIENTATION #####
        self._handle_state(self.orientation)
        #
        # ##### TOUCH 1 #####
        self._handle_state(self.touch_finger_1_active)
        self._handle_state(self.touch_finger_1_id)
        self._handle_state(self.touch_finger_1_x)
        self._handle_state(self.touch_finger_1_y)
        self._handle_state(self.touch_finger_1)

        # ##### TOUCH 2 #####
        self._handle_state(self.touch_finger_2_active)
        self._handle_state(self.touch_finger_2_id)
        self._handle_state(self.touch_finger_2_x)
        self._handle_state(self.touch_finger_2_y)
        self._handle_state(self.touch_finger_2)

        # ##### TRIGGER FEEDBACK INFO #####
        self._handle_state(self.left_trigger_feedback_active)
        self._handle_state(self.left_trigger_feedback_value)
        self._handle_state(self.left_trigger_feedback)
        self._handle_state(self.right_trigger_feedback_active)
        self._handle_state(self.right_trigger_feedback_value)
        self._handle_state(self.right_trigger_feedback)
        # ##### BATTERY #####
        self._handle_state(self.battery_level_percentage)
        self._handle_state(self.battery_full)
        self._handle_state(self.battery_charging)
        self._handle_state(self.battery)
        self._post_update()
