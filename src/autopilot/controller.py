"""
Autopilot controller module for managing automated driving systems.
"""

import logging
from typing import Dict, Any
from abc import ABC, abstractmethod


class AutopilotInterface(ABC):
    """Abstract interface for autopilot systems."""
    
    @abstractmethod
    def start(self) -> None:
        """Start the autopilot system."""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stop the autopilot system."""
        pass
    
    @abstractmethod
    def set_speed(self, speed: float) -> None:
        """Set target speed."""
        pass
    
    @abstractmethod
    def set_steering(self, angle: float) -> None:
        """Set steering angle."""
        pass


class SimulationAutopilot(AutopilotInterface):
    """Simulation autopilot for testing and development."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize simulation autopilot."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.active = False
        self.current_speed = 0.0
        self.current_steering = 0.0
        
    def start(self) -> None:
        """Start simulation autopilot."""
        self.logger.info("🎮 Starting simulation autopilot")
        self.active = True
        
    def stop(self) -> None:
        """Stop simulation autopilot."""
        self.logger.info("⏹️  Stopping simulation autopilot")
        self.active = False
        self.current_speed = 0.0
        self.current_steering = 0.0
        
    def set_speed(self, speed: float) -> None:
        """Set simulated speed."""
        if self.active:
            max_speed = self.config.get('max_speed', 25)
            self.current_speed = min(speed, max_speed)
            self.logger.debug(f"Simulation speed: {self.current_speed} mph")
            
    def set_steering(self, angle: float) -> None:
        """Set simulated steering angle."""
        if self.active:
            # Clamp steering to reasonable range
            self.current_steering = max(-1.0, min(1.0, angle))
            self.logger.debug(f"Simulation steering: {self.current_steering}")


class AutopilotController:
    """Main autopilot controller that manages different autopilot implementations."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize autopilot controller.
        
        Args:
            config: Autopilot configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize appropriate autopilot based on provider
        provider = config.get('provider', 'simulation')
        
        if provider == 'simulation':
            self.autopilot = SimulationAutopilot(config)
        elif provider == 'tesla':
            # Placeholder for Tesla integration
            self.logger.warning("Tesla autopilot not implemented - using simulation")
            self.autopilot = SimulationAutopilot(config)
        elif provider == 'comma':
            # Placeholder for Comma AI integration
            self.logger.warning("Comma AI autopilot not implemented - using simulation")
            self.autopilot = SimulationAutopilot(config)
        else:
            self.logger.warning(f"Unknown provider '{provider}' - using simulation")
            self.autopilot = SimulationAutopilot(config)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure autopilot is stopped."""
        self.stop()
    
    def start(self) -> None:
        """Start the autopilot system."""
        if self.config.get('safety_mode', True):
            self.logger.info("🛡️  Safety mode enabled")
        self.autopilot.start()
    
    def stop(self) -> None:
        """Stop the autopilot system."""
        self.autopilot.stop()
    
    def set_speed(self, speed: float) -> None:
        """Set autopilot speed."""
        self.autopilot.set_speed(speed)
    
    def set_steering(self, angle: float) -> None:
        """Set autopilot steering."""
        self.autopilot.set_steering(angle)