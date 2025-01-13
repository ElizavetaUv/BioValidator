import argparse
from pathlib import Path
import httpx
import sys


BASE_API_PATH = "http://localhost:8083"


def _create_reference(client: httpx.Client, name: str) -> None:
    resp = client.post(
        "./references",
        json={
            "name": name,
        }
    )
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 409:
            return
        print(exc.response.text, file=sys.stderr)
        sys.exit(1)

def _add_mutations(client: httpx.Client, name: str, mutations_path: Path) -> None:
    with mutations_path.open("rb") as fd:
        resp = client.post(
            f"./references/{name}/calculate/mutations",
            files={
                "file": fd
            }
        )
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(exc.response.text, file=sys.stderr)
            sys.exit(1)

            raise exc

def _validate(mutations_path: Path) -> None:
    if not mutations_path.exists():
        print(f"Such path: '{str(mutations_path)}' doesn't exist", file=sys.stderr)
        sys.exit(1)
    
    if mutations_path.is_dir():
        print(f"Path '{str(mutations_path)}' is a directory", file=sys.stderr)
        sys.exit(1)


def add_reference(name: str, mutations_path: Path) -> None:
    client = httpx.Client(base_url=BASE_API_PATH)
    _create_reference(client=client, name=name)
    _add_mutations(client=client, name=name, mutations_path=mutations_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='Reference Adder',
        description='<>',
        epilog='<>'
    )
    parser.add_argument('-n', '--name', required=True, help="Reference name")
    parser.add_argument('-mp', '--mutations-path', required=True, type=Path, help="Reference mutations path")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    name = args.name
    mutations_path = args.mutations_path

    _validate(
        mutations_path=mutations_path,
    )
    add_reference(
        name=name,
        mutations_path=mutations_path
    )


if __name__ == "__main__":
    main()
