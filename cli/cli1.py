import click
from queries import Star, Issue, PullRequest

cli1 = click.Group()

@cli1.command(help = 'fetch data from GitHub.')
@click.option('-q','--query', 'query',
                help = 'specify the query. This option is mandatory.', 
                required = True, 
                type = click.Choice(['Star', 'Issue', 'PullRequest']))
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
    if query == 'Star':
        Star.main(args, cache_dir, no_cache)
    elif query == 'Issue':
        Issue.main(args, cache_dir, no_cache)
    else:
        PullRequest.main(args, cache_dir, no_cache)
    