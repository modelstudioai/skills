"""spark-video lib — pure helpers (schemas, ffmpeg wrappers, manifest scanners).

Scripts under scripts/ import from here. No direct API calls live in lib/ —
those go through ./scripts/bl (so they're logged) or scripts/providers/.
"""
__version__ = "0.2.0"
