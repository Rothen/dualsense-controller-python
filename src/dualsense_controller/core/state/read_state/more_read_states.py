from functools import partial

from dualsense_controller.core.core.Lockable import Lockable
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.state.mapping.StateValueMapper import StateValueMapper
from dualsense_controller.core.state.read_state.ReadState import ReadState
from dualsense_controller.core.state.read_state.ValueCalc import ValueCalc
from dualsense_controller.core.state.read_state.ValueCompare import ValueCompare
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.read_state.value_type import Accelerometer, Battery, Gyroscope, JoyStick, \
    Orientation, TouchFinger, TriggerFeedback
from dualsense_controller.core.state.typedef import CompareFn, CompareResult, Number, StateValue, StateValueFn, default_compare_fn
from dualsense_controller.core.util import check_value_restrictions
from dualsense_controller.core.state.mapping.typedef import MapFn
from dualsense_controller.core.state.mapping.common import FromTo

ENFORCE_UPDATE_DEFAULT: bool = False
CAN_UPDATE_ITSELF_DEFAULT: bool = True

class JoystickReadState(ReadState[JoyStick]):
    def __init__(self,
                 name: ReadStateName,
                 value_calc_fn: StateValueFn[JoyStick],
                 deadzone_raw: Number,
                 raw_to_mapped_fn: MapFn,
                 mapped_to_raw_fn: MapFn,
                 in_report_lockable: Lockable[InReport],
                 middle_deadzone: Number,
                 from_to_x: FromTo | None = None,
                 from_to_y: FromTo | None = None,
                 enforce_update: bool = ENFORCE_UPDATE_DEFAULT,
                 can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT
                 ):
        super().__init__(
            name=name,
            in_report_lockable=in_report_lockable,
            value_calc_fn=value_calc_fn,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=self.compare_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            mapped_to_raw_fn=mapped_to_raw_fn
        )

        self.deadzone_raw: Number = deadzone_raw

        check_value_restrictions(
            name=str(name),
            middle_deadzone=middle_deadzone,
            mapped_min_max_values=[
                (from_to_x.to_min if from_to_x is not None else 0),
                (from_to_x.to_max if from_to_x is not None else 255),
                (from_to_y.to_min if from_to_y is not None else 0),
                (from_to_y.to_max if from_to_y is not None else 255),
            ]
        )

    def compare_fn(self, a: JoyStick, b: JoyStick) -> CompareResult[JoyStick]:
        return ValueCompare.compare_joystick(a, b, self.deadzone_raw)


class TriggerValueReadState(ReadState[int]):
    def __init__(self,
                 name: ReadStateName,
                 value_calc_fn: StateValueFn[int],
                 deadzone_raw: Number,
                 raw_to_mapped_fn: MapFn,
                 mapped_to_raw_fn: MapFn,
                 in_report_lockable: Lockable[InReport],
                 from_to: FromTo | None = None,
                 enforce_update: bool = ENFORCE_UPDATE_DEFAULT,
                 can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT
                 ):
        super().__init__(
            name=name,
            in_report_lockable=in_report_lockable,
            value_calc_fn=value_calc_fn,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=self.compare_fn,
            raw_to_mapped_fn=raw_to_mapped_fn,
            mapped_to_raw_fn=mapped_to_raw_fn
        )

        self.deadzone_raw: Number = deadzone_raw

        check_value_restrictions(
            name=str(name),
            mapped_min_max_values=[
                (from_to.to_min if from_to is not None else 0),
                (from_to.to_max if from_to is not None else 255),
            ]
        )

    def compare_fn(self, a: int, b: int) -> CompareResult[int]:
        return ValueCompare.compare_trigger_value(a, b, self.deadzone_raw)


