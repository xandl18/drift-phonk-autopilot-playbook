#!/usr/bin/env python3
"""
Drift Phonk Autopilot Playbook - Main Application
Entry point for the synchronized drift phonk autopilot system.
"""

import argparse
import sys
import logging
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent))

from autopilot.controller import AutopilotController
from audio.processor import AudioProcessor
from sync.synchronizer import PatternSynchronizer
from utils.config import ConfigManager
from utils.logger import setup_logging


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Drift Phonk Autopilot Playbook - Synchronized driving experience"
    )
    parser.add_argument(
        "--config", 
        default="config/default.yaml",
        help="Configuration file path (default: config/default.yaml)"
    )
    parser.add_argument(
        "--mode",
        choices=["drift", "simulation", "audio-only"],
        default="simulation",
        help="Operation mode (default: simulation)"
    )
    parser.add_argument(
        "--pattern",
        default="basic_drift",
        help="Drift pattern to use (default: basic_drift)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = ConfigManager(args.config)
        
        # Setup logging
        setup_logging(config.get_logging_config(), debug=args.debug)
        logger = logging.getLogger(__name__)
        
        logger.info(f"Starting Drift Phonk Autopilot in {args.mode} mode")
        logger.info(f"Using pattern: {args.pattern}")
        
        # Initialize components
        autopilot = AutopilotController(config.get_autopilot_config())
        audio = AudioProcessor(config.get_audio_config())
        synchronizer = PatternSynchronizer(config.get_sync_config())
        
        # Safety check
        if args.mode != "simulation" and config.get("development.simulation_only", True):
            logger.warning("Forcing simulation mode due to safety configuration")
            args.mode = "simulation"
            
        # Load pattern
        pattern_path = Path("patterns") / f"{args.pattern}.yaml"
        if not pattern_path.exists():
            logger.error(f"Pattern file not found: {pattern_path}")
            return 1
            
        # Start the synchronized session
        with autopilot, audio, synchronizer:
            if args.mode == "drift":
                logger.info("🚗 Starting drift mode - ENSURE YOU ARE IN A SAFE ENVIRONMENT")
                synchronizer.start_drift_session(autopilot, audio, pattern_path)
            elif args.mode == "simulation":
                logger.info("🎮 Starting simulation mode")
                synchronizer.start_simulation_session(audio, pattern_path)
            elif args.mode == "audio-only":
                logger.info("🎵 Starting audio-only mode")
                synchronizer.start_audio_session(audio, pattern_path)
                
    except KeyboardInterrupt:
        logger.info("Session interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1
        
    logger.info("Session completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())