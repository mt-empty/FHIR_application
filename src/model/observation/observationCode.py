from enum import Enum

class ObservationCode(Enum):
    """
    the observation code enum class, new observation should be added here

    Args:
        Enum (class): python enum module
    """
    CHOLESTEROL = "2093-3"
    BLOOD_PRESSURE = "55284-4"
    TOBACCO_SMOKING_STATUS_NHIS = "72166-2"
    