class LeftJoystickReadState(JoystickReadState):
    def __init__(self, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_STICK,
            value_calc_fn=ValueCalc.get_left_stick,
            deadzone_raw=state_value_mapper.left_stick_deadzone_mapped_to_raw,
            raw_to_mapped_fn=state_value_mapper.left_stick_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.left_stick_mapped_to_raw,
            middle_deadzone=state_value_mapper.left_stick_deadzone_mapped,
            from_to_x=state_value_mapper.mapping_data.left_stick_x if state_value_mapper.mapping_data is not None else None,
            from_to_y=state_value_mapper.mapping_data.left_stick_y if state_value_mapper.mapping_data is not None else None,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class RightJoystickReadState(JoystickReadState):
    def __init__(self, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_STICK,
            value_calc_fn=ValueCalc.get_right_stick,
            deadzone_raw=state_value_mapper.right_stick_deadzone_mapped_to_raw,
            raw_to_mapped_fn=state_value_mapper.right_stick_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.right_stick_mapped_to_raw,
            middle_deadzone=state_value_mapper.right_stick_deadzone_mapped,
            from_to_x=state_value_mapper.mapping_data.right_stick_x if state_value_mapper.mapping_data is not None else None,
            from_to_y=state_value_mapper.mapping_data.right_stick_y if state_value_mapper.mapping_data is not None else None,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class LeftJoystickXReadState(ReadState[int]):
    def __init__(self, depends_on: LeftJoystickReadState, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_STICK_X,
            value_calc_fn=ValueCalc.get_left_stick_x,
            in_report_lockable=in_report_lockable,
            depends_on=(depends_on, ),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=state_value_mapper.left_stick_x_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.left_stick_x_mapped_to_raw
        )


class LeftJoystickYReadState(ReadState[int]):
    def __init__(self, depends_on: LeftJoystickReadState, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_STICK_Y,
            value_calc_fn=ValueCalc.get_left_stick_y,
            in_report_lockable=in_report_lockable,
            depends_on=(depends_on, ),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=state_value_mapper.left_stick_y_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.left_stick_y_mapped_to_raw
        )


class RightJoystickXReadState(ReadState[int]):
    def __init__(self, depends_on: RightJoystickReadState, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_STICK_X,
            value_calc_fn=ValueCalc.get_right_stick_x,
            in_report_lockable=in_report_lockable,
            depends_on=(depends_on, ),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=state_value_mapper.right_stick_x_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.right_stick_x_mapped_to_raw
        )


class RightJoystickYReadState(ReadState[int]):
    def __init__(self, depends_on: RightJoystickReadState, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_STICK_Y,
            value_calc_fn=ValueCalc.get_right_stick_y,
            in_report_lockable=in_report_lockable,
            depends_on=(depends_on, ),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            raw_to_mapped_fn=state_value_mapper.right_stick_y_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.right_stick_y_mapped_to_raw
        )


class GyroscopeReadState(ReadState[Gyroscope]):
    def __init__(self, threshold_raw: Number, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.GYROSCOPE,
            value_calc_fn=ValueCalc.get_gyroscope,
            in_report_lockable=in_report_lockable,
            default_value=Gyroscope(),
            compare_fn=self.compare,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        self.threshold_raw = threshold_raw
        # self.threshold = threshold

    def compare(self, a: Gyroscope, b: Gyroscope) -> CompareResult[Gyroscope]:
        return ValueCompare.compare_gyroscope(a, b, self.threshold_raw)


class GyroscopeXState(ReadState[int]):
    def __init__(self, depends_on: GyroscopeReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.GYROSCOPE_X,
            depends_on=(depends_on, ),
            value_calc_fn=ValueCalc.get_gyroscope_x,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class GyroscopeYState(ReadState[int]):
    def __init__(self, depends_on: GyroscopeReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.GYROSCOPE_Y,
            depends_on=(depends_on, ),
            value_calc_fn=ValueCalc.get_gyroscope_y,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class GyroscopeZState(ReadState[int]):
    def __init__(self, depends_on: GyroscopeReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.GYROSCOPE_Z,
            depends_on=(depends_on, ),
            value_calc_fn=ValueCalc.get_gyroscope_z,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class AccelerometerReadState(ReadState[Accelerometer]):
    def __init__(self, threshold_raw: Number, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.ACCELEROMETER,
            value_calc_fn=ValueCalc.get_accelerometer,
            in_report_lockable=in_report_lockable,
            default_value=Accelerometer(),
            compare_fn=self.compare,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )

        self.threshold_raw = threshold_raw

    def compare(self, a: Accelerometer, b: Accelerometer) -> CompareResult[Accelerometer]:
        return ValueCompare.compare_accelerometer(a, b, self.threshold_raw)


class AccelerometerXState(ReadState[int]):
    def __init__(self, depends_on: AccelerometerReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.ACCELEROMETER_X,
            depends_on=(depends_on, ),
            value_calc_fn=ValueCalc.get_accelerometer_x,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class AccelerometerYState(ReadState[int]):
    def __init__(self, depends_on: AccelerometerReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.ACCELEROMETER_Y,
            depends_on=(depends_on, ),
            value_calc_fn=ValueCalc.get_accelerometer_y,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class AccelerometerZState(ReadState[int]):
    def __init__(self, depends_on: AccelerometerReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.ACCELEROMETER_Z,
            depends_on=(depends_on, ),
            value_calc_fn=ValueCalc.get_accelerometer_z,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class OrientationState(ReadState[Orientation]):
    def __init__(self, threshold_raw: Number, depends_on: AccelerometerReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.ORIENTATION,
            value_calc_fn=ValueCalc.get_orientation,
            in_report_lockable=in_report_lockable,
            default_value=Orientation(0, 0, 0),
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=(depends_on, ),
            compare_fn=self.compare
        )
        
        self.threshold_raw = threshold_raw
    
    def compare(self, a: Orientation, b: Orientation) -> CompareResult[Orientation]:
        return ValueCompare.compare_orientation(a, b, self.threshold_raw)


class DPadReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.DPAD,
            value_calc_fn=ValueCalc.get_dpad,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class DPadUpReadState(ReadState[int]):
    def __init__(self, depends_on: DPadReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_UP,
            value_calc_fn=ValueCalc.get_btn_up,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=(depends_on, ),
        )


class DPadLeftReadState(ReadState[int]):
    def __init__(self, depends_on: DPadReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_LEFT,
            value_calc_fn=ValueCalc.get_btn_left,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=(depends_on, ),
        )


class DPadDownReadState(ReadState[int]):
    def __init__(self, depends_on: DPadReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_DOWN,
            value_calc_fn=ValueCalc.get_btn_down,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=(depends_on, ),
        )


class DPadRightReadState(ReadState[int]):
    def __init__(self, depends_on: DPadReadState, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_RIGHT,
            value_calc_fn=ValueCalc.get_btn_right,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            depends_on=(depends_on, ),
        )


class ButtonSquareReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_SQUARE,
            value_calc_fn=ValueCalc.get_btn_square,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonCrossReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_CROSS,
            value_calc_fn=ValueCalc.get_btn_cross,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonCircleReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_CIRCLE,
            value_calc_fn=ValueCalc.get_btn_circle,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonTriangleReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_TRIANGLE,
            value_calc_fn=ValueCalc.get_btn_triangle,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonL1ReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_L1,
            value_calc_fn=ValueCalc.get_btn_l1,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonR1ReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_R1,
            value_calc_fn=ValueCalc.get_btn_l1,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonL2ReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_L2,
            value_calc_fn=ValueCalc.get_btn_l2,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonR2ReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_R2,
            value_calc_fn=ValueCalc.get_btn_l2,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonL3ReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_L3,
            value_calc_fn=ValueCalc.get_btn_l3,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonR3ReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_R3,
            value_calc_fn=ValueCalc.get_btn_l3,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonCreateReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_CREATE,
            value_calc_fn=ValueCalc.get_btn_create,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonOptionsReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_OPTIONS,
            value_calc_fn=ValueCalc.get_btn_options,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonPSReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_PS,
            value_calc_fn=ValueCalc.get_btn_ps,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonTouchpadReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_TOUCHPAD,
            value_calc_fn=ValueCalc.get_btn_touchpad,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class ButtonMuteReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BTN_MUTE,
            value_calc_fn=ValueCalc.get_btn_mute,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger1ActiveReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_1_ACTIVE,
            value_calc_fn=ValueCalc.get_touch_finger_1_active,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger1IDReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_1_ID,
            value_calc_fn=ValueCalc.get_touch_finger_1_id,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger1XReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_1_X,
            value_calc_fn=ValueCalc.get_touch_finger_1_x,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger1YReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_1_Y,
            value_calc_fn=ValueCalc.get_touch_finger_1_y,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger1ReadState(ReadState[TouchFinger]):
    def __init__(self,
                 depends_on: tuple[TouchFinger1ActiveReadState, TouchFinger1IDReadState, TouchFinger1XReadState, TouchFinger1YReadState],
                 in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_1,
            value_calc_fn=ValueCalc.get_touch_finger_1,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_touch_finger,
            depends_on=depends_on
        )


class TouchFinger2ActiveReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_2_ACTIVE,
            value_calc_fn=ValueCalc.get_touch_finger_2_active,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger2IDReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_2_ID,
            value_calc_fn=ValueCalc.get_touch_finger_2_id,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger2XReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_2_X,
            value_calc_fn=ValueCalc.get_touch_finger_2_x,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger2YReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_2_Y,
            value_calc_fn=ValueCalc.get_touch_finger_2_y,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class TouchFinger2ReadState(ReadState[TouchFinger]):
    def __init__(self,
                 depends_on: tuple[TouchFinger2ActiveReadState, TouchFinger2IDReadState, TouchFinger2XReadState, TouchFinger2YReadState],
                 in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.TOUCH_FINGER_2,
            value_calc_fn=ValueCalc.get_touch_finger_2,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_touch_finger,
            depends_on=depends_on
        )


class LeftTriggerValueReadState(TriggerValueReadState):
    def __init__(self, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_TRIGGER_VALUE,
            value_calc_fn=ValueCalc.get_left_trigger_value,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            deadzone_raw=state_value_mapper.left_trigger_deadzone_mapped_to_raw,
            raw_to_mapped_fn=state_value_mapper.left_trigger_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.left_trigger_mapped_to_raw,
            from_to=state_value_mapper.mapping_data.left_trigger if state_value_mapper.mapping_data is not None else None
        )


class LeftTriggerFeedbackActiveReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_TRIGGER_FEEDBACK_ACTIVE,
            value_calc_fn=ValueCalc.get_left_trigger_feedback_active,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class LeftTriggerFeedbackValueReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_TRIGGER_FEEDBACK_VALUE,
            value_calc_fn=ValueCalc.get_left_trigger_feedback_value,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class LeftTriggerFeedbackReadState(ReadState[TriggerFeedback]):
    def __init__(self, depends_on: tuple[LeftTriggerFeedbackActiveReadState, LeftTriggerFeedbackValueReadState], in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.LEFT_TRIGGER_FEEDBACK,
            value_calc_fn=ValueCalc.get_left_trigger_feedback,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_trigger_feedback,
            depends_on=depends_on
        )


class RightTriggerValueReadState(TriggerValueReadState):
    def __init__(self, state_value_mapper: StateValueMapper, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_TRIGGER_VALUE,
            value_calc_fn=ValueCalc.get_right_trigger_value,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            deadzone_raw=state_value_mapper.right_trigger_deadzone_mapped_to_raw,
            raw_to_mapped_fn=state_value_mapper.right_trigger_raw_to_mapped,
            mapped_to_raw_fn=state_value_mapper.right_trigger_mapped_to_raw,
            from_to=state_value_mapper.mapping_data.right_trigger if state_value_mapper.mapping_data is not None else None
        )


class RightTriggerFeedbackActiveReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_TRIGGER_FEEDBACK_ACTIVE,
            value_calc_fn=ValueCalc.get_right_trigger_feedback_active,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class RightTriggerFeedbackValueReadState(ReadState[int]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_TRIGGER_FEEDBACK_VALUE,
            value_calc_fn=ValueCalc.get_right_trigger_feedback_value,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself
        )


class RightTriggerFeedbackReadState(ReadState[TriggerFeedback]):
    def __init__(self, depends_on: tuple[RightTriggerFeedbackActiveReadState, RightTriggerFeedbackValueReadState], in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.RIGHT_TRIGGER_FEEDBACK,
            value_calc_fn=ValueCalc.get_right_trigger_feedback,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_trigger_feedback,
            depends_on=depends_on
        )


class BatteryLevelPercentageReadState(ReadState[float]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BATTERY_LEVEL_PERCENT,
            value_calc_fn=ValueCalc.get_battery_level_percentage,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False
        )


class BatteryFullReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BATTERY_FULL,
            value_calc_fn=ValueCalc.get_battery_full,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False
        )


class BatteryChargingReadState(ReadState[bool]):
    def __init__(self, in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BATTERY_CHARGING,
            value_calc_fn=ValueCalc.battery_charging,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            ignore_none=False
        )


class BatteryReadState(ReadState[Battery]):
    def __init__(self, depends_on: tuple[BatteryLevelPercentageReadState, BatteryFullReadState, BatteryChargingReadState], in_report_lockable: Lockable[InReport], enforce_update: bool = ENFORCE_UPDATE_DEFAULT, can_update_itself: bool = CAN_UPDATE_ITSELF_DEFAULT):
        super().__init__(
            name=ReadStateName.BATTERY,
            value_calc_fn=ValueCalc.get_battery,
            in_report_lockable=in_report_lockable,
            enforce_update=enforce_update,
            can_update_itself=can_update_itself,
            compare_fn=ValueCompare.compare_battery,
            ignore_none=False,
            depends_on=depends_on
        )
