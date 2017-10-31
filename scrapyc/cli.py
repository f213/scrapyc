from urllib.parse import urlparse

import click

from scrapyc import ScrapydClient


def validate_url(ctx, param, value):
    if value is None:
        raise click.UsageError('Please supply a crapyd URL (e.g. --url http://localhost:6800)')

    parsed = urlparse(value)
    if not len(parsed.scheme) or not len(parsed.netloc):
        raise click.BadParameter('Invalid scrapyd URL. Valid one should start with http:// or https://')

    return value


@click.group()
@click.option('--url', type=click.STRING, callback=validate_url, help='scrapyd URL')
@click.option('--username', type=click.STRING, help='(Optional) Username for basic authorization')
@click.option('--password', type=click.STRING, help='(Optional) Password for basic authorization')
@click.pass_context
def cli(ctx, url, username=None, password=None):
    ctx.obj['client'] = ScrapydClient(url, username, password)


@cli.command(short_help='Run a project')
@click.argument('project', type=click.STRING)
@click.option('--spider', default='spider', type=click.STRING, help='(Optional) spider name')
@click.pass_context
def schedule(ctx, project, spider):
    ctx.obj['client'].schedule(project, spider)


def main():
    return cli(
        obj=dict(),
        auto_envvar_prefix='SCRAPYC',
    )
