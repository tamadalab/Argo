import click
from scripts_ import N_STAR, N_RIS, R_RIS, LT_CIS, N_MGCL, R_MGPR, R_PRLP, LT_PR

cli2 = click.Group()

@cli2.command(help = 'draw line chart from fetched data.')
@click.option('-m','--metric', 'metric', 
                help = 'specify the metric (chart script). This option is mandatory.',
                required = True,
                type = click.Choice(['N_STAR', 'N_RIS', 'R_RIS', 'LT_CIS', 
                                    'N_MGCL','R_MGPR', 'R_PRLP', 'LT_PR']))
@click.option('-f', '--format', 'format',
                help = 'specify the output image format. available: pdf, svg, and png. default: svg.',
                type = click.Choice(['pdf', 'svg', 'png']),
                default = 'png')
@click.option('-c', '--cache_dir', 'cache_dir', 
                help = 'specify the cache directory path.',
                default = "Graph_image")
@click.option('-d', '--write_data', 'write_data', 
                help = 'set file name of graph data destination. if this option is absent, argo outputs no graph data.',
                default = None)
@click.argument('args',
                nargs = -1)
def draw(metric, args, format, cache_dir, write_data):
    if metric == 'N_STAR':
        N_STAR.main(args, format, cache_dir, write_data)
    elif metric == 'N_RIS':
        N_RIS.main(args, format, cache_dir, write_data)
    elif metric == 'R_RIS':
        R_RIS.main(args, format, cache_dir, write_data)
    elif metric == 'LT_CIS':
        LT_CIS.main(args, format, cache_dir, write_data)
    elif metric =='N_MGCL':
        N_MGCL.main(args, format, cache_dir, write_data)
    elif metric =='R_MGPR':
        R_MGPR.main(args, format, cache_dir, write_data)
    elif metric =='R_PRLP':
        R_PRLP.main(args, format, cache_dir, write_data)
    elif metric == 'LT_PR':
        LT_PR.main(args, format, cache_dir, write_data)

    