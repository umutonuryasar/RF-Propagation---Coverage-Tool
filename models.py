import numpy as np
from scipy.constants import c

# Constants for models
RADIUS_OF_EARTH = 6371e3  # in meters, used in some models
TIREM_CONSTANT = 0.1  # Placeholder constant for TIREM model

### 1. Free Space Propagation Model ###
def free_space_path_loss(frequency, distance):
    """
    Calculate the Free Space Path Loss (FSPL) in dB.
    
    :param frequency: Frequency in MHz
    :param distance: Distance in km
    :return: Path loss in dB
    """
    wavelength = c / (frequency * 1e6)  # Convert frequency to Hz and calculate wavelength
    fspl = 20 * np.log10(distance * 1e3) + 20 * np.log10(frequency) + 20 * np.log10(4 * np.pi / c)
    return fspl

### 2. Rain Propagation Model ###
def rain_attenuation(frequency, distance, rain_rate):
    """
    Calculate the rain attenuation in dB/km.
    
    :param frequency: Frequency in GHz
    :param distance: Distance in km
    :param rain_rate: Rainfall rate in mm/h
    :return: Rain attenuation in dB
    """
    # Simplified rain attenuation model (ITU-R P.838-3)
    k = 0.0001 * frequency ** 0.72  # Attenuation coefficient (depends on frequency)
    alpha = 0.9  # Power-law exponent
    rain_loss = k * rain_rate ** alpha * distance
    return rain_loss

### 3. Gas Propagation Model ###
def gas_attenuation(frequency, distance):
    """
    Calculate the gas attenuation in dB/km.
    
    :param frequency: Frequency in GHz
    :param distance: Distance in km
    :return: Gas attenuation in dB
    """
    # Simplified model assuming dry air at standard temperature and pressure
    specific_attenuation = 0.05 * frequency  # Attenuation factor for dry air
    gas_loss = specific_attenuation * distance
    return gas_loss

### 4. Fog Propagation Model ###
def fog_attenuation(frequency, distance, fog_density):
    """
    Calculate the fog attenuation in dB/km.
    
    :param frequency: Frequency in GHz
    :param distance: Distance in km
    :param fog_density: Fog density in g/m³
    :return: Fog attenuation in dB
    """
    # Simplified fog attenuation model
    specific_attenuation = 0.2 * fog_density * frequency ** 2
    fog_loss = specific_attenuation * distance
    return fog_loss

### 5. Close-In Propagation Model ###
def close_in_path_loss(frequency, distance, reference_distance=1):
    """
    Calculate the Close-In (CI) Path Loss model in dB.
    
    :param frequency: Frequency in MHz
    :param distance: Distance in km
    :param reference_distance: Reference distance in meters (default is 1 meter)
    :return: Path loss in dB
    """
    path_loss_exponent = 2  # Free-space path loss exponent
    close_in_loss = 20 * np.log10(distance / reference_distance) + 20 * np.log10(frequency) + 20 * np.log10(4 * np.pi / c)
    return close_in_loss

### 6. Longley-Rice Propagation Model ###
def longley_rice_path_loss(frequency, distance, terrain_type="average"):
    """
    Estimate the Longley-Rice path loss.
    
    :param frequency: Frequency in MHz
    :param distance: Distance in km
    :param terrain_type: Terrain type (default is "average")
    :return: Path loss in dB
    """
    # Placeholder model - real Longley-Rice is much more complex
    terrain_factor = {"average": 0.5, "hilly": 1.0, "mountainous": 2.0}
    factor = terrain_factor.get(terrain_type, 0.5)
    longley_rice_loss = factor * (20 * np.log10(frequency) + 20 * np.log10(distance) + 32.45)
    return longley_rice_loss

### 7. TIREM Propagation Model ###
def tirem_path_loss(frequency, distance, terrain_type="average"):
    """
    Estimate the TIREM path loss.
    
    :param frequency: Frequency in MHz
    :param distance: Distance in km
    :param terrain_type: Terrain type (default is "average")
    :return: Path loss in dB
    """
    # Placeholder model - real TIREM is more complex and requires specific data
    terrain_factor = {"average": 0.8, "hilly": 1.2, "mountainous": 1.5}
    factor = terrain_factor.get(terrain_type, 0.8)
    tirem_loss = factor * (20 * np.log10(frequency) + 20 * np.log10(distance) + TIREM_CONSTANT)
    return tirem_loss

### 8. Ray Tracing Propagation Model ###
def ray_tracing_path_loss(frequency, distance, environment="urban"):
    """
    Estimate the Ray Tracing path loss.
    
    :param frequency: Frequency in GHz
    :param distance: Distance in km
    :param environment: Environment type ("urban", "rural", etc.)
    :return: Path loss in dB
    """
    # Simplified ray tracing model with basic reflection and diffraction losses
    env_factor = {"urban": 3.0, "rural": 1.5}
    factor = env_factor.get(environment, 3.0)
    ray_tracing_loss = factor * (20 * np.log10(frequency) + 20 * np.log10(distance) + 10 * np.log10(4 * np.pi / c))
    return ray_tracing_loss
