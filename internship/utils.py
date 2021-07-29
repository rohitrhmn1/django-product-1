import random
import string
from pathlib import Path


def user_image_upload_path(instance, filepath):
    ext = Path(filepath).suffix
    return "user_profile/" + f"{instance.unique_id}/" + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) + ext


def unique_id_generator():
    return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
