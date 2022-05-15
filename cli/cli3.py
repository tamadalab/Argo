import click
import glob

cli3 = click.Group()

@cli3.command(help = 'list available queries and metrics.')
@click.option('-M', '--metrics_dir', 'metrics_dir',
                help = 'specify the directory contains chart scripts.')
@click.option('-Q', '--queries_dir', 'queries_dir',
                help = 'specify the directory contains GraphQL queries.')
def list(metrics_dir, queries_dir):
    if metrics_dir != None:
        dir = "metrics"
    else:
        dir = "queries/format/"
    
    files = glob.glob(dir)
    for file in files:
        print(file)