import argparse
import os.path as osp
from collections import defaultdict

import yaml
from cerberus import Validator

collection_schema = {
    'Name': {
        'type': 'string'
    },
    'Metadata': {
        'type': 'dict',
        'required': False,
        'schema': {
            'Training Data': {
                'type': ['string', 'list'],
                'schema': {
                    'type': 'string'
                },
                'required': False,
            },
            'Epochs': {
                'type': 'integer',
                'required': False,
            },
            'Batch Size': {
                'type': 'integer',
                'required': False,
            },
            'Training Techniques': {
                'type': 'list',
                'schema': {
                    'type': 'string'
                },
            },
            'Training Resources': {
                'type': 'string',
                'required': False,
            },
            'FLOPs': {
                'type': 'number',
                'required': False,
            },
            'Parameters': {
                'type': 'integer',
                'required': False,
            },
            'Training Time': {
                'type': 'number',
                'required': False,
            },
            'Train time (s/iter)': {
                'type': 'number',
                'required': False,
            },
            'Training Memory (GB)': {
                'type': 'float',
                'required': False,
            },
            'Architecture': {
                'type': 'list',
                'required': False,
                'schema': {
                    'type': 'string',
                }
            }
        },
    },
    'Paper': {
        'type': 'dict',
        'required': False,
        'schema': {
            'URL': {
                'type': 'string'
            },
            'Title': {
                'type': 'string'
            },
        },
    },
    'README': {
        'type': 'string'
    },
    'Weights': {
        'type': 'string'
    },
}

model_schema = {
    'Name': {
        'type': 'string'
    },
    'In Collection': {
        'type': 'string',
    },
    'Metadata': {
        'type': 'dict',
        'schema': {
            'Training Data': {
                'type': ['string', 'list'],
                'schema': {
                    'type': 'string'
                },
                'required': False,
            },
            'Epochs': {
                'type': 'integer',
                'required': False,
            },
            'Batch Size': {
                'type': 'integer',
                'required': False,
            },
            'Training Techniques': {
                'type': 'list',  # ['string', 'list'] may be better
                'schema': {
                    'type': 'string'
                },
                'required': False,
            },
            'Training Resources': {
                'type': 'string',
                'required': False,
            },
            'FLOPs': {
                'type': 'number',
                'required': False,
            },
            'Parameters': {
                'type': 'integer',
                'required': False,
            },
            'Training Time': {
                'type': 'number',
                'required': False,
            },
            'Train time (s/iter)': {
                'type': 'number',
                'required': False,
            },
            'Training Memory (GB)': {
                'type': 'float',
                'required': False,
            },
            'Architecture': {
                'type': 'list',  # ['string', 'list'] may be better
                'required': False,
                'schema': {
                    'type': 'string',
                }
            },
            'inference time (ms/im)': {
                'type': 'list',
                'required': False,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'value': {
                            'type': 'float',  # 'number' may be better
                        },
                        'hardware': {
                            'type': 'string',
                        },
                        'backend': {
                            'type': 'string',
                        },
                        'batch size': {
                            'type': 'integer',
                        },
                        'mode': {
                            'type': 'string',
                        },
                        'resolution': {
                            'type': 'list',
                        }
                    },
                },
            },
        },
    },
    'Results': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'Task': {
                    'type': 'string'
                },
                'Dataset': {
                    'type': 'string'
                },
                'Metrics': {
                    'type': 'dict',
                }
            }
        },
    },
    'Config': {
        'type': 'string'
    },
    'Weights': {
        'type': 'string',
        'required': False
    },
    'Training Log': {
        'type': 'string',
        'required': False
    },
    'README': {
        'type': 'string',
        'required': False
    },
    'Paper': {
        'type': 'dict',
        'required': False,
        'schema': {
            'URL': {
                'type': 'string',
                'required': False
            },
            'Title': {
                'type': 'string'
            },
        },
    },
    'Converted From': {
        'type': 'dict',
        'required': False,
        'schema': {
            'Weights': {
                'type': 'string'
            },
            'Code': {
                'type': 'string'
            },
        },
    },
    'Image': {
        'type': 'string',
        'required': False,
    },
    'Code': {
        'type': 'dict',
        'required': False,
        'schema': {
            'URL': {
                'type': 'string'
            },
            'Version': {
                'type': 'string'
            }
        }
    }
}

collection_validatetor = Validator(collection_schema)
model_validatetor = Validator(model_schema)


def load_metafile(path: str):
    if not osp.exists(path):
        print(f'File "{path}" does not exist.')
        return None

    with open(path) as f:
        raw = yaml.load(f, Loader=yaml.SafeLoader)

    return raw


def check_model_index(path: str) -> bool:
    retv = 0
    error_messages = defaultdict(dict)
    collection_names = defaultdict(list)
    model_names = defaultdict(list)
    model_index_data = load_metafile(path)

    if model_index_data is None or not isinstance(model_index_data, dict):
        print('Expected the file {path} to contain a dict, '
              f'but got {model_index_data}')
        retv = 1
    else:
        for metafile_path in model_index_data['Import']:
            metafile_data = load_metafile(metafile_path)

            error_message = {}
            if metafile_data is not None:
                collections = metafile_data.get('Collections')
                if collections is not None:
                    for collection in collections:
                        collection_names[collection['Name']].append(
                            metafile_path)
                        if not collection_validatetor.validate(collection):
                            error_message.setdefault('collections', {})
                            error_message['collections'][collection[
                                'Name']] = collection_validatetor.errors
                            retv = 1

                models = metafile_data.get('Models')
                if models is not None:
                    for model in models:
                        model_names[model['Name']].append(metafile_path)
                        if not model_validatetor.validate(model):
                            error_message.setdefault('models', {})
                            error_message['models'][
                                model['Name']] = model_validatetor.errors
                            retv = 1

            else:
                retv = 1

            if len(error_message) > 0:
                error_messages[metafile_path] = error_message

    for name, paths in collection_names.items():
        if len(paths) > 1:
            print(f'Collection "{name}" is defined in multiple places:')
            for path in paths:
                print(f'\t{path}')

            retv = 1

    for name, paths in model_names.items():
        if len(paths) > 1:
            print(f'Model "{name}" is defined in multiple places:')
            for path in paths:
                print(f'\t{path}')

            retv = 1

    for path, msg in error_messages.items():
        print(f'\n{path}')
        for k, v in msg.items():
            print(f'\t{k}: {v}')

    return retv


def main():
    parser = argparse.ArgumentParser(description='Check model index')
    parser.add_argument('filename', help='model-index file path')
    args = parser.parse_args()

    retv = check_model_index(args.filename)

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
