import os
from pathlib import Path
from moondream import MoondreamModel  # your base class

class HfMoondream(MoondreamModel):

    @classmethod
    def from_pretrained(cls, *args, **kwargs):

        path = args[0]

        # =========================
        # FORCE LOCAL PATH ONLY
        # =========================
        path = os.path.abspath(path)

        if not os.path.exists(path):
            raise ValueError(f"Model path does not exist: {path}")

        kwargs["local_files_only"] = True
        kwargs["trust_remote_code"] = False

        return super().from_pretrained(path, **kwargs)
