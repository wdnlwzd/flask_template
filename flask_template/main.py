import click
import os
import os.path
import sh


HERE = os.path.abspath(os.path.dirname(__file__))


@click.group()
def cli():
    pass


def get_templates():
    dirs = os.scandir(os.path.join(HERE, 'templates'))
    templates = []
    for entry in dirs:
        if entry.is_dir():
            templates.append(entry.name)
    return templates


@cli.command()
@click.option('-t', '--template', default='simple', help='template')
@click.argument('project_name')
def create(template, project_name):
    templates = get_templates()
    if template not in templates:
        click.echo('%s template not found' % template, err=True)
        return
    project_dir = './' + project_name
    sh.mkdir('-p', project_dir)
    sh.cp('-rf', os.path.join(HERE, 'templates/simple/'), project_dir)
    for f in sh.find(project_dir, '-name', '*.py'):
        sh.sed('-i', '', '-e', 's/%s/%s/g' % ('proj', project_name), f.strip())
    sh.mv(os.path.join(project_dir, 'proj'), os.path.join(project_dir, project_name))


@cli.command()
def list():
    templates = get_templates()
    for t in templates:
        print(t)


if __name__ == '__main__':
    cli()
