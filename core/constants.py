DEFAULT_COLOR = '#FFFFFF'
COLORS = {'#0000FF': 'ca',
          '#149E9C': 'bd',
          '#18930B': 'bb',
          '#20F606': 'ba',
          '#24AEFF': 'bc',
          '#610081': 'da',
          '#90C423': 'cc',
          '#A34B0A': 'ac',
          '#C8005D': 'db',
          '#C8B02A': 'ad',
          '#D464F0': 'dc',
          '#D900CC': 'cd',
          '#EC2809': 'ea',
          '#EE9A28': 'ed',
          '#EFD276': 'ec',
          '#F0C0C1': 'ab',
          '#F0FD39': 'cb',
          '#FB0007': 'aa',
          '#FD8609': 'dd',
          '#FDC50B': 'eb',
          '#5FFEEE': 'fa',
          '#C2CCDF': 'fb',
          '#596468': 'fc',
          '#000000': 'fd'}


def abbr2color(x):
    for k, v in COLORS.items():
        if v == x:
            return k
    return DEFAULT_COLOR


def color2abbr(x):
    return COLORS.get(x, "")
