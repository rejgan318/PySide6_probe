from random import sample
from pathlib import Path

import requests

# Set False if you don't use tqdm. Else 'pip install tqdm'
USE_TQDM = True
if USE_TQDM:
    from tqdm import tqdm


def download_random_images(path: str = None,
                           count: int = None,
                           size: tuple[int, int] = None,
                           use_tqdm: bool = False) -> list[str]:
    """
    Download random images from picsum.photos
        Note: We can use same threads with count=1

    :param path: directory for downloaded images. Must be. Default: current directory
    :param count: Count of images to download. Default: 1
    :param size: Size of image (width, height) in pixels. Default: (300, 200)
    :param use_tqdm: True to show tqdm progress indicator. Default False

    :return: List of downloaded images full names
    """
    path = Path(path or Path.cwd())
    count = count or 1
    size = size or (300, 200)
    url = f'https://picsum.photos/{size[0]}/{size[1]}'  # returns random image every time

    range_images = range(count)
    if USE_TQDM:
        range_images = range_images if not use_tqdm else tqdm(range_images, desc="Downloading images")

    random_nums = sample(range(10000), count)
    images = []
    for i in range_images:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = f'{size[0]}x{size[1]}_{random_nums[i]:04}.jpg'
            full_name = str(path / image_name)
            with open(full_name, 'wb') as file:
                file.write(response.content)
        images.append(full_name)

    return images


if __name__ == "__main__":
    # Example usage

    from pprint import pprint

    # parameters by default
    random_images = download_random_images()
    print(f"Downloaded to current directory image {Path(random_images[0]).name}")

    IMG_PATH = r"random_images"
    IMG_COUNT = 3
    IMG_SIZE = (400, 400)
    print(f"Download {IMG_COUNT} images to {IMG_PATH} size {IMG_SIZE[0]}x{IMG_SIZE[1]}px")
    Path(IMG_PATH).mkdir(parents=True, exist_ok=True)
    random_images = download_random_images(path=IMG_PATH, count=IMG_COUNT, size=IMG_SIZE, use_tqdm=True)
    pprint(random_images)
