from typing import TypedDict
from enum import Enum, auto

from Enums.MotionAttributes import *
from Enums.PropTypes import PropTypes


class LetterType(Enum):
    Type1 = (
        [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ],
        "Type1",
    )
    Type2 = (["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"], "Type2")
    Type3 = (["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"], "Type3")
    Type4 = (["Φ", "Ψ", "Λ"], "Type4")
    Type5 = (["Φ-", "Ψ-", "Λ-"], "Type5")
    Type6 = (["α", "β", "Γ"], "Type6")

    def __init__(self, letters, description):
        self._letters = letters
        self._description = description

    @property
    def letters(self):
        return self._letters

    @property
    def description(self):
        return self._description

    @staticmethod
    def get_letter_type(str: str) -> "LetterType":
        for letter_type in LetterType:
            if str in letter_type.letters:
                return letter_type


class MotionCombinationType(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


class ArrowAttribute(Enum):
    COLOR = "color"
    LOC = "loc"
    MOTION_TYPE = "motion_type"
    TURNS = "turns"


class PropAttribute(Enum):
    COLOR = "color"
    PROP_TYPE = "prop_type"
    LOC = "loc"
    ORI = "ori"


class MotionAttribute(Enum):
    COLOR = "color"
    ARROW = "arrow"
    PROP = "prop"
    MOTION_TYPE = "motion_type"
    PROP_ROT_DIR = "prop_rot_dir"
    TURNS = "turns"
    START_LOC = "start_loc"
    START_ORI = "start_ori"
    END_LOC = "end_loc"
    END_ORI = "end_ori"


class OrientationCombination(Enum):
    IN_VS_IN = "in_vs_in"
    IN_VS_CLOCK_IN = "in_vs_clock-in"
    IN_VS_CLOCK = "in_vs_clock"
    IN_VS_CLOCK_OUT = "in_vs_clock-out"
    IN_VS_OUT = "in_vs_out"
    IN_VS_COUNTER_OUT = "in_vs_counter-out"
    IN_VS_COUNTER = "in_vs_counter"
    IN_VS_COUNTER_IN = "in_vs_counter-in"
    CLOCK_IN_VS_CLOCK_IN = "clock-in_vs_clock-in"
    CLOCK_IN_VS_CLOCK = "clock-in_vs_clock"
    CLOCK_IN_VS_CLOCK_OUT = "clock-in_vs_clock-out"
    CLOCK_IN_VS_OUT = "clock-in_vs_out"
    CLOCK_IN_VS_COUNTER_OUT = "clock-in_vs_counter-out"
    CLOCK_IN_VS_COUNTER = "clock-in_vs_counter"
    CLOCK_IN_VS_COUNTER_IN = "clock-in_vs_counter-in"
    CLOCK_VS_CLOCK = "clock_vs_clock"
    CLOCK_VS_CLOCK_OUT = "clock_vs_clock-out"
    CLOCK_VS_OUT = "clock_vs_out"
    CLOCK_VS_COUNTER_OUT = "clock_vs_counter-out"
    CLOCK_VS_COUNTER = "clock_vs_counter"
    CLOCK_VS_COUNTER_IN = "clock_vs_counter-in"
    CLOCK_OUT_VS_CLOCK_OUT = "clock-out_vs_clock-out"
    CLOCK_OUT_VS_OUT = "clock-out_vs_out"
    CLOCK_OUT_VS_COUNTER_OUT = "clock-out_vs_counter-out"
    CLOCK_OUT_VS_COUNTER = "clock-out_vs_counter"
    CLOCK_OUT_VS_COUNTER_IN = "clock-out_vs_counter-in"
    OUT_VS_OUT = "out_vs_out"
    OUT_VS_COUNTER_OUT = "out_vs_counter-out"
    OUT_VS_COUNTER = "out_vs_counter"
    OUT_VS_COUNTER_IN = "out_vs_counter-in"
    COUNTER_OUT_VS_COUNTER_OUT = "counter-out_vs_counter-out"
    COUNTER_OUT_VS_COUNTER = "counter-out_vs_counter"
    COUNTER_OUT_VS_COUNTER_IN = "counter-out_vs_counter-in"
    COUNTER_VS_COUNTER = "counter_vs_counter"
    COUNTER_VS_COUNTER_IN = "counter_vs_counter-in"
    COUNTER_IN_VS_COUNTER_IN = "counter-in_vs_counter-in"


### MOTION ATTRIBUTES ###
class MotionAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    prop_rot_dir: PropRotDirs
    loc: Locations
    turns: Turns
    start_loc: Locations
    start_ori: Orientations
    end_loc: Locations
    end_ori: Orientations


class ArrowAttributesDicts(TypedDict):
    color: Colors
    motion_type: MotionTypes
    location: Locations
    turns: Turns


class PropAttributesDicts(TypedDict):
    color: Colors
    prop_type: PropTypes
    loc: Locations
    ori: Orientations


### LETTER GROUPS ###
class MotionTypeCombination(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class MotionTypeLetterGroups(Enum):
    PRO_VS_PRO = "ADGJMPS"
    ANTI_VS_ANTI = "BEHKNQT"
    STATIC_VS_STATIC = "αβΓ"
    PRO_VS_ANTI = "CFILORUV"
    STATIC_VS_PRO = "WYΣθ"
    STATIC_VS_ANTI = "XZΔΩ"
    DASH_VS_PRO = "W-Y-Σ-θ-"
    DASH_VS_ANTI = "X-Z-Δ-Ω-"
    DASH_VS_STATIC = "ΦΨΛ"
    DASH_VS_DASH = "Φ-Ψ-Λ-"


class VTG_Modes(Enum):
    TOG_SAME = "TS"
    TOG_OPP = "TO"
    SPLIT_SAME = "SS"
    SPLIT_OPP = "SO"
    QUARTER_TIME_SAME = "QTS"
    QUARTER_TIME_OPP = "QTO"


class TKAHandpathMode(Enum):
    ALPHA_TO_ALPHA = "α→α"  # ABC
    BETA_TO_ALPHA = "β→α"  # DEF
    BETA_TO_BETA = "β→β"  # GHI
    ALPHA_TO_BETA = "α→β"  # JKL
    GAMMA_TO_GAMMA_OPP_ANTIPARALLEL = "Γ→Γ_opp_antiparallel"  # MNO
    GAMMA_TO_GAMMA_OPP_PARALLEL = "Γ→Γ_opp_parallel"  # PQR
    GAMMA_TO_GAMMA_SAME_DIR = "Γ→Γ_same"  # STUV

    GAMMACLOCK_TO_GAMMACLOCK = "Γclock→Γclock"
    GAMMACLOCK_TO_GAMMACOUNTER = "Γclock→Γcounter"
    GAMMACOUNTER_TO_GAMMACOUNTER = "Γcounter→Γcounter"
    GAMMACOUNTER_TO_GAMMACLOCK = "Γcounter→Γclock"


class PictographType(Enum):
    MAIN = "main"
    OPTION = "option"
    BEAT = "beat"
    START_POS = "start_pos"
    CODEX_PICTOGRAPH = "codex_pictograph"


class MotionTypeCombination(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class LetterGroupsByMotionType(Enum):
    ADGJMPS = "ADGJMPS"
    BEHKNQT = "BEHKNQT"
    αβΓ = "αβΓ"
    CFILORUV = "CFILORUV"
    WYΣθ = "WYΣθ"
    XZΔΩ = "XZΔΩ"
    X_Z_Δ_Ω_ = "X-Z-Δ-Ω-"
    ΦΨΛ = "ΦΨΛ"
    Φ_Ψ_Λ_ = "Φ-Ψ-Λ-"


class TabName(Enum):
    MOTION_TYPE = auto()
    COLOR = auto()
    LEAD_STATE = auto()


from enum import Enum


class ParallelCombinationsSet(Enum):
    SET = "set"


class Handpaths(Enum):
    DASH_HANDPATH = "dash_handpath"
    STATIC_HANDPATH = "static_handpath"
    CW_HANDPATH = "cw_handpath"
    CCW_HANDPATH = "ccw_handpath"


class RotationAngles(Enum):
    ANGLE_0 = 0
    ANGLE_90 = 90
    ANGLE_180 = 180
    ANGLE_270 = 270


class OptimalLocationEntries(Enum):
    X = "x"
    Y = "y"


class StartEndLocationTuple(Enum):
    LOCATIONS = "Locations"


class OptimalLocationDicts(Enum):
    DICT = "dict"


class Positions(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


class SpecificPositions(Enum):
    ALPHA1 = "alpha1"
    ALPHA2 = "alpha2"
    ALPHA3 = "alpha3"
    ALPHA4 = "alpha4"
    BETA1 = "beta1"
    BETA2 = "beta2"
    BETA3 = "beta3"
    BETA4 = "beta4"
    GAMMA1 = "gamma1"
    GAMMA2 = "gamma2"
    GAMMA3 = "gamma3"
    GAMMA4 = "gamma4"
    GAMMA5 = "gamma5"
    GAMMA6 = "gamma6"
    GAMMA7 = "gamma7"
    GAMMA8 = "gamma8"


class ShiftHandpaths(Enum):
    CW_HANDPATH = "cw_handpath"
    CCW_HANDPATH = "ccw_handpath"


class HexColors(Enum):
    COLOR_1 = "#ED1C24"
    COLOR_2 = "#2E3192"


class Directions(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class GridModes(Enum):
    DIAMOND = "diamond"
    BOX = "box"


class RadialOrientations(Enum):
    IN = "in"
    OUT = "out"


class NonRadialOrientations(Enum):
    CLOCK = "clock"
    COUNTER = "counter"


class OrientationTypes(Enum):
    RADIAL = "radial"
    NONRADIAL = "nonradial"


class Axes(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class MotionTypeCombinations(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class VTG_Timings(Enum):
    SPLIT = "split"
    TOGETHER = "together"


class VTG_Directions(Enum):
    SAME = "same"
    OPP = "opp"


class OpenCloseStates(Enum):
    OPEN = "open"
    CLOSE = "close"


class Letters(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    Σ = "Σ"
    Δ = "Δ"
    θ = "θ"
    Ω = "Ω"
    W_DASH = "W-"
    X_DASH = "X-"
    Y_DASH = "Y-"
    Z_DASH = "Z-"
    Σ_DASH = "Σ-"
    Δ_DASH = "Δ-"
    θ_DASH = "θ-"
    Ω_DASH = "Ω-"
    Φ = "Φ"
    Ψ = "Ψ"
    Λ = "Λ"
    Φ_DASH = "Φ-"
    Ψ_DASH = "Ψ-"
    Λ_DASH = "Λ-"
    α = "α"
    β = "β"
    Γ = "Γ"


class AdjustmentStrs(Enum):
    MINUS_1 = "-1"
    MINUS_0_5 = "-0.5"
    PLUS_1 = "+1"
    PLUS_0_5 = "+0.5"


class AdjustmentNums(Enum):
    FLOAT = float
    INT = int


class LetterTypeDescriptions(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


class MotionAttributes(Enum):
    COLOR = "color"
    ARROW = "arrow"
    PROP = "prop"
    MOTION_TYPE = "motion_type"
    PROP_ROT_DIR = "prop_rot_dir"
    TURNS = "turns"
    START_LOC = "start_loc"
    START_ORI = "start_ori"
    END_LOC = "end_loc"
    END_ORI = "end_ori"
    LEAD_STATE = "lead_state"


class Pictograph_Key(Enum):
    KEY = str


class PictographAttributesDict(TypedDict):
    letter: Letters
    start_pos: SpecificPositions
    end_pos: SpecificPositions
    blue_motion_type: MotionTypes
    blue_prop_rot_dir: PropRotDirs
    blue_start_loc: Locations
    blue_end_loc: Locations
    blue_turns: Turns
    blue_start_ori: Orientations
    blue_end_ori: Orientations
    red_motion_type: MotionTypes
    red_prop_rot_dir: PropRotDirs
    red_start_loc: Locations
    red_end_loc: Locations
    red_turns: Turns
    red_start_ori: Orientations
    red_end_ori: Orientations