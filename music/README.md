# Music Directory

This directory is for storing phonk music tracks to be used with the autopilot system.

## Supported Formats

- MP3 (.mp3)
- WAV (.wav) 
- FLAC (.flac)
- OGG (.ogg)

## Recommended Music Characteristics

### Phonk Music Specifications
- **BPM Range**: 120-180 BPM (optimal for drift patterns)
- **Key**: Minor keys work best for drift aesthetics
- **Length**: 3-8 minutes recommended
- **Bass**: Strong bass presence enhances the experience

### Audio Quality
- **Sample Rate**: 44.1 kHz or higher
- **Bit Depth**: 16-bit minimum, 24-bit preferred
- **Dynamic Range**: Avoid heavily compressed tracks

## Example Files

Add your phonk tracks here following this naming convention:
- `basic_phonk.mp3` - For basic drift patterns
- `aggressive_phonk.mp3` - For advanced drift patterns  
- `chill_phonk.mp3` - For relaxed driving sessions

## Copyright Notice

⚠️ **IMPORTANT**: Only use music you have the rights to use. Respect copyright laws and licensing requirements.

## Pattern Integration

Reference music files in your pattern YAML files:

```yaml
music_file: "music/your_track.mp3"
```

## Beat Detection

The system will automatically analyze tracks for:
- BPM (beats per minute)
- Beat timing
- Musical structure
- Dynamic sections