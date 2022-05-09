from email.policy import default
from xmlrpc.client import boolean
import click
from fetch import Star
from fetch import Issue
from fetch import PullRequest
from draw import N_STAR
from draw import N_RIS
from draw import R_RIS
from draw import LT_CIS
from draw import N_MGCL
from draw import R_MGPR
from draw import R_PRLP
from draw import LT_PR


@click.group()
def cli():
    pass


@cli.command()
@click.option('-q','-query', 
                help = 'specify the query. This option is mandatory.', 
                required = True, 
                type = click.Choice(['Star', 'Issue', 'PullRequest']))
@click.option('-c', '-cache_dir',
                help = 'specify the cache directory path.',
                default = True)
@click.option('-no_cache', 
                help = 'no cache the fetched data.',
                type = boolean,
                default = False)
@click.argument('args',
                nargs = -1) #nargs で可変長で値が受け取れる．
def fetch(q, args, c, no_cache):
    if q == 'Star':
        Star.main(args, c, no_cache)
    elif q == 'Issue':
        Issue.main(args, c, no_cache)
    else:
        PullRequest.main(args, c, no_cache)

@cli.command()
@click.option('-m','-metric',
                help = 'specify the metric (chart script). This option is mandatory.',
                required = True,
                type = click.Choice(['N_STAR', 'N_RIS', 'R_RIS', 'LT_CIS', 
                                    'N_MGCL','R_MGPR', 'R_PRLP', 'LT_PR']))
@click.option('-f', '-format',
                help = 'specify the output image format. available: pdf, svg, and png. default: svg.',
                type = click.Choice(['pdf', 'svg', 'png']),
                default = 'png')
@click.option('-c', '-cache_dir', 
                help = 'specify the cache directory path.',
                default = "Graph_image")
@click.option('-d', '-write_data', 
                help = 'set file name of graph data destination. if this option is absent, argo outputs no graph data.',
                default = None)
@click.argument('args',
                nargs = -1)
def draw(m, args, f, c, d):
    if m == 'N_STAR':
        N_STAR.main(args, f, c, d)
    elif m == 'N_RIS':
        N_RIS.main(args, f, c, d)
    elif m == 'R_RIS':
        R_RIS.main(args, f, c, d)
    elif m == 'LT_CIS':
        LT_CIS.main(args, f, c, d)
    elif m =='N_MGCL':
        N_MGCL.main(args, f, c, d)
    elif m =='R_MGPR':
        R_MGPR.main(args, f, c, d)
    elif m =='R_PRLP':
        R_PRLP.main(args, f, c, d)
    elif m == 'LT_PR':
        LT_PR.main(args, f, c, d)



if __name__ == '__main__':
    cli()