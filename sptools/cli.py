import click


# @click.group()
# def db():
#     pass
#
#
# @db.command('hello')
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)
#
#
# @db.command('hi')
# def hi():
#     """Clear the existing data and create new tables."""
#     click.echo('Initialized the database.')
#
#
# if __name__ == '__main__':
#     db()
@click.group()
@click.option('--debug/--no-debug', '-d/-nd', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
def sync(ctx):
    click.echo('Debug is %s' % (ctx.obj['DEBUG']))


if __name__ == '__main__':
    cli(obj={})
