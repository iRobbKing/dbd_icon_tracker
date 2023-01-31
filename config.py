import tomllib

_STATUS_ICONS_CONFIG = 'config/icons.toml'
_COORDINATES_CONFIG = 'config/coordinates.toml'


def _read_status_icons():
    with open(_STATUS_ICONS_CONFIG, 'rb') as file:
        return tomllib.load(file)


def _get_required_data(required_data, read_data):
    for option in required_data:
        if option not in read_data:
            raise ValueError(f'Failed read option {option} from "{_COORDINATES_CONFIG}".')

        yield option, read_data[option]


def _read_coordinates():
    required_data = (
        'survivor_portrait',
        'next_survivor_offset',
        'action_offset',
        'action_size',
    )

    with open(_COORDINATES_CONFIG, 'rb') as file:
        read_data = tomllib.load(file)

    return dict(_get_required_data(required_data, read_data))


STATUSES = _read_status_icons()
COORDINATES = _read_coordinates()
