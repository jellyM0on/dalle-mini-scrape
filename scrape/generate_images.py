import logging
import requests
from typing import List

logger = logging.getLogger(__name__)

def generate_images(endpoint: str, prompt: str, timeout: int = 60) -> List[str]:
    logger.debug("POST %s prompt=%r", endpoint, prompt)

    resp = requests.post(
        endpoint,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"prompt": prompt},
        timeout=timeout,
    )

    resp.raise_for_status()
    data = resp.json()
    images = data.get("images", []) or []
    logger.info("Endpoint returned %d image(s)", len(images))
    return images
