import click

from .generate import generate_elm_client


@click.command()
@click.argument('spec-file', type=click.Path(exists=True, dir_okay=False, readable=True, file_okay=True))
@click.argument('module-name')
def main(spec_file, module_name):
    code = generate_elm_client(spec_file, module_name)
    print(code)
    return 0


if __name__ == '__main__':
    main()