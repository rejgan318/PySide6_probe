from pathlib import Path
from time import perf_counter
from random import sample


def playload(file_name:str, fraction: float = 0.1) -> float:

    start = perf_counter()
    content = Path(file_name).read_bytes()
    _ = sample(content, int(len(content) * fraction))

    return perf_counter() - start


if __name__ == '__main__':

    files_dir = r"s:\MyMedia\Фото\Семейка\20210828 Фабрика с семьей"
    files = list(Path(files_dir).glob("*.jpg"))
    load_times = [playload(str(file)) for file in files]

    print(f"Среднее время: {sum(load_times) / len(load_times):6.1f}\n"
          f"Общее время:   {sum(load_times):6.1f}")


