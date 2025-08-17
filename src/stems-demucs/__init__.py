"""
Python API for audio separation using Demucs
"""
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, List

class DemucsWrapper:
    """Wrapper class for Demucs audio separation"""
    
    AVAILABLE_MODELS = [
        "htdemucs",      # Hybrid Transformer Demucs
        "htdemucs_ft",   # Fine-tuned version (recommended)
        "mdx_extra",     # MDX model
        "mdx_extra_q",   # Quantized MDX model
    ]
    
    def __init__(self, model: str = "htdemucs_ft", device: str = "cpu"):
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model {model} not supported. Available: {self.AVAILABLE_MODELS}")
        
        self.model = model
        self.device = device
    
    def separate(self, 
                input_path: str, 
                output_dir: Optional[str] = None,
                stems: Optional[List[str]] = None) -> Path:
        """
        Separate audio into stems
        
        Args:
            input_path: Path to input audio file
            output_dir: Output directory (uses temp if None)
            stems: List of stems to extract (None for all)
        
        Returns:
            Path to output directory containing stems
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Use temp directory if no output specified
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="demucs_")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Build command
        cmd = [
            "python", "-m", "demucs",
            "-n", self.model,
            "-d", self.device,
            "-o", str(output_path),
            str(input_path)
        ]
        
        # Run separation
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Separation completed: {result.stdout}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Demucs separation failed: {e.stderr}")
        
        return output_path / self.model / input_path.stem
    
    def get_stems(self, separated_dir: Path) -> dict:
        """Get paths to separated stem files"""
        stems = {}
        stem_names = ["drums", "bass", "other", "vocals"]
        
        for stem in stem_names:
            stem_file = separated_dir / f"{stem}.wav"
            if stem_file.exists():
                stems[stem] = stem_file
        
        return stems

# Example usage function
def quick_separate(input_file: str, model: str = "htdemucs_ft") -> dict:
    """
    Quick separation function that returns stem file paths
    
    Args:
        input_file: Path to audio file
        model: Demucs model to use
    
    Returns:
        Dictionary mapping stem names to file paths
    """
    demucs = DemucsWrapper(model=model)
    output_dir = demucs.separate(input_file)
    return demucs.get_stems(output_dir)
