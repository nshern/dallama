import argparse
import os

from model import Model


def ensure_directory_exists():
    directory = os.path.expanduser("~/.config/llama_farm")
    if not os.path.isdir(directory):
        print(f"Creating config directory in {directory}...")
        os.makedirs(directory)

    return directory


def clean(directory):
    for f in os.listdir(directory):
        os.remove(f"{directory}/{f}")


def view_models():
    pass


def create_model(args):
    if "base_model" in args:
        base_model = args.base_model

    if "parameters" in args:
        parameters = args.parameters

    if "template" in args:
        template = args.template

    if "system" in args:
        system = args.system

    if "adapter" in args:
        adapter = args.adapter

    if "license" in args:
        license = args.license

    model = Model(
        base_model=base_model,  # type: ignore
        parameters=parameters,  # type: ignore
        template=template,  # type: ignore
        system=system,  # type: ignore
        adapter=adapter,  # type: ignore
        license=license,  # type: ignore
    )

    model.create_model()


def parse_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    clean_parser = subparser.add_parser("clean", help="delete all modelfiles")
    clean_parser.set_defaults(clean=clean)

    create_parser = subparser.add_parser("create", help="create new model")
    clean_parser.set_defaults(create=create_model)
    create_parser.add_argument("-b", "--base-model", required=True)
    create_parser.add_argument("-p", "--parameters")
    create_parser.add_argument("-t", "--template")
    create_parser.add_argument("-s", "--system")
    create_parser.add_argument("-a", "--adapter")
    create_parser.add_argument("-l", "--license")

    view_parser = subparser.add_parser("view", help="view models")
    view_parser.set_defaults(view=view_models)

    args = parser.parse_args()

    return args


def main():
    directory = ensure_directory_exists()

    args = parse_args()

    if "clean" in args:
        clean(f"{directory}/modelfiles")

    if "create" in args:
        create_model(args)


if __name__ == "__main__":
    main()
