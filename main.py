from api.server import launch
from cli.command import parse_cli


if __name__ == "__main__":
    args = parse_cli()

    launch(app="api.server:application",
           host=args['--host'],
           port=args['--port'])
