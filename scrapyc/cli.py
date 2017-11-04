# -*- coding: utf-8 -*-
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import click
import six

from scrapyc import ScrapydClient, exceptions


def validate_url(ctx, param, value):
    if value is None:
        raise click.UsageError('Please supply a crapyd URL (e.g. --url http://localhost:6800), or use SCRAPYC_URL environment variable')

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

    try:
        ctx.obj['client'].get_status()
    except exceptions.UnAuthorizedException:
        raise click.ClickException('Got 401 error during query to %s, please double-check username and password.' % url)


@cli.command(short_help='Run a project')
@click.argument('project', type=click.STRING)
@click.option('--spider', default='spider', type=click.STRING, help='(Optional) spider name')
@click.pass_context
def schedule(ctx, project, spider):
    try:
        response = ctx.obj['client'].schedule(project, spider)
    except exceptions.ProjectDoesNotExist:
        raise click.ClickException('Given project "%s" does not exist on %s' % (project, ctx.obj['client'].host))
    except exceptions.SpiderDoesNotExist:
        raise click.ClickException('Given spider "%s" is not present in the project %s' % (spider, project))

    log_link = ctx.obj['client'].get_log_link(project, spider, response['jobid'])

    click.secho('OK', fg='green', nl=False)
    click.echo(', %s' % log_link)


@cli.command(short_help='List spiders')
@click.argument('project', type=click.STRING)
@click.pass_context
def spiders(ctx, project):
    try:
        spiders = list(ctx.obj['client'].list_spiders(project))
    except exceptions.ProjectDoesNotExist:
        raise click.ClickException('Given project "%s" does not exist on %s' % (project, ctx.obj['client'].host))

    for spider in spiders:
        click.echo(spider)


@cli.command(short_help='List projects')
@click.pass_context
def projects(ctx):
    for project in ctx.obj['client'].list_projects():
        click.echo(project)


@cli.command(short_help='Get daemon status')
@click.pass_context
def status(ctx):
    status = ctx.obj['client'].get_status()

    node_name = status.pop('node_name')
    st = status.pop('status')
    click.echo('Scrapyd node name: ', nl=False)
    click.secho(node_name, fg='blue', nl=False)
    click.echo(', status: ', nl=False)
    click.secho(st.upper(), fg='green')
    click.echo()

    for key, value in six.iteritems(status):
        click.echo(key.title() + ': ', nl=False)
        click.secho(str(value), fg='green')


def main():
    return cli(
        obj=dict(),
        auto_envvar_prefix='SCRAPYC',
    )
