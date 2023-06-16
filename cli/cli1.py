import click
import pandas as pd
import os
from queries import Star, Issue, PullRequest, Fork

cli1 = click.Group()

@cli1.command(help = 'fetch data from GitHub.')
@click.option('-q','--query', 'query',
                help = 'specify the query. This option is mandatory.', 
                required = True, 
                type = click.Choice(['Star', 'Issue', 'PullRequest', 'Fork']))
@click.option('-c', '--cache_dir','cache_dir',
                help = 'specify the cache directory path.',
                default = True)
@click.option('--no_cache', 'no_cache',
                help = 'no cache the fetched data.',
                type = bool,
                default = False)
@click.argument('args',
                nargs = -1) #nargs で可変長で値が受け取れる．
def fetch(query, args, cache_dir, no_cache):
    names = []
    names = parse_args(args)

    if query == 'Star':
        Star.main(names, cache_dir, no_cache)
    elif query == 'Issue':
        Issue.main(names, cache_dir, no_cache)
    elif query == 'PullRequest':
        PullRequest.main(names, cache_dir, no_cache)
    elif query == 'Fork':
        Fork.main(names, cache_dir, no_cache)

def parse_args(args):
    names = []
    for arg in args:
        if is_csv_file(arg):
            df = pd.read_csv(arg)
            names.extend(df["name"].tolist())
        elif os.path.isdir(arg):
            for filename in os.listdir(arg):
                filepath = os.path.join(arg, filename)
                _, ext = os.path.splitext(filepath)
                if ext.lower() != ".csv":
                        continue
                df = pd.read_csv(filepath)
                names.extend(df['name'].tolist())
        else:
            names.append(arg)
    return names

def is_csv_file(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() == '.csv'
