import base64, pathlib, time, logging, os, argparse

from scrape.drive_client import DriveClient
from scrape.generate_images import generate_images

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

OUT_DIR = pathlib.Path("outputs")

# Utils
def decode_and_save(b64png: str, path: pathlib.Path) -> pathlib.Path:
    png_bytes = base64.b64decode(b64png)
    path.write_bytes(png_bytes)
    return path

def upload_and_cleanup(drive: DriveClient, file_path: pathlib.Path, folder_id: str) -> None:
    try:
        drive.upload_png(str(file_path), folder_id)
        os.remove(file_path)
        logger.info("Uploaded and deleted local file: %s", file_path)
    except Exception as e:
        logger.exception("Upload failed for %s: %s", file_path, e)


def main(prompt: str, start_call: int, end_call: int, folder_id: str, endpoint: str, delay: int):
    if start_call <= 0 or end_call <= 0:
        raise ValueError("--start and --end must be positive integers.")
    if start_call > end_call:
        raise ValueError("--start cannot be greater than --end.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    drive = DriveClient(credentials_path="credentials.json", token_path="token.pickle")

    total = end_call - start_call + 1
    for idx, call in enumerate(range(start_call, end_call + 1), start=1):
        logger.info("Request %d/%d (call index=%d)...", idx, total, call)

        try:
            # Images are returned as base64
            b64_images = generate_images(endpoint, prompt)
        except Exception as e:
            logger.exception("Generation call failed (index %d): %s", call, e)
            if call < end_call:
                time.sleep(delay)
            continue

        for i, b64png in enumerate(b64_images, start=1):
            first_word = prompt.split()[0]
            path = OUT_DIR / f"{first_word}_{call:02d}_{i:02d}.png"

            decode_and_save(b64png, path)
            upload_and_cleanup(drive, path, folder_id)

        if call < end_call:
            time.sleep(delay)

    logger.info("All requests done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images and upload to Google Drive")
    parser.add_argument("--prompt", required=True, help="Prompt")
    parser.add_argument("--start", type=int, default=1, help="Starting call index (inclusive)")
    parser.add_argument("--end", type=int, required=True, help="Ending call index (inclusive)")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder ID")
    parser.add_argument("--endpoint", default="https://bf.pcuenca.net/generate", help="Endpoint URL")
    parser.add_argument("--delay", type=int, default=10, help="Delay between calls")

    args = parser.parse_args()
    main(args.prompt, args.start, args.end, args.folder_id, args.endpoint, args.delay)