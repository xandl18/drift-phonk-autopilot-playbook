"""
Pattern synchronization module for coordinating music and autopilot.
"""

import logging
import yaml
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from autopilot.controller import AutopilotController
    from audio.processor import AudioProcessor


class PatternSynchronizer:
    """Synchronizes drift patterns with phonk music."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize pattern synchronizer.
        
        Args:
            config: Synchronization configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.beat_detection = config.get('beat_detection', True)
        self.pattern_timing = config.get('pattern_timing', 'auto')
        self.visual_feedback = config.get('visual_feedback', True)
        
        self.active = False
        self.current_pattern: Optional[Dict[str, Any]] = None
        self.sync_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop synchronization."""
        self.stop()
    
    def load_pattern(self, pattern_path: Path) -> bool:
        """Load a drift pattern from YAML file.
        
        Args:
            pattern_path: Path to the pattern file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not pattern_path.exists():
                # Create a basic pattern if file doesn't exist
                self.current_pattern = self._create_basic_pattern()
                self.logger.info(f"Created basic pattern (file not found: {pattern_path})")
                return True
                
            with open(pattern_path, 'r') as f:
                self.current_pattern = yaml.safe_load(f)
                
            self.logger.info(f"📋 Loaded pattern: {pattern_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load pattern {pattern_path}: {e}")
            return False
    
    def start_drift_session(self, autopilot: 'AutopilotController', 
                          audio: 'AudioProcessor', pattern_path: Path) -> None:
        """Start synchronized drift session.
        
        Args:
            autopilot: Autopilot controller instance
            audio: Audio processor instance
            pattern_path: Path to the drift pattern
        """
        self.logger.info("🚗🎵 Starting synchronized drift session")
        
        if not self.load_pattern(pattern_path):
            self.logger.error("Failed to load pattern - aborting session")
            return
        
        # Safety check
        self.logger.warning("⚠️  ENSURE YOU ARE IN A SAFE, CLOSED ENVIRONMENT ⚠️")
        time.sleep(3)  # Give user time to read warning
        
        # Start components
        autopilot.start()
        audio.start()
        
        # Load and play music
        music_file = self.current_pattern.get('music_file', 'music/default_phonk.mp3')
        if audio.load_track(music_file):
            audio.play()
        
        # Start synchronization
        self._start_sync_loop(autopilot, audio)
    
    def start_simulation_session(self, audio: 'AudioProcessor', pattern_path: Path) -> None:
        """Start simulation session (no actual autopilot).
        
        Args:
            audio: Audio processor instance
            pattern_path: Path to the drift pattern
        """
        self.logger.info("🎮🎵 Starting simulation session")
        
        if not self.load_pattern(pattern_path):
            self.logger.error("Failed to load pattern - aborting session")
            return
        
        # Start audio
        audio.start()
        
        # Load and play music
        music_file = self.current_pattern.get('music_file', 'music/default_phonk.mp3')
        if audio.load_track(music_file):
            audio.play()
        
        # Start simulation loop
        self._start_simulation_loop(audio)
    
    def start_audio_session(self, audio: 'AudioProcessor', pattern_path: Path) -> None:
        """Start audio-only session.
        
        Args:
            audio: Audio processor instance
            pattern_path: Path to the drift pattern
        """
        self.logger.info("🎵 Starting audio-only session")
        
        if not self.load_pattern(pattern_path):
            self.logger.error("Failed to load pattern - aborting session")
            return
        
        # Start audio
        audio.start()
        
        # Load and play music
        music_file = self.current_pattern.get('music_file', 'music/default_phonk.mp3')
        if audio.load_track(music_file):
            audio.play()
        
        # Simple playback loop
        try:
            while True:
                time.sleep(1.0)
                if self.visual_feedback:
                    beat_phase = audio.get_current_beat_phase()
                    self.logger.info(f"🎵 Beat: {beat_phase:.2f}")
        except KeyboardInterrupt:
            self.logger.info("Audio session stopped by user")
    
    def stop(self) -> None:
        """Stop synchronization."""
        self.logger.info("⏹️  Stopping synchronization")
        self.active = False
        self.stop_event.set()
        
        if self.sync_thread and self.sync_thread.is_alive():
            self.sync_thread.join(timeout=2.0)
    
    def _start_sync_loop(self, autopilot: 'AutopilotController', 
                        audio: 'AudioProcessor') -> None:
        """Start the main synchronization loop.
        
        Args:
            autopilot: Autopilot controller instance
            audio: Audio processor instance
        """
        self.active = True
        self.stop_event.clear()
        
        self.sync_thread = threading.Thread(
            target=self._sync_loop,
            args=(autopilot, audio),
            daemon=True
        )
        self.sync_thread.start()
        
        # Wait for session to complete
        try:
            self.sync_thread.join()
        except KeyboardInterrupt:
            self.logger.info("Session interrupted by user")
            self.stop()
    
    def _start_simulation_loop(self, audio: 'AudioProcessor') -> None:
        """Start simulation loop.
        
        Args:
            audio: Audio processor instance
        """
        self.active = True
        
        try:
            while self.active:
                beat_phase = audio.get_current_beat_phase()
                
                if self.visual_feedback:
                    # Show visual feedback
                    self.logger.info(f"🎮 Simulation - Beat: {beat_phase:.2f}")
                
                time.sleep(2.0)  # Update every 2 seconds
                
        except KeyboardInterrupt:
            self.logger.info("Simulation stopped by user")
    
    def _sync_loop(self, autopilot: 'AutopilotController', audio: 'AudioProcessor') -> None:
        """Main synchronization loop.
        
        Args:
            autopilot: Autopilot controller instance
            audio: Audio processor instance
        """
        self.logger.info("Starting synchronization loop")
        
        # Get pattern steps
        steps = self.current_pattern.get('steps', [])
        step_index = 0
        
        while self.active and not self.stop_event.is_set():
            if not steps:
                time.sleep(1.0)
                continue
            
            # Get current step
            step = steps[step_index % len(steps)]
            
            # Execute step based on beat timing
            beat_phase = audio.get_current_beat_phase()
            
            if self.pattern_timing == 'beat' and beat_phase < 0.1:  # On beat
                self._execute_step(autopilot, step)
                step_index += 1
                time.sleep(0.2)  # Avoid multiple executions per beat
            elif self.pattern_timing == 'auto':
                self._execute_step(autopilot, step)
                step_index += 1
                time.sleep(step.get('duration', 2.0))
            
            if self.visual_feedback:
                self.logger.info(f"🚗 Step {step_index}: {step.get('name', 'Unknown')}")
    
    def _execute_step(self, autopilot: 'AutopilotController', step: Dict[str, Any]) -> None:
        """Execute a single pattern step.
        
        Args:
            autopilot: Autopilot controller instance
            step: Pattern step configuration
        """
        speed = step.get('speed', 15.0)
        steering = step.get('steering', 0.0)
        
        autopilot.set_speed(speed)
        autopilot.set_steering(steering)
    
    def _create_basic_pattern(self) -> Dict[str, Any]:
        """Create a basic drift pattern.
        
        Returns:
            Basic pattern configuration
        """
        return {
            'name': 'Basic Drift',
            'description': 'Simple drift pattern for demonstration',
            'music_file': 'music/default_phonk.mp3',
            'steps': [
                {'name': 'Straight', 'speed': 20.0, 'steering': 0.0, 'duration': 3.0},
                {'name': 'Left Drift', 'speed': 15.0, 'steering': -0.7, 'duration': 2.0},
                {'name': 'Recover', 'speed': 18.0, 'steering': 0.3, 'duration': 1.5},
                {'name': 'Right Drift', 'speed': 15.0, 'steering': 0.7, 'duration': 2.0},
                {'name': 'Recover', 'speed': 18.0, 'steering': -0.3, 'duration': 1.5},
            ]
        